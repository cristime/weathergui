import requests
import requests
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4688.0 Safari/537.36 Edg/97.0.1069.0"
}
url = "http://www.weather.com.cn/weather/101220501.shtml"

res = requests.get(url, headers)

# print(res.content.decode("utf-8"), end="\n"*5)

html = etree.HTML(res.content.decode("utf-8"), parser=etree.HTMLParser())
result = html.xpath('//div[@id="7d"]/ul/li[1]/h1/text()')
print(result)