from django.shortcuts import render, redirect
import json, requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import pdb

def login(request):
    return render(request, 'dashboard.html')

@csrf_exempt
def pages(request):
    print("here")
    if request.method == "POST":

        data = request.POST.get('access_token')
        
        pages = requests.get(("https://graph.facebook.com/me/accounts") , params = {"access_token" : data }).json()['data']
        page_list = []
        for page in pages:
            p = {
                'id'            : page['id'],
                'name'          : page['name'],
                'category'      : page['category'],
                'access_token'  : page['access_token'],
            }
            page_list.append(p)

        return render(request, "pages.html",context={'pages':page_list})
    return render(request,"pages.html")

@csrf_exempt
def edit(request, id, token=None):
    fields=["id","category","name","phone","impressum","general_info","about","attire","bio","location","parking","hours","emails","website","description","company_overview","personal_info","access_token"]
    fieldstring=','.join(fields)

    if request.method == "POST" or token:
        if token:
            token = token
        else:
            token = request.POST.get("token")
        page_detail = requests.get(("https://graph.facebook.com/"+str(id)+"?") , params = {"fields": fieldstring, "access_token" : token }).json()
        return render(request, 'page_edit.html', context = {'page':page_detail})
    return render(request, 'pages.html')

@csrf_exempt
def update(request, id):
    
    token = request.POST.get("token")
    emails = []
    emails.append(request.POST.get("email"))
    print(emails)
    Data = {}
    Data['access_token'] = token
    Data['about'] = request.POST.get('about')
    Data['phone'] = request.POST.get('phone')
    Data['description'] = request.POST.get('description')
    Data['website'] = request.POST.get("website")
    Data['impressum'] = request.POST.get('impressum')
    Data['company_overview'] = request.POST.get("overview")
    Data['page_id'] = request.POST.get("page_id")
    Data['emails'] = emails
    
    response = requests.post(("https://graph.facebook.com/"+str(id)), json=Data).json()
    return edit(request, Data['page_id'], token)