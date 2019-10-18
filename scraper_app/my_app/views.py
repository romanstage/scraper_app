import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from .import models

BASE_AVITO_URL = 'https://www.avito.ru/moskva?q={}'


# Create your views here.
def home(request):
    return render(request, 'base.html')



def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_AVITO_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('div', {'class': 'item'})

    final_postings = []

    if post_listings:
        for post in post_listings:
            #PRICE
            try:
                post_title = post.find('div', {'class': 'description'}).find('h3').text.strip()
            except:
                post_title = ''

            #URL
            try:
                post_url = 'https://www.avito.ru' + post.find('div', {'class': 'description'}).find('a').get('href')
            except:
                post_url = ''

            # PRICE
            try:
                post_price = post.find('div', {'class': 'about'}).text.strip()
            except:
                post_price = 'НЕ УКАЗАНА'

            # IMAGE
            try:
                post_image_url = post.find('div', {'class': 'item-slider-image'}).find('img').get('src')
            except:
                post_image_url = 'http://www.tourniagara.com/wp-content/uploads/2014/10/default-img.gif'


            final_postings.append((post_title, post_url, post_price, post_image_url))


    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }


    return render (request, 'my_app/new_search.html',stuff_for_frontend)