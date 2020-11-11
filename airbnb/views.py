from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from bs4 import BeautifulSoup
import requests

class AirbnbList(APIView):
    def post(self, request):
        param = request.data
        area = param["area"] 
        checkin = param["checkin"] if param["checkin"] else "2020-11-16"
        checkout = param["checkout"] if param["checkout"] else "2020-11-21"
        adults = param["adults"] if param["adults"] else "1"
        children = param["children"] if param["children"] else None
        infants = param["infants"] if param["infants"] else None

        url = f'https://www.airbnb.co.kr/s/{area}/homes' \
            f'?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes'\
            f'&checkin={checkin}'\
            f'&checkout={checkout}'
        url += f'&adults={adults}' if adults else ''
        url += f'&children={children}' if children else ''
        url += f'&infants={infants}' if infants else ''

        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        html.close()

        airbnb_list=soup.findAll('div',{'class':'_1048zci'})

        data = []
        for i in airbnb_list:
            img = i.find('img')["src"]
            location = i.find('div', {'class':'_167qordg'}).text
            name = i.find('div', {'class': '_bzh5lkq'}).text
            information = i.find('div', {'class': '_kqh46o'}).text
            states = i.find('div', {'class': '_kqh46o'}).text
            price = i.find('span', {'class': '_1p7iugi'})
            try:
                star = i.find('span', {'class': "_18khxk1"}).find('span', {'class': '_10fy1f8'}).text
            except:
                star = ""
            try:
                discount = price.find('span', {'class': '_16shi2n'}).text
                onprice = price.text.replace(discount,'')
            except:
                discount = ""
                onprice = price.text

            totalprice = i.find('button', {'class': '_ebe4pze'}).text[:-8]
            data.append({"location":location,
                    "information":information,
                    "states":states,
                    "img":img,
                    "name":name,
                    "discount":discount,
                    "onprice":onprice,
                    "totalprice":totalprice,
                        "star":star})

        queryset = {"data":data}
        return Response(queryset)
