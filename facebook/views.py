from django.shortcuts import render, redirect
import json, requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def login(request):
    return render(request, 'dashboard.html')

@login_required
@csrf_exempt
def pages(request, access_token=None):
    if request.method == "POST" or access_token:
        try:
            data = request.POST.get('access_token')
        except:
            data = access_token
        
        pages = requests.get(("https://graph.facebook.com/me/accounts") , params = {"access_token" : data }).json()['data']
        page_list = []
        for page in pages:
            p = {
                'id'            : page['id'],
                'name'          : page['name'],
                'category'   : page['category'],
                'access_token'  : page['access_token'],
            }
            page_list.append(p)

        return render(request, "pages.html",context={'pages':page_list})
    return render(request,"pages.html")

@login_required
@csrf_exempt
def edit(request, id):
    fields=["category","name","phone","impressum","general_info","about","attire","bio","location","parking","hours","emails","website","description","company_overview","personal_info","access_token"]
    fieldstring=','.join(fields)

    if request.method == "POST":
        token = request.POST.get("token")
        page_detail = requests.get(("https://graph.facebook.com/"+str(id)+"?") , params = {"fields": fieldstring, "access_token" : token }).json()
        return render(request, 'page_edit.html', context = {'page':page_detail})
    return render(request, 'pages.html')

@login_required
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
    Data['emails'] = emails

    response = requests.post(("https://graph.facebook.com/"+str(id)), json=Data).json()
    print(response)
    
    return redirect('login')