import requests

headers={
'Host': 'p.zwjhl.com',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Referer': 'http://www.lsjgcx.com/',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9'
}

while 1:
    req = requests.get(' http://p.zwjhl.com/price.aspx?url=https%3a%2f%2fitem.jd.com%2f100000769432.html',headers=headers)
    print(req.status_code)