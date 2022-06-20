#  coding=utf-8

import re
import json

import requests
import pandas as pd


def request_data(page):
    cookies = {
        'cna': 'WcyfGgfwtx8CAWcbGHKt6foB',
        't': 'eaeb053e9e677e4e4fec253c05d74d03',
        'tracknick': '%5Cu7B49%5Cu5F85%5Cu7199%5Cu671B',
        'thw': 'cn',
        'sgcookie': 'E100QRhZtt3h3ouXylVvtWMEEirsegHWyZ2mI10L1sN4dAQJx0qmbkXHjMZkEIWiDT78y5FFA3xKxE0ntqI%2FzvWX%2B4PH8TqUQTsnenhPUY6IjpzI3bHFtPy9hBVWM5teRuM%2F',
        '_cc_': 'URm48syIZQ%3D%3D',
        'enc': 'sAUMsZDbdTSlTdCrcAW7eFA0y8DMTaW1SRPSkRXXWFpNspn25mtioyzNUoKpSkXyx3u6DvT2u%2BHuABpV1TR%2B4g%3D%3D',
        'uc1': 'cookie14=UoexMSpaOz2q1A%3D%3D',
        'cookie2': '1773c49ab2fa830ca1c287875e089720',
        '_tb_token_': 'efe587ae3f8de',
        'alitrackid': 'www.taobao.com',
        'lastalitrackid': 'www.taobao.com',
        'xlly_s': '1',
        'JSESSIONID': '3BE72A368B93E616359605CA39A9FE1D',
        'l': 'eBOHqmLeLNNmbWkNBO5w-urza77OzCOf1xNzaNbMiInca1PATgILxNChTl5J7dtjgtfAQetzHj297Rnk-_Udg2HvCbKrCyClkxJ6-',
        'tfstk': 'cxNRBFGbsijka_gY78B08uizloFRaFR-vUiw9WQEplIFoMRJNsb_s5KT-Tgtb0QA.',
        'isg': 'BGFhXzDHp76LOwtc7Yy83uHncC17DtUA0tFOzcMzDWmbKoL8C1-90O0sjF6skW04',
    }

    headers = {
        'authority': 's.taobao.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'script',
        'referer': 'https://s.taobao.com/search?q=%E8%8B%B9%E6%9E%9C%E6%89%8B%E6%9C%BA&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.jianhua.201856-taobao-item.2&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=1&ntoffset=1&p4ppushleft=2%2C48&s=44',
        'accept-language': 'zh-CN,zh;q=0.9',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'cna=WcyfGgfwtx8CAWcbGHKt6foB; t=eaeb053e9e677e4e4fec253c05d74d03; tracknick=%5Cu7B49%5Cu5F85%5Cu7199%5Cu671B; thw=cn; sgcookie=E100QRhZtt3h3ouXylVvtWMEEirsegHWyZ2mI10L1sN4dAQJx0qmbkXHjMZkEIWiDT78y5FFA3xKxE0ntqI%2FzvWX%2B4PH8TqUQTsnenhPUY6IjpzI3bHFtPy9hBVWM5teRuM%2F; _cc_=URm48syIZQ%3D%3D; enc=sAUMsZDbdTSlTdCrcAW7eFA0y8DMTaW1SRPSkRXXWFpNspn25mtioyzNUoKpSkXyx3u6DvT2u%2BHuABpV1TR%2B4g%3D%3D; uc1=cookie14=UoexMSpaOz2q1A%3D%3D; cookie2=1773c49ab2fa830ca1c287875e089720; _tb_token_=efe587ae3f8de; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; xlly_s=1; JSESSIONID=3BE72A368B93E616359605CA39A9FE1D; l=eBOHqmLeLNNmbWkNBO5w-urza77OzCOf1xNzaNbMiInca1PATgILxNChTl5J7dtjgtfAQetzHj297Rnk-_Udg2HvCbKrCyClkxJ6-; tfstk=cxNRBFGbsijka_gY78B08uizloFRaFR-vUiw9WQEplIFoMRJNsb_s5KT-Tgtb0QA.; isg=BGFhXzDHp76LOwtc7Yy83uHncC17DtUA0tFOzcMzDWmbKoL8C1-90O0sjF6skW04',
    }

    params = {
        'data-key': 's',
        'data-value': '88',
        'ajax': 'true',
        '_ksTS': '1653531657159_1020',
        'callback': 'jsonp1021',
        'q': '苹果手机',
        'commend': 'all',
        'ssid': 's5-e',
        'search_type': 'item',
        'sourceId': 'tb.index',
        'spm': 'a21bo.jianhua.201856-taobao-item.2',
        'ie': 'utf8',
        'initiative_id': 'tbindexz_20170306',
        'bcoffset': '-2',
        'ntoffset': '4',
        'p4ppushleft': '2,48',
        's': '%s' % (page * 44),
    }

    response = requests.get('https://s.taobao.com/search', params=params, cookies=cookies, headers=headers)
    print(response.status_code)

    result = response.content.decode('utf-8')
    result2 = re.findall(r'\n\n[a-z]+[0-9]+\((.*)\);', result)[0]
    result3 = json.loads(result2)

    # print(result3)
    list1 = result3['mods']['itemlist']['data']['auctions']
    return list1


def save_to_excel(list2):
    df = pd.DataFrame(list2)
    df.to_excel('result2.xlsx')
    print('保存文件成功')


if __name__ == '__main__':
    list2 = list()  # 
    for page in range(2):
        list1 = request_data(page)
        for i in list1:
            item = dict()
            item['raw_title'] = i.get('raw_title')  # 标题
            item['view_price'] = i.get('view_price', 0)  # 价格
            item['nick'] = i.get('nick', '未知店铺')  # 店铺名
            list2.append(item)

    save_to_excel(list2)