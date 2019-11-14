from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse

import requests
from lxml.etree import HTML
import csv
import json

# from django.views.decorators.csrf import ensure_csrf_cookie


headers = {
    'accept': "*/*",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "no-cache,no-cache",
    'pragma': "no-cache",
    'referer': "https://www.imdb.com/title/tt4154796/reviews?ref_=tt_ql_3",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    'x-requested-with': "XMLHttpRequest",
    'Postman-Token': "6e1e722d-5ca3-4f9b-a185-b8eb2f83d0a6"
}



def crawlData(request):
    id = request.GET['id']
    model =  request.GET['model']
    rsult = crawl(id)
    rating_tb = 0
    return JsonResponse({'data' : rsult , 'total' : len(rsult), 'rating_tb': (rating_tb / len(rsult))})


# @ensure_csrf_cookie
def customData(request):
    datas = json.loads(request.body.decode('utf-8'))
    data = datas['data']
    model = datas['model']
    rating_tb = 0
    rsult= [{
        'rating' : -10,
        'content' : data,
        'id' : 1
    }]
    return JsonResponse({'data' : rsult , 'total' : len(rsult), 'rating_tb': (rating_tb / len(rsult))})


def getAllReview(key):
    url = 'https://www.imdb.com/title/{key}/reviews?ref_=tt_urv'.format(key = key)
    response = requests.get(url,headers=headers)
    html = HTML(response.text)
    rs = html.xpath('//*[@id="main"]/section/div[2]/div[1]/div/span//text()')
    text = rs[0].replace(',', '')
    arr_rs = [int(s) for s in text.split() if s.isdigit()]
    return arr_rs[0]


def crawl(id):

    all_cmt = getAllReview(id)
    rs = []
    i = 0
    while i < all_cmt:
        count = 0
        if i == 0:
            url = 'https://www.imdb.com/title/{key}/reviews/_ajax'.format(key=id)
        else:
            url = 'https://www.imdb.com/title/{key}/reviews/_ajax?ref_=undefined&paginationKey={pageToken}'.format(pageToken=pageToken,key=id)

        response = requests.get(url,headers=headers)
        html = HTML(response.text)

        pageToken = html.xpath('string(//div[@class="load-more-data"]/@data-key)')

        div_list = html.xpath('//div[@class="lister-list"]/div')
        for div in div_list:
            rating = div.xpath('string(.//span[@class="rating-other-user-rating"]/span[1])')
            commentList  = div.xpath('.//div[@class="text show-more__control"]//text()')
            
            el = {
                'rating' : rating,
                'content' :''.join(commentList),
                'id' : i + count +1
            }
            count = count + 1
            if i + count > all_cmt:
                break 
            else:
                rs.append(el)
        i = i + count
    print(len(rs))
    return rs

            