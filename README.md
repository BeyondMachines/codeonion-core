# codeonion-core
The initial implementation of the codeonion product code


# Running locally

## Installation to run locally

1. Install Docker on your computer and make sure it runs properly
2. create a project container folder. Make sure you DONT name the project container `codeonion-core` - otherwise zappa will complain.
3. Enter the project folder and set up virtualenv in it (`virtualenv -p python3 .`) 
4. Activate the virtualenv (`source bin/activate`)
5. In the project container folder clone thw codeonion-core project from github
6. Enter the codeonion-core project and run the pip install -r requirements.txt
7. Generate your own local `secret_key.txt` file in the `codeonion-core` so Django will run:
```
LC_ALL=C </dev/urandom tr -dc 'A-Za-z0-9!"#$%&()*+,-./:;<=>?@[\]^_`{|}~' | head -c 50 > secret.txt
    echo DJANGO_SECRET_KEY='"'`cat secret.txt`'"' > django_env.txt
    rm secret.txt
```
8. Apply all migrations `python manage.py migrate`
9. Populate fixtures to the database `python manage.py loaddata main/fixtures/Message.json --app main.Message`
10. Generate your own API personal access token key in github and store it in a file `github_key.txt` in the `codeonion-core` folder. Go to `https://github.com/settings/tokens` to generate it. Set it to 90 days expiration. Give it only repo/public_repo permissions.
11. Run the server from the `codeonion-core` folder using `python manage.py runserver`
12. Go to http://127.0.0.1:8000 to see the page. Test that it's running locally by pasting the following URL: https://github.com/Miserlou/Zappa

## Documentation (sort of)
See the program_flow.md of the program flow. More to come as we build it. 

## The Dockerfile 
The dockerfile is used to run the zappa tool properly regardless of the underlying platform (hopefully)


To build the docker image use the following command:
`docker build -t zappa-docker-image .`
To run the docker image use the `zappashell.sh` script. 
It will run the docker image and drop you in the command line of zappa. To check that everything is running run `zappa status`.

**Important prerequisites for the docker image to run properly**
1. The path in the Dockerfile on the line `WORKDIR /var/codeonion/codeonion-core` must be equal to the path in `zappashell.zh` in this section `"$(pwd):/var/codeonion/codeonion-core"`. Otherwise the docker won't be able to see your local folder with code to deploy it. 
2. The AWS profile in your ~/.aws/credentials must be named exactly as it's referenced in `zappashell.sh` in  the section `-e AWS_PROFILE=zappa `. Otherwise zappa won't be able to authenticate to AWS even if you have created a proper user. 


## Similar product
https://requires.io 

# New text for the team to add one thing

## Jasmin
### This is really cool.    
## Dragana

## Marko
## Hello World from Marko
## Marjan
##### Hello from Marjan
