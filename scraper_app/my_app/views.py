import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from .import models


def home(request):
    return render(request, 'base.html')


def get_html(url):
    r = requests.get(url)
    return r.text


def get_page_data(html):
    soup = BeautifulSoup(html, features='html.parser')
    post_listings = soup.find_all('div', {'class': 'item'})

    final_postings = []

    if post_listings:
        for post in post_listings:
            # PRICE
            try:
                post_title = post.find('div', {'class': 'description'}).find('h3').text.strip()
            except:
                post_title = ''

            # URL
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

    return final_postings

def get_total_pages(html):
    soup = BeautifulSoup(html, features='html.parser')

    pages = soup.find('div', {'class': 'pagination-pages'}).find_all('a', {'class': 'pagination-page'})[-1].get('href')
    total_pages = int(pages.split('=')[1].split('&')[0])
    print("total pages ",total_pages)
    return int(total_pages)

def new_search(request):
    BASE_AVITO_URL = 'https://www.avito.ru/rossiya?q={}'

    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    start_url = BASE_AVITO_URL.format(quote_plus(search))


    page_part = 'p='

    total_pages = get_total_pages(get_html(start_url))

    final_postings = []

    for i in range(total_pages):
        final_url = 'https://www.avito.ru/rossiya?' + page_part + str(i) + '&q=' + quote_plus(search)
        html = get_html(final_url)
        final_postings+=get_page_data(html)
    print(final_postings)

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }

    return render (request, 'my_app/new_search.html',stuff_for_frontend)