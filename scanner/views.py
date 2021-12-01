from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, HttpResponseRedirect
import requests  # the http requests framework
from zappa.asynchronous import task, get_async_response  # the async communication framework in zappa
from django.http import JsonResponse  # to create
from django.urls import reverse_lazy  # reverse url for redirect to internal url view
from github import Github, GithubException  # the objects needed
from urllib.parse import urlparse  # this is needed for domain parsing
from time import sleep
import datetime
import json
from django.core.exceptions import ObjectDoesNotExist
import os
import boto3
import botocore
import uuid

# Import models

from scanner.models import Dependency, Repo_Dependency_Pair, Scanned_Repo 
from django.conf import settings

# Import functions

# Create your views here.
def get_local_ssm_key(name):
    ssm = boto3.client('ssm')
    try:
        key = ssm.get_parameter(Name=name, WithDecryption=True)
        return key['Parameter']['Value']
    except botocore.exceptions.ClientError as error:
        # print(error)
        return error


# spec: receives url to check for validity as a repo url. 
# If url valid, returns confirmation that the repo is valid, the repo type and the repo_path
# if url not valid, returns 
# receives: URL string from the frontend form
# returns: valid_repo_url: boolean (True if the URL string is valid path to repo, 
#           repo: string (which type of repo, currently 'github'))
#           path: string (the path part of the URL (after the TLD))
def check_valid_repo_url(repo_url):
    domain = urlparse(repo_url).netloc
    path = urlparse(repo_url).path[1:]

    if domain in ('github.com', 'www.github.com'):
        valid_repo_url = True
        repo = 'github'
        return(valid_repo_url, repo, path)
    else:
        valid_repo_url = False
        repo = None
        path = None
        return(valid_repo_url, repo, path)


# spec: receives repository name to check for validity of repo. 
# If repository name valid, opens a (at the moment) github repo connection and
# returns the repo connection. Otherwise raises an exception
# receives: repository: String ((the path part of the URL (after the github.com))
# returns: if successful, r: github repository object
#          if not successful raises an exception that the repo is not valid, and returns the requested string  path
def open_github_repo(repository):
    repo = None
    if str(settings.LOCAL_TEST) == 'True':
        GITHUB_FILE = 'github_key.txt'
        with open(GITHUB_FILE) as f:
            GITHUB_KEY = f.read().strip()
    else:
        GITHUB_KEY =  get_local_ssm_key("CODEFOX_GITHUB_KEY")
    g = Github(GITHUB_KEY)
    try:
        r = g.get_repo(repository)
    except GithubException as error:
        raise Exception('You didn\'t enter a valid GitHub Repo. The URL you entered is:' + repository)
    return r
    # if r.language.lower() in ['python']:
    #     r1 = scan_github_repo(r)
    #     return(r1) 


# spec: use this to prepopulate the uuid ids when adding the uuid migrations
def generate_uuid():
    repo_in_db = Scanned_Repo.objects.all()
    for i in repo_in_db:
        uid = uuid.uuid4()
        i.repo_id = uid
        i.save()


def update_repo_last_scan(repository):
    repo_in_db = Scanned_Repo.objects.get(repo_name=repository,repo_store='github')
    repo_in_db.repo_last_checked_date = datetime.datetime.now().date()
    repo_in_db.save()
    return(repo_in_db)



def save_repo(repository, store, language):
    new_repo = Scanned_Repo()
    new_repo.repo_name = repository
    new_repo.repo_store = store
    new_repo.repo_primary_language = language
    new_repo.save()
    return(new_repo)


def save_dependency(dependency, language, license):
    obj, created = Dependency.objects.update_or_create(dependency_name =dependency, dependency_language = language, dependency_license = license )
    return(obj)


def save_repo_dep_pair(repo, dependency):
    new_pair = Repo_Dependency_Pair()
    new_pair.repo = repo
    new_pair.dependency = dependency
    new_pair.save()
    return(new_pair)



