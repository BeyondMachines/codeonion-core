get visit 
render form
sumbmit link
validate that it's a url
get the domain and validate
if valid domain get the path and send it to scanner/reporter

Scanner:
look for repo in db.
if repo found and scan completed (has a scan date) check for the scan date. 
if the scan date is less than 6 months old
query for the repo/dependency pairs and return them
if more than 6 months old, send to new scan.

if repo not found, or scan is not completed or scan older than 6 months,
get the repo dependencies
for each dependency
query dependency date
if dependency in db and scan less than 1 month, query dependency pair and return status, and save/update depenency
if dependency not in db or scan more than 1 month
look up dependency

return dependency and update the dependency db and the repo/pair dependency
go to next dependency
when finshed, update the repo scan (add new scan date)
query for the repo/dependency pairs and return them


Detailed program flow for each function

User visits home view:
Get Home view: 
    Executes `home_view` from `main`
    `gets scope_message` and `url_instructons_message` from the Message objects in DB. 
    renders the empty form for the request submission

Post Home view
    Executes `home_view` from `main`
    Populates the `request_url` from the variable `repository` in the POST request (The input object name is `repository` in the form )
    Checks if the URL is one of a valid repository, and parses out the `repo_type` (now only "github") and the `repo_path` (the path after `github.com`)
    If repo not valid returns a message that the repo isn't valid and quotes the request url. 
    If repo valid tries to open a github connection to the `repo_path`
    If github connection not valid, changes the `url_instructons_message` that the path is not valid and returns the URL.
    If github connection is valid:
        Check if the repo is already in DB (already scanned)
            If the repo is in DB, 
                If repo scan is not older than 90 days
                    return the UUID of the repo from DB and a marker that the scan is complete
                If repo scan is older than 90 days or not present
                    executes a new scan process
                    returns the UUID of the repo from DB and a marker that the scan is not complete
                    returns the status of the process
    The Javascript:
        if the scan_is_complete
            send the request to the API to get the results
        if the scan is not complete
            long poll for the api complete
            when api is complete send the request to the API to get the results


    ```Modification```
                If repo scan is not older than 90 days
                    return some parameter that will invoke the get to the scanned db API
                    how do I block people from bombarding the API? Do I want to block people from bombarding the API?
                    
                If repo scan is older than 90 days or not present
                    executes a new scan process
                    returns the status of the process

