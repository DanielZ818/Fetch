"""
The first version of Pankit: Get filename given a shared baidupan url
Tried to simulate human request and session using cookies
Archived and discontinued!
"""

import time
import requests

url = 'https://pan.baidu.com/s/1M75vcorqcpsdfwxX_mxfQ?pwd=foo'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en',
    'Connection': 'keep-alive',
    'Host': 'pan.baidu.com',
    'Referer': 'https://pan.baidu.com/share/init?surl=M75vcorqcplv4wxX_mlxfQ&pwd=753j',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

cookies = 'foo=foo'
cookies = cookies.split('; ')
cookie = {}
for i in cookies:
    cookie[i.split('=')[0]] = '='.join(i.split('=')[1::])


a = {
    # 'BAIDUID': 'EBB03E20FBC6ABA16F5D2415773CA56F:FG=1',
     # 'BAIDUID_BFESS': 'EBB03E20FBC6ABA16F5D2415773CA56F:FG=1',
     # 'ab_jid': '2a685982b9268e01b7e046b1cc27e3dd1d8c',
     # 'ab_bid': '2a685982b9268e01b7e046b1cc27e3dd1d8c',
     # 'ab_sr': '1.0.1_ZTA1NTQwZmEyNzU2NTA1ZDRhNzVmYWE4MGE2OTMyNTBjZjY2MWRkZjMzNjU4MjUyZjhkYzRiYmE5MjE1MmY1Y2UxNTRjNzRmNjIzMjlhZWZkYTg1NzIyMzk1YzUzOWIxZjJjYzEyYTQ5YTVmMDkwYjk4ODdkMjE5ZmY4N2FhOWU0MDY3ZGEzZGM2M2UyNjk5YzQ1M2Y3ZTY2ZTRjNjMyYw==',
     # 'ab_jid_BFESS': '2a685982b9268e01b7e046b1cc27e3dd1d8c',
     # 'XFI': '4fd6431f-4378-9eb4-3a46-086db696439f',
     # 'XFCS': '0A959A29C9B1EA571CDC065AE4C23A7AAF08CD71784304DFC0C88519CD1969FB',
     # 'XFT': 'iRsIdNZyELMAqkQF2ngjxSs/Fh2L0N2Hdv0OsOapgU4=',
     # 'csrfToken': 'S3cqiabmfU_k5larW1hTeZ64',
     # 'HMACCOUNT': 'F1CE75B7C9A22E84',
     # 'HMACCOUNT_BFESS': 'F1CE75B7C9A22E84',
     # 'PANWEB': '1',
     # 'Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0': '1683488649',
     'BDCLND': 'bxvhNHmeq8fLdwoaecTFDRRlBPgzOSmjH1xINTD%2FdhA%3D',
     # 'XFS': 'iRsIdNZyELMAqkQF2ngjxSs/Fh2L0N2Hdv0OsOapgU4=',
     # 'Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0': '1683489379',
     # 'ndut_fmt': '7FD069FA2E1FD6273C395DE56DB68AABBB313C'
     }

# response = requests.get(url, headers=headers, cookies=a)
# print(response.url)
# print(response.status_code)
# # print(response.json())
# title = BeautifulSoup(response.text, features='html.parser').prettify().title()
# print(title.split('Title')[1])



query = {'surl': 'M75vcorqcplv4wxX_mlxfQ',
         't': str(int(time.time())),
         'channel': 'chunlei',
         'web': '1'
         }
data = {'pwd': '753j'}
cookie = {'csrfToken': 'nNuRN2fxB0YKul28bpseUuzj',
          'BAIDUID': 'BAIDUID=D07A4D9B27C49238A6F6974A2C6D7DF5:FG=1',
          'BAIDUID_BFESS':'6BAC56A9603441B173D503953D255F34',
          'PANWEB': '1'
          }
url = 'https://pan.baidu.com/share/verify'
h = requests.post(url=url, data=data)
print(h.text)