def check_repo_in_db(repository):
    older_than_90_days = datetime.datetime.now() - datetime.timedelta(90)
    # print(repository)
    try:
        repo_in_db = Scanned_Repo.objects.get(repo_name=repository,repo_store='github')
        # print(repo_in_db)
        if repo_in_db.repo_last_checked_date:
            repo_exists = True
            # print(repo_exists)
            if repo_in_db.repo_last_checked_date < older_than_90_days.date():
                older = True
                # print(older)
            else:
                older = False
                # print(older)
        else:
            repo_exists = True  
            older = True
            # print(repo_exists,older)
    except ObjectDoesNotExist:
        repo_in_db = None
        repo_exists = False
        older = False
    return(repo_in_db, repo_exists, older)
    

# spec: receives a repo object, and then checks if it's already scanned or not and whether it's scanned in the last 90 days. 
# If scanned in last 90 days returns result from previous scan.
# if not scanned or older scan creates a record and starts a loop to find the repo dependencies, 
# scan them and at the end updates last scanned date to today.
# receives: repository: String ((the path part of the URL (after the github.com))
# returns: for asynchronous execution returns the task_id for async check
# returns: if successful, r: github repository object
#          if not successful raises an exception that the repo is not valid, and returns the requested string path
@task(capture_response=True)
def scan_github_repo(repo_name):
    repository = open_github_repo(repo_name)
    older_than_90_days = datetime.datetime.now() - datetime.timedelta(90)
    repo_in_db, repo_exists, older = check_repo_in_db(repository)
    print('fetching dependency files')
    dependency_files = get_dependency_files_from_repo(repository, 'python')
    if dependency_files: 
        print("looping through dependency files")
        dependency_dict = get_dependencies_from_dep_files(repository, dependency_files, 'python')
        scan_status = scan_repo_dependencies(repo_in_db, dependency_dict, 'python')
        Scanned_Repo.objects.filter(repo_name=repository,repo_store='github').update(repo_last_checked_date=datetime.datetime.now().date())
        # dep_in_db = Repo_Dependency_Pair.objects.filter(repo = repo_in_db)
        dep_uuid = Scanned_Repo.objects.get(repo_name=repository,repo_store='github').repo_id
        return(dep_uuid)
    else:
        print("no dependency files")
        dep_in_db = False
        dep_in_db_error_message = "Python repo " + repository.full_name + " doesn't have requirements.txt, requirements.in or Pipfile.lock"
        Scanned_Repo.objects.filter(repo_name=repository,repo_store='github').update(repo_last_checked_date=datetime.datetime.now().date())
        Scanned_Repo.objects.filter(repo_name=repository,repo_store='github').update(repo_scan_error=True)
        Scanned_Repo.objects.filter(repo_name=repository,repo_store='github').update(repo_scan_error_message=dep_in_db_error_message)
        dep_uuid = Scanned_Repo.objects.get(repo_name=repository,repo_store='github').repo_id
        return(dep_uuid)


# spec: receives dependency as string, finds license, creates a record of the dependency in the DB
# returns status code: 0 for success, -1 for errors or not found 
def lookup_dep_license(dependency, language):
    older_than_30_days = datetime.datetime.now() - datetime.timedelta(30)
    if language == 'python':
        base_url = 'https://pypi.org/pypi/'  # right now it only works for python, this should be changed to be more flexible for other languages
        package_url = dependency + '/json'
        url = base_url + package_url
    try:
        dep_in_db = Dependency.objects.get(dependency_name=dependency,dependency_language=language)
        if dep_in_db.dependency_license_last_checked_date < older_than_30_days.date():
            older = True
        else:
            older = False
    except ObjectDoesNotExist:
        dep_in_db = None
        older = True
    if not older and dep_in_db is not None:
        print('dependency',dependency,'newer',dep_in_db.dependency_license_last_checked_date)
        license_status = 0
        return(license_status, dep_in_db)
    else:
        try: 
            r = requests.get(url)
        except (requests.ConnectionError, requests.Timeout) as error:
            license_status = 1
            license_found = error
            return(license_status, license_found)
        if r:
            if r.status_code == 200:
                json_content = r.json()
            else:
                license_found = r.status_code
                license_status = -1
                return(license_status, license_found)
            try:
                license_found = json_content["info"]["license"]
            except JSONDecodeError: 
                license_found = "License Not found, please check manually"
            license_status = 0
            dep_in_db = save_dependency(dependency,language,license_found)
            return(license_status, dep_in_db)
        else:
            license_found = "Dependency Not found, please check manually"
            license_status = -1
            return(license_status, license_found)


