from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, HttpResponseRedirect
import datetime
from django.core.exceptions import ObjectDoesNotExist
from zappa.asynchronous import task, get_async_response  # the async communication framework in zappa
import os
import random
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import datetime



# Create your views here.

from scanner.models import Scanned_Repo, Repo_Dependency_Pair, Dependency

from reporter.serializers import Repo_Dependency_Pair_Serializer, Dependency_Serializer


@csrf_exempt
def repo_dependencies_view(request, repo_id):
    if request.method == 'GET':
        older_than_90_days = datetime.datetime.now() - datetime.timedelta(90)
        # print(repo_id)
        try:
            repo_in_db = Scanned_Repo.objects.get(repo_id=repo_id)
            if repo_in_db.repo_last_checked_date > older_than_90_days.date():
                if repo_in_db and not repo_in_db.repo_scan_error:
                    dep_in_db = Dependency.objects.filter(dependency__repo=repo_in_db).values('dependency_name', 'dependency_language', 'dependency_license','dependency_license_last_checked_date')
                    serializer = Dependency_Serializer(dep_in_db, many=True)
                    return JsonResponse({ 'status': 'true', 'results': serializer.data}, safe=False)
                else:
                    return JsonResponse({ 'status': 'false', 'results': repo_in_db.repo_scan_error_message}, safe=False)
            else:
                message = {"error": "Results too old"}
                return JsonResponse(message, status=404)
        except Scanned_Repo.DoesNotExist as error:
            message = {"error": "Not Found"}
            return JsonResponse(message, status=404)
    else:
        message = {"error": "Bad Request"}
        return JsonResponse(message, status=405)

    """
    List all transformers, or create a new transformer
    """
    


def get_repo_dependencies_from_db(repo_in_db):
    dep_in_db = Repo_Dependency_Pair.objects.filter(repo=repo_in_db)
    return(dep_in_db)


@csrf_exempt
def scan_status_view(request, repo_id):
    # print(repo_id)
    if os.environ.get('AWS_REGION'): # Check whether AWS_REGION variable exists to see if running in AWS or locally
        response = get_async_response(repo_id)
        # print(response)
        if response is None:
            message = {"error": "Not Found"}
            return JsonResponse(message, status=404)
        elif response['status'] == 'complete':
            resp = response['status']
            return JsonResponse({ 'status': resp}, safe=False)
        else:
            # resp = 'incomplete'
            resp = response['status']
            return JsonResponse({ 'status': resp}, safe=False)
    else:
        response = 'complete'
        return JsonResponse({ 'status': response}, safe=False)

        # response = random.randint(1,101) 


    # if response['status'] == 'complete':

    # sleep(2)
    # return redirect('async_response', response_id=response_id)
    # return "Not yet ready. Redirecting.", 302, {
    #     'Content-Type': 'text/plain; charset=utf-8',
    #     'Location': url_for('async_response', response_id=response_id, backoff=5),
    #     'X-redirect-reason': "Not yet ready.",
    #}

@csrf_exempt
def repo_scan_status_view(request, repo_id):
    if request.method == 'GET':
        
            repo_in_db = Scanned_Repo.objects.get(repo_id=repo_id)
            
            if repo_in_db.repo_scan_status == 'none':
                return JsonResponse({ 'status': 'none'}, safe=False)
                
            elif repo_in_db.repo_scan_status == 'started':
                return JsonResponse({ 'status': 'started'}, safe=False) 

            elif repo_in_db.repo_scan_status == 'completed':
                return JsonResponse({ 'status': 'completed'}, safe=False)        
        
            else:
                return JsonResponse({ 'status': 'error'}, safe=False)

    else:
        message = {"error": "Bad Request"}
        return JsonResponse(message, status=405)            
