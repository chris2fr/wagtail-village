# from django.shortcuts import render
from django.http import HttpResponse
import datetime


# import requests
# import lesgv.services

# # Create your views here.
# def items(request):
#     #pull data from third party rest api
#     response = requests.get('https://jsonplaceholder.typicode.com/users')
#     #convert reponse data into json
#     items = response.json()
#     #print(users)
#     return render(request, "items.html", {'items': items})


# def posts(request):
#     return render(request, "lesgv/fait_ma_home_page_blog.html", {'posts': lesgv.services.get_blog_posts()})


def htmlmenu(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)