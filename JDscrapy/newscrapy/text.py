import requests

r = requests.get('https://item.jd.com/7341432.html')
print(r.text)