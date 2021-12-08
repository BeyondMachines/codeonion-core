from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, HttpResponseRedirect
import requests  # the http requests framework
from zappa.asynchronous import task, get_async_response  # the async communication framework in zappa
from django.http import JsonResponse  # to create
from django.urls import reverse_lazy  # reverse url for redirect to internal url view
from github import Github, GithubException  # the objects needed
from urllib.parse import urlparse  # this is needed for domain parsing
from time import sleep
import json
import boto3
import os
import botocore

# Import models

from main.models import Message 
from scanner.models import Repo_Dependency_Pair

# Import views

from scanner.views import open_github_repo, check_valid_repo_url, scan_github_repo, check_repo_in_db, generate_uuid, save_repo
from reporter.views import get_repo_dependencies_from_db

# Create your views here.

def get_local_ssm_key(name):
    ssm = boto3.client('ssm')
    try:
        key = ssm.get_parameter(Name=name, WithDecryption=True)
        return key['Parameter']['Value']
    except botocore.exceptions.ClientError as error:
        return error


# def home_view(request, *args, **kwargs):
#     scope_message =  get_local_ssm_key("CODEFOX_TEST_POSTGRES_USER"),
#     context = {
#         'scope_message': scope_message,
#     }
#     return render(request, "home/home.html", context)


def home_view(request, *args, **kwargs):
    scope_message = Message.objects.get(message_title="scope_message").message_text
    url_instructons_message = Message.objects.get(message_title="url_instructons_message").message_text
    repo_scan_completed = False
    repo_scan_started = False
    scan_response_id = None
    repo_connection = None
    repo_uuid = None
    repo_name = None
    validRepo = False
    request_url = None

    # generate_uuid() # this is commented, should be used only once to generate the initial uuids in the migrations process for the testing.

    if request.method == 'POST':
        # web_site = 'https://'+str(request.POST.get('website'))  # this was the first prototype for zappa async. Keeping it here for reference
        request_url = request.POST.get('repository')
        
        repo_name = request_url.split(sep='/')[-1].strip()

        # async_call_id = open_site(web_site) # this was the first prototype for zappa async. Keeping it here for reference
        valid_repo, repo_type, repo_path = check_valid_repo_url(request_url)
        if valid_repo:
            validRepo = True
            try:
                repo_connection = open_github_repo(repo_path)
                
            except Exception as error:
                url_instructons_message = error
            if repo_connection:
                
                repo_in_db, repo_exists, older = check_repo_in_db(repo_connection)
                # print('check_repo_in_db', repo_in_db, repo_exists, older)
                if repo_exists and not older:
                    # print('if repo exists and not older', repo_in_db, repo_exists, older)
                    repo_scan_started = True
                    repo_scan_completed = True
                    repo_uuid = repo_in_db.repo_id
                    print('repo_uuid', repo_uuid)
                elif repo_exists and older:
                    # print('if repo exists and older', repo_in_db, repo_exists, older)
                    repo_uuid = repo_in_db.repo_id
                    # print('repo_uuid', repo_uuid)
                    repo_scan_started = True
                    scan_response = scan_github_repo(repo_path)
                    if os.environ.get('AWS_REGION'):
                        scan_response_id = scan_response.response_id
                        repo_scan_completed = False
                    else:
                        scan_response_id = scan_response
                        # repo_scan_completed = True
                        repo_scan_completed = False

                else:
                    # print('if repo NOT exists', repo_in_db, repo_exists, older)
                    repo_in_db = save_repo(repo_connection,'github','python')
                    repo_uuid = repo_in_db.repo_id
                    # print('repo_uuid', repo_uuid)
                    repo_scan_started = True
                    scan_response = scan_github_repo(repo_path)
                    if os.environ.get('AWS_REGION'):
                        scan_response_id = scan_response.response_id
                        repo_scan_completed = False
                    else:
                        scan_response_id = scan_response
                        # repo_scan_completed = True
                        repo_scan_completed = False

        else:
            url_instructons_message = 'You didn\'t enter a GitHub URL. The URL you entered is: ' + request_url
            validRepo = False
        
        # START this was the first prototype for zappa async. Keeping it here for reference
        # try:
        #     response_id = async_call_id.response_id
        # except:
        #     response_id = async_call_id
        # END this was the first prototype for zappa async. Keeping it here for reference

    context = {
        'url': request_url,
        'validRepo' : validRepo,
        'repo_name':repo_name,
        'url_instructons_message': url_instructons_message,
        'scope_message': scope_message,
        'repo_scan_completed': repo_scan_completed,
        'repo_scan_started': repo_scan_started,
        'scan_response_id': scan_response_id,
        'repo_uuid': repo_uuid

    }
    return render(request, "home/home.html", context)


# START this was the first prototype for zappa async. Keeping it here for reference
# @task(capture_response=True)
# def open_site(site):
#     try:
#         request_site = requests.get(site)
#         request_response = request_site.status_code
#     except (requests.ConnectionError, requests.Timeout) as error:
#         print(str(error))
#         request_response = 'error'
#     return request_response
# END this was the first prototype for zappa async. Keeping it here for reference



# def check_dependencies(g, repo_name):
#     deps = []
#     dependency_dict = []
#     dep_dict = []
#     dev_dep_dict = []
#     try:
#         test_repo = g.get_repo("VATBox/" + repo_name)
#     except:
#         print("check_dependencies", repo_name, "not found")
#     if test_repo.   :
#         if test_repo.language.lower() in ['javascript','typescript']:
#             try:
#                 contents = test_repo.get_contents("package.json")
#             except:
#                 print("JS/TS repo",test_repo.full_name,"doesn't have package.json")
#                 return(deps)
#             dependency_dict = json.loads(contents.decoded_content.decode())
#             try:
#                 dep_dict =  dependency_dict["dependencies"]
#             except:
#                 dep_dict = []
#             try:
#                 dev_dep_dict =  dependency_dict["devDependencies"]
#             except:
#                 dev_dep_dict = []
#             if dep_dict:
#                 for i in dep_dict:
#                     license = get_dep_license(i, 'js')
#                     deps.append([repo_name, "JS/TS", i, license, "Production Dependency"])
#             if dev_dep_dict:
#                 for j in dev_dep_dict:
#                     license = get_dep_license(j, 'js')
#                     deps.append([repo_name, "JS/TS", j, license, "Dev Dependency"])
#         elif test_repo.language.lower() in ['python']:
#             try:
#                 contents = test_repo.get_contents("requirements.txt")
#             except:
#                 print("Python repo",test_repo.full_name,"doesn't have requirements.txt")
#                 return(deps)
#             requirements_string = contents.decoded_content.decode().splitlines()
#             for line in requirements_string:
#                 dependency_dict.append(line.split(sep='==', maxsplit=1)[0])
#             for i in dependency_dict:
#                 license = get_dep_license(i, 'py')
#                 deps.append([repo_name, "Python", i, license, "Production Dependency"])

#     return(deps)