# spec: receives repo as github object and language as a string, finds files with dependencies and creates a dict of all detected dependency files
# returns dict of dependency files
def get_dependency_files_from_repo(repository, language):
    if language == 'python':
        dependency_files = []  # this will be the array of dependencies found 
        contents = repository.get_contents("")  # END of loop to search through all repo contents for dependency files
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repository.get_contents(file_content.path))  # if we find a 
            else:
                if file_content.name in ["requirements.txt","requirements.in","Pipfile.lock"]:  # these are the files we are looking for (this should be pulled up from database)
                    dependency_files.append(file_content)  # END of loop to search through all repo contents for dependency files
    return(dependency_files)


# spec: receives a repository, dict of files and a language as a string, parses the files and extracts the dependencies
# returns dict of dependencies
def get_dependencies_from_dep_files(repository, dependency_files, language):
    if language == 'python':
        dependency_list = []
        for dep in dependency_files:
            if dep.path == "Pipfile.lock":
                pipline = []
                dep_contents = repository.get_contents(dep.path)
                requirements_string = dep_contents.decoded_content.decode().splitlines()
                for line in requirements_string:
                    if line.endswith(": {"):
                        content_line = line.split(sep='"', maxsplit=2)[1].strip()
                        pipline.append(content_line)
                        default = "default"
                        develop = "develop"
                        meta = "_meta"
                        hash = "hash"
                        for p in pipline:
                            if not str(p) == default and not str(p) ==  develop and not str(p) ==  meta and not str(p) ==  hash:
                                dependency_list.append(p)
            if dep.path == "requirements.txt" or dep.path == "requirements.in":
                strings_to_replace = ['>=','>','<=','<','~=']
                dep_contents = repository.get_contents(dep.path) 
                requirements_string = dep_contents.decoded_content.decode().splitlines()
                for line in requirements_string:
                    for string in strings_to_replace:
                        line = line.replace(string, '==')
                    content_line = line.split(sep='==', maxsplit=1)[0].strip()
                    if not content_line.startswith('#') and len(content_line)>1:
                        dependency_list.append(content_line)
    return(dependency_list) 
            # dep_contents = repository.get_contents(dep.path)
            # requirements_string = dep_contents.decoded_content.decode().splitlines()
            # for line in requirements_string:
            #     for string in strings_to_replace:
            #         line = line.replace(string, '==')
            #     content_line = line.split(sep='==', maxsplit=1)[0].strip()
            #     if not content_line.startswith('#') and len(content_line)>1:
            #         dependency_list.append(content_line)
    # return(dependency_list)


# spec: receives a repository, dict of dependencies and a language as a string, invokes lookup on the license and stores the pair for repo/dependency
# returns status
def scan_repo_dependencies(repository, dependency_list, language):
    for dep in dependency_list:
        status, dependency_in_db = lookup_dep_license(dep, language)
        if status == 0:
            try:
                pair = Repo_Dependency_Pair.objects.get(repo=repository, dependency=dependency_in_db)
            except ObjectDoesNotExist:
                save_repo_dep_pair(repository, dependency_in_db)
    
