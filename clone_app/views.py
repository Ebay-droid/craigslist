import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models

BASE_URL = 'https://newyork.craigslist.org/d/for-sale/search/sss?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
  return render(request,'base.html')


def new_search(request):
  search = request.POST.get('search')
  models.Search.objects.create(search=search)
  final_url = BASE_URL.format(quote_plus(search))
  
  response = requests.get(final_url)
  data = response.text
  # print (data)
  soup = BeautifulSoup(data, features='html.parser')
  post_listing = soup.find_all('li',{'class':'result-row'})
  final_listing =[]

  for post in post_listing:
    post_title = post.find('a',{'class':'result-title'}).text
    post_url = post.find('a',{'class':'result-title'})['href']
    if post.find('span',{'class':'result-price'}):
      post_price = post.find('span',{'class':'result-price'}).text
    else:
      post_price='N/A'  

    if post.find(class_='result-image').get('data-ids'):
      post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
      post_image_url = BASE_IMAGE_URL.format(post_image_id)

    else:
      post_image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSjfsQp6Ay4_F5w8cmeaAPielCQ_238MeXTKQ&usqp=CAU'  

    final_listing.append((post_title,post_url,post_price,post_image_url))
   
  stuff_for_frontend = {
    'search':search,
    'final_listing':final_listing,
  }
  return render(request,'my_app/new_search.html', stuff_for_frontend)  