# -*- coding: utf-8 -*-

import requests
import time
import json
import execjs
import random
import hashlib

"""
加密参数说明:
    1、verify_msg: 滑动轨迹等信息参数加密
    2、dimensions: 运行环境等信息参数加密
    3、extend_param: 屏幕信息参数加密, 可按自己电脑信息写死
    4、对接口所有参数按指定顺序排序后的字符串进行md5加密校验
"""

headers = {
    'referer': 'https://ebooking.ctrip.com/ebkovsassembly/Login',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

# 接口通用参数
params = {
    # 'callback': 'captcha06615687560558079',
    'callback': 'captcha05245505977574092',
    # 滑块使用接口标识, 如登录时需要滑块验证, 则为: crm_login_online, 手机号查询订单: crm_getorder_online, 按自己需求替换
    'appid': '100012428',
    'business_site': 'ebk_login_online',
    'version': '2.5.33'
}


def _generate_trace():
    """
    生成轨迹
    :return:
    """
    distance = random.randint(280, 290)
    # zx = random.randint(330, 340)
    zx = random.randint(240, 250)
    # zy = random.randint(240, 250)
    zy = random.randint(170, 180)
    # 初速度
    v = 0
    # 位移/轨迹列表，列表内的一个元素代表0.02s的位移
    tracks_list = []
    # 当前的位移
    current = 0
    while current < distance - 13:
        # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
        a = random.randint(10000, 12000)  # 加速运动
        # 初速度
        v0 = v
        t = random.randint(9, 18)
        s = v0 * t / 1000 + 0.5 * a * ((t / 1000) ** 2)
        # 当前的位置
        current += s
        # 速度已经达到v,该速度作为下次的初速度
        v = v0 + a * t / 1000
        # 添加到轨迹列表
        if current < distance:
            tracks_list.append(round(current))
    # 减速慢慢滑
    if round(current) < distance:
        for i in range(round(current) + 1, distance + 1):
            tracks_list.append(i)
    else:
        for i in range(tracks_list[-1] + 1, distance + 1):
            tracks_list.append(i)
    y_list = []
    for j in range(len(tracks_list)):
        y = random.choice(
            [0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
             -1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, -1, 0, 0])
        y_list.append(y)
        j += 1
    trace = []
    for index, x in enumerate(tracks_list):
        trace.append({
            'x': zx + x,
            'y': zy + y_list[index]
        })
    print(trace)
   #  trace = [
   #    {'x': 248, 'y': 171},
   #  {'x': 250, 'y': 172},
   #  {'x': 256, 'y': 174},
   #  {'x': 264, 'y': 174},
   #  {'x': 276, 'y': 177},
   #  {'x': 295, 'y': 178},
   #  {'x': 309, 'y': 178},
   #  {'x': 332, 'y': 182},
   #  {'x': 357, 'y': 183},
   #  {'x': 389, 'y': 188},
   #  {'x': 416, 'y': 188},
   #  {'x': 441, 'y': 188},
   #  {'x': 468, 'y': 188},
   #  {'x': 490, 'y': 190},
   #  {'x': 512, 'y': 190},
   # {'x': 532, 'y': 191}
   #  ]
    return trace


def get_token():
    """
    获取页面 token 认证
    :return:
    """
    url = "https://m.ctrip.com/restapi/soa2/11470/getToken.json?t={}&callback=$_bf_uniq_F1".format(
        int(time.time() * 1000))
    resp = requests.get(url, headers=headers, verify=False)
    result = json.loads(resp.text.replace('$_bf_uniq_F1(', '').replace(')', ''))
    token = result['data']['token']
    return token


def get_sfp(token):
    """
    加密 token 生成 sfp 参数
    :param token:
    :return:
    """
    with open('get_sfp.js', 'rb') as f:
        fjs = f.read().decode()
    fctx = execjs.compile(fjs)
    sfp = fctx.call('get_sfp', token)
    return sfp


def init_encrypt(sfp):
    """
    滑块初始化接口加密
    :param sfp:
    :return:
    """
    with open('../xc_slider.js', 'rb') as f:
        js = f.read().decode()
    ctx = execjs.compile(js)
    data = ctx.call('init_encrypt', sfp)
    return data


def verify_encrypt(verify_msg, dimensions):
    """
    滑块验证接口加密
    :param verify_msg:
    :param dimensions:
    :return:
    """
    with open('../xc_slider.js', 'rb') as f:
        js = f.read().decode()
    ctx = execjs.compile(js)
    return ctx.call('verify_encrypt', verify_msg, dimensions)


def process_param(trace, pass_time, start_time):
    """
    轨迹等信息参数处理
    :param trace:
    :param pass_time: 滑动总时间
    :param start_time: 开始时间
    :return:
    """
    """
    st: 1585811521482
slidingTime: 276
display: "1920x1080"
keykoardTrack: []
slidingTrack: (27) [{…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}]
timezone: -480
flashState: false
language: "zh-CN"
platform: "Win32"
cpuClass: undefined
hasSessStorage: true
hasLocalStorage: true
hasIndexedDB: true
hasDataBase: true
doNotTrack: false
touchSupport: false
mediaStreamTrack: true

0: {x: 248, y: 171}
1: {x: 250, y: 172}
2: {x: 256, y: 174}
3: {x: 264, y: 174}
4: {x: 276, y: 177}
5: {x: 295, y: 178}
6: {x: 309, y: 178}
7: {x: 332, y: 182}
8: {x: 357, y: 183}
9: {x: 389, y: 188}
10: {x: 416, y: 188}
11: {x: 441, y: 188}
12: {x: 468, y: 188}
13: {x: 490, y: 190}
14: {x: 512, y: 190}
15: {x: 532, y: 191}

284

Array(27)
0: {x: 250, y: 177}     
1: {x: 251, y: 177}
2: {x: 259, y: 177}
3: {x: 269, y: 177}
4: {x: 283, y: 174}
5: {x: 300, y: 172}
6: {x: 318, y: 169}
7: {x: 339, y: 165}
8: {x: 359, y: 164}
9: {x: 376, y: 163}
10: {x: 390, y: 163}
11: {x: 404, y: 163}
12: {x: 417, y: 163}
13: {x: 428, y: 163}
14: {x: 441, y: 163}
15: {x: 451, y: 163}
16: {x: 459, y: 163}
17: {x: 467, y: 163}
18: {x: 473, y: 163}
19: {x: 478, y: 163}
20: {x: 485, y: 163}
21: {x: 492, y: 163}
22: {x: 500, y: 163}
23: {x: 508, y: 163}
24: {x: 517, y: 163}
25: {x: 526, y: 163}
26: {x: 533, y: 163}
"""
    M = {
        'st': start_time,
        'slidingTime': pass_time,
        # 'display': "1366x768",
        'display': "1920x1080",
        'keykoardTrack': [],
        'slidingTrack': trace,
        'timezone': -480,
        'flashState': 'false',
        'language': "zh-CN",
        'platform': "Win32",
        'cpuClass': 'undefined',
        'hasSessStorage': 'true',
        'hasLocalStorage': 'true',
        'hasIndexedDB': 'true',
        'hasDataBase': 'true',
        'doNotTrack': 'false',
        'touchSupport': 'false',
        'mediaStreamTrack': 'true'
    }
    x = json.dumps(M)
    x = x.replace('"undefined"', 'undefined')
    x = x.replace('"true"', 'true')
    x = x.replace('"false"', 'false')
    x = x.replace(' ', '')
    return x


def md5_encrypt(verify_msg, dimensions, extend_param):
    """
    md5 加密 sign 参数
    :param verify_msg:
    :param dimensions:
    :return:
    """
    # "b2bfedd7904a33b2b46a9f8d0fb2e3e8"

    md5 = hashlib.md5()
    text = "appid=100012428&business_site={}&version=2.5.33&verify_msg="\
               .format(params['business_site']) + verify_msg + "&dimensions=" + dimensions + "&extend_param=" + extend_param
               # .format(params['business_site']) + verify_msg + "&dimensions=" + dimensions + "&extend_param=iSGlZQho4OSS/KGB9EdMa9l56eWLMf22JI42bFItXwdAD1fueskfM5oFJ90ou9GbTTF/G6OrnXQh/4KUcGd1fIbmifFEMCs685+juuDT4jc1/lnYrJ7NTlvcgm0bvZx6X8QLeh9ItOdcaQO/hqll1DsjJRx2IHBbYd2OGycXpAmO7oqBhsjk9jruUv9uP2ll"
               # .format(params['business_site']) + verify_msg + "&dimensions=" + dimensions + "&extend_param=iSGlZQho4OSS/KGB9EdMa9l56eWLMf22JI42bFItXwdAD1fueskfM5oFJ90ou9GbTTF/G6OrnXQh/4KUcGd1fIbmifFEMCs685+juuDT4jc1/lnYrJ7NTlvcgm0bvZx6X8QLeh9ItOdcaQO/hqll1DsjJRx2IHBbYd2OGycXpAmO7oqBhsjk9jruUv9uP2ll"
    md5.update(text.encode())
    return md5.hexdigest()


def get_verify_msg(data):
    """
    轨迹加密
    :param data:
    :return:
    """
    with open('../../../../../../Downloads/xc_slider.js', 'rb') as f:
        js = f.read().decode()
    ctx = execjs.compile(js)
    verify_msg = ctx.call('get_verify_msg', data)
    return verify_msg


def _init_slider(data):
    """
    滑块初始化
    :param data:
    :return:
    """
    # "https://ebooking.ctrip.com/captcha/risk_inspect?callback=captcha05245505977574092&extend_param=2V6x7pDkvcrysIz84iab1mkrIPLIDVRU%2BBPiPIEj9UR0sLdhXm%2BUhGjQbfw7Iu1cQtzz3xOQmga3JZpBIrgg0U5VJbM2oYmsTbu5DnNprEE%3D&appid=100012428&business_site=ebk_login_online&version=2.5.33&dimensions=GMLapjsYAM0mi9yIxCrPmkTNxfIMbNDfQ2sKnIihQxyojiCfQi85bnAiy%2FVH8SfW5zUDz6GUOhyretNfKw2ljS6JOm66EiZrm3vp3Jl0jOwBakvF3sp0Akg2uFN5RgguD8oWS1M9StJ7T8j%2BjiywM3LW772qzOYA5exxk4lUcCiiFdQIbT%2F63xywxYul9ra2I%2FzFXFCrGMGUl%2F16%2F5vU5GIZ2aOSYygQ%2Bd7iQvx%2BBYn3SWVQErUkwrJYNypzl4ybxPQitV6JmUZOMcBsxYl%2BsoPfX1bEFSZDEDAGXQtfFSPWHrNKXY5VtjP4y1%2Bf%2FpfrZsRoTg4kZY6bpqQEOZJFxFZd%2FcQuhWv3PCOBPaieD%2Fem8%2BlFmYjH%2BKpSIkcH7zA0W0Y59TGiDpcypRILC8HYZ%2BpAJfNiM61%2BXoDbtEwL3n3kQGa9hsPpQ5mAI1YAE4aUKmGqXOmCjsLfkf7budJihI%2BlSR7s7NrcbR3yeAg9MmTgDomNT%2FOP6GChuR03LkPy9Xl4D86ka4CKv7akcdU6bXD%2BQuD9ru3KxsoGhfKVL7B2wcspak3HMcAcJVZnvAryhpRgUDhRxv9%2BHTWjKf3qF%2F%2FpAxtK%2FPYq5DlIIcmxTPMpNlZUzSsRHEFmEwLwFMIHPoLhx1NWHGrDFHF9QAaJbIxPNEzEd4kjYsC2qB6bSaYPp1vXSEFmdZzjnArNoT337YbyHTqUOirb9kRIvIRnH7KMhX6dfqlthfxf0Cjnk2qx%2FrW6P37F56LJXJyFBetgB2yg7MtDi6sFQfveq6Em5pooOkTvUASmOPiWB37JjtWwESSl3FLmpIoMuyOxqICvSDfd%2FSvF3BC3D7ESD06ImGeraWhYPpxORrluX7rrNTXX3sILvMxbYQ5YeFfjJoYV8pUs4GscPptZ5UyMTRl5fqyJxONF7Yi3O48%2BdzAgnkrbksNEsY6nxiOUq9Mz5%2BVMv9O48HMHSYXaGdlS3S8%2FiTRA0YAMWDotj6nte0qOfOr6lZiDmQNAdK1snOBI2krDoYnF3KBqEDbdy9JKxx2sDTswl5sNla%2FGJXXknhpcyTZaJFAYutQggZoMx8KE85r6Et%2BGYc7fp0gJ%2BMAaM9l0oxNt%2FvRSA4LD9CgbqvRMb4LeESsyGMD5s%2BljhiGynIW%2BEc1WJRcdlm499vDK%2BZTYZf3FCvuaA7W0QshIkyTKeaUydic1Ob0KFNOBolDWJBqfYSqT263iFn9qlGbwrsq6W9xXdD7J087z6grjXDbctf%2Fhj7VIfDfr3%2FTIdsQM8aVXRGNrCf2q1aPHshZFbSMFCSLiDquPOp9X5pGIrOMpyGgO6JryqoXk5I3JOZF2v%2F40KjjvkQ5szFFlrMNGVW8ttIcuJsNuffCII1VATfK2e%2FDD0irMqr3kpXMCAABQk%2FOL&sign=efb612c865ada93f27dc25f509c80335"
    url = 'https://ebooking.ctrip.com/captcha/risk_inspect'
    params.update(data)
    resp = requests.get(url, params=params, headers=headers, verify=False)
    # result = json.loads(resp.text.replace('captcha029311869916299216(', '').replace(')', ''))
    # result = json.loads(resp.text.replace('captcha06615687560558079(', '').replace(')', ''))
    result = json.loads(resp.text.replace('captcha05245505977574092(', '').replace(')', ''))
    if result['message'] == 'Success':
        print('滑块初始化成功! ')
        return result['result']['rid']
    return None


def _slider_verify(rid, verify_msg, dimensions, sign, extend_param):
    """
    滑块验证
    :param rid: 滑块标识
    :param verify_msg: 轨迹等信息加密参数
    :param dimensions: 环境加密参数
    :param sign: md5 校验签名
    :return:
    """
    url = "https://ebooking.ctrip.com/captcha/verify_slider"

    params.update({
        'rid': rid,
        'verify_msg': verify_msg,
        'dimensions': dimensions,
        # 'extend_param': 'iSGlZQho4OSS/KGB9EdMa9l56eWLMf22JI42bFItXwdAD1fueskfM5oFJ90ou9GbTTF/G6OrnXQh/4KUcGd1fIbmifFEMCs685+juuDT4jc1/lnYrJ7NTlvcgm0bvZx6X8QLeh9ItOdcaQO/hqll1DsjJRx2IHBbYd2OGycXpAmO7oqBhsjk9jruUv9uP2ll',
        'extend_param': extend_param,
        'sign': sign,
    })
    print("params", params)
    resp = requests.get(url, params=params, headers=headers, verify=False)
    result = json.loads(resp.text.replace('captcha05245505977574092(', '').replace(')', ''))
    print(result)
    if result['message'] == 'Success':
        if result['result']['risk_info']['risk_level'] == 0:
            return {
                'success': 1,
                'message': '校验通过! ',
                'data': {
                    'token': result['result']['token']
                }
            }
        return {
            'success': 1,
            'message': '需要进一步点选验证! ',
            'data': None
        }
    return {
        'success': 0,
        'message': '校验失败! ',
        'data': None
    }


def crack():
    token = get_token()
    sfp = get_sfp(token)
    data = init_encrypt(sfp)
    time.sleep(random.uniform(0.1, 0.5))
    start_time = int(time.time() * 1000)
    dimensions = data['dimensions']
    rid = _init_slider(data)
    trace = _generate_trace()
    pass_time = int(time.time() * 1000) - start_time
    y_data = process_param(trace, pass_time, start_time)
    verify_msg = get_verify_msg(y_data)
    sign = md5_encrypt(verify_msg, dimensions, data['extend_param'])
    result = _slider_verify(rid, verify_msg, dimensions, sign, data['extend_param'])
    return result


if __name__ == '__main__':
    x = crack()
    print(x)

