# -*- coding: utf-8 -*-
import json
import time

import requests

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    "referer": "https://passport.tujia.com/PortalSite/LoginPage/?originUrl=https%3A%2F%2Fwww.tujia.com%2F"
}



def get_token():
    url = "https://passport.tujia.com/feapi/passportapi/captcha/applyImgCode"
    headers.update({"content-type": "application/json;charset=UTF-8"})
    now_time = time.time()
    querystring = {
        '_apitsp': '%s672'.format(now_time),
        '_fasTraceId': '%s673BhH4Xk3S_9ibDmJ34K0jTNhZE3izbt5GjDZjb'.format(now_time)
    }

    payload = json.dumps(
        {"parameter":
            {
                "bizCode": 24
            }
        }
    )

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False)
    res = response.json()
    print('get_token', response.text)
    if res.get('errcode') == 0:
        return res['data']
    return 0


def initialize(data):
    url = 'https://cf.aliyun.com/nocaptcha/initialize.jsonp'

    querystring = {
        'a': data['appkey'],
        't': data['token'],
        'scene': data['scene'],
        'lang': 'cn',
        'v': 'v1.2.17',
        'href': 'https://passport.tujia.com/PortalSite/LoginPage/',
        'comm': {},
        'callback': 'initializeJsonp_01364215067305965'
    }
    respone = requests.request('GET', url, headers=headers, params=querystring, verify=False)
    print(respone.text)


def analyze(data, verify_msg):
    url = "https://cf.aliyun.com/nocaptcha/analyze.jsonp"
    querystring = {
        'a': data['appkey'],
        't': data['token'],
        'n': verify_msg,
        'p': json.dumps({
          "key": "code0",
          "ncSessionID": "5e70053efef8",
          "umidToken": "T67663A2AD52DCFF6985779CB163130B899CD2845F20B730DFF82D40063"
        }),
        'scene': 'nc_register',
        'asyn': 0,
        'lang': 'cn',
        'v': 1000,
        'callback': 'jsonp_08050064196730045'
    }

    resp = requests.get(url, pamars=querystring, headers=headers, verify=False)
    result = json.loads(resp.text.replace('jsonp_08050064196730045(', '').replace(')', ''))



def ynuf(data):
    url = "https://ynuf.aliapp.org/service/um.json"
    headers.update({'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'})
    querystring = {
        "_fasTraceId": "%s097EGkMwRKt_9ibDmJ34K0jTNhZE3izbt5GjDZjb".format(time.time())
    }
    payload = {
            'data': "106!E5hmc0clZZEHORoIjmTPz83e2DuE5AkD0tdQZ8UUzEH0nc6rU2umzXczUWaJPhAmnlmYZiUJdOKVfNQ5ij5XA3YhWWbABDG+mlI4NBIq15dAewsLVFQcwB+bNltJfdKpA1KxPWCQUASEIsBL4Sr31XazPN/fwLzkGZjXF92EXZWL8Ch1URFssTNlOn0Ugv4oPsK52ecUJswDfOkw22UukyjsOLTUiaswSy+qEDAUE0iW6uXPZFUU6ucU6oxM6gUjqEEcd+Mj4uDj6qXw/Raj6u85mt21yS7lsjxEsLU6H9GpvqlqwEgzLVH07SIw6e0qwUMROZiLO5Ij6TEs1jXJfcO2J5+ylIfselZfTjosQZ5ayPmOHIm+06KSLo99oxQJ97iaWCWOXGmF8+8nJ5PXCVdagWNrz+eCu7VnyoL/Gl7jQ5qutajR/xIcYJGRlr1P4uouYqWlxCoM3OLQUaF6v4d3MvWv36OJhS71RTOzr+QU526lTa8PkUPpn2aCcTbR3llSYGrgjDMvPafZgUp8JlOp1vT38uu3xOwYk8xxb1F68aS9fp6BmQGxFWv/i34tqBeL2cj7BHIIvYaIHGaSeXI2bRDneTHTuOL6yCpDcsnCdVaYgKQpGckktyp+KPPj4f1uUfSFnvAUVyKJcdi9GjBVFwiqYdWfTyRyO7MPsdC9CPd3dJOYo4JvJ++vR0baISSzNPN9yeYQ8YDPdjnaJIp+kOzWOdhabKZmvKjiHeHWdm==",
            'xa': data['appkey'],
            'xt': None,
            'efy': 1
        }

    respone = requests.request('POST', url, headers=headers, params=querystring, data=payload, verify=False)
    print(respone.text)


def crack():
    data = get_token()
    if data:
        initialize(data)



if __name__ == '__main__':
    crack()