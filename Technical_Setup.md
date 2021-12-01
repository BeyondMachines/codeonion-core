## Templates
### Basic concept:
The HTML templates for all pages start from one base template so it's fairly easy to manage the entire style of the site. 
All major elements that need to span all pages (general meta tags, general CSS, icon image etc) are loaded in the base template.
The basic template is called `base.html`. All other pages load the base template and add elements in their own tagged sections. 
The location of the templates are defined in the `TEMPLATES` block of the `settings.py`, in the section `DIRS` 

### TEMPLATES structure 
The structure of the TEMPLATES/DIRS is as follows. Put all relevant files in the appropriate subfolders. 

|- TEMPLATES/DIRS  
|   |- general  
|   |- home  
|   |   |- components

### Using templates
The general folder contains the root templates that need to be inherited by all files.
The home folder provides the pages that are available to the root url. 
The components subfolder contains the details of the blocks of the main page. Aim to break apart functioning elements into separate files so they can be reused elsewhere.


## Static files
### Basic concepts:
* STATICFILES_DIRS  - the paths where the static files are placed during development so they can be collected into the STATIC_ROOT during the `python manage.py collectstatic`
For our implementation the STATICFILES_DIRS is `static_data` in the root of the code folder.

* STATIC_ROOT - The absolute path to the directory where collectstatic will collect static files for deployment.
For our implementation the local version of STATIC_ROOT is `static_assets` in the root of the code folder.

* STATIC_URL - URL to use when referring to static files located in STATIC_ROOT.
    default: None
    Example: "/static/" or "http://static.example.com/"

### STATICFILES_DIRS structure
The structure of the STATICFILES_DIRS is as follows. Put all relevant files in the appropriate subfolders. They will be replicated during the python manage.py collectstatic.

|- STATICFILES_DIRS  
|   |- js  
|   |- img  
|   |- css  

### Using static files
Add all static files during development into the STATICFILES_DIRS folder. That folder IS part of the code and must be included in the repo. 
The STATIC_ROOT is populated from STATICFILES_DIRS using  `python manage.py collectstatic`. This folder IS NOT part of the source code and shouldn't be included in the repo.
Please note that `collectstatic` will only collect and populate folders which are not empty.

### Placing static files to S3 bucket
While there are automated mechanisms for pushing the staticfiles to an S3 bucket, for small implementations and for rare changes of the static files you can upload manually. 
This is done to reduce costs, since S3 charges for uploads when they are frequent.
Just upload the STATIC_ROOT content to the root of the S3 bucket, and subsequently upload changed pieces one by one. 


## S3 Static files setup

### Create an S3 Bucket
For the test environment we have set up a bucket `codeonion-static-test` with the following setup
```
Block all public access
Bucket Versioning - Disable
Server-side encryption: Disabled
(Advanced) Object Lock: Disable
```

Add CORS policy to allow for public access
```
[
    {
        "AllowedHeaders": [],
        "AllowedMethods": [
            "GET"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
]
```

### Create a cloudfront distribution
Create a new cloudfront distribution with the following setup
```
Origin domain: codeonion-static-test.s3.us-east-2.amazonaws.com
Name: codeonion-static-test.s3.us-east-2.amazonaws.com
S3 bucket access: Yes use OAI (bucket can restrict access to only CloudFront
Origin access identity: 
Bucket policy: Yes, update the bucket policy
Enable Origin Shield: No
Distribution url: d1zr246difihfv.cloudfront.net
Distribution cname: pubcdn-test.codeonion.net
Compress by default
Viewer protocol policy: Redirect http to https
Allowed HTTP methods: GET, HEAD
Restrict viewer access: No
Cache policy and origin request policy: CachingOptimized
```
Create a cname record in the Route53 for pubcdn-test.codeonion.net to point to d1zr246difihfv.cloudfront.net

### Install django-storages
`pip install django-storages` to install django storages. 
Add the `'storages'` line to the `settings.py` file under `INSTALLED_APPS`
Add the configuration for the AWS parameters - docs here: https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html

### Copy files to the S3 bucket 
Copy the content of the local STATIC_ROOT folder to the S3 bucket and check if they are visible via the URL of the CDN.