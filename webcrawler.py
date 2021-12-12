import json

import requests
from lxml import etree


class WebCrawler:
    def __init__(self, cityCodeFile : str):
        """
        初始化
        :param cityCodeFile: 表示城市代码的文件路径
        """
        # 读取城市编码 json
        with open(cityCodeFile, "r") as file:
            self.cityCodes = json.load(file)
        
        # requests 相关设置: url 前缀与请求头
        self.urlPrefix = "http://www.weather.com.cn/weather/{}.shtml"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4688.0 Safari/537.36 Edg/97.0.1069.0"
        }

        # 预定义好的匹配字符串
        self.matchDate = '//div[@id="7d"]/ul/li[{}]/h1/text()'
        self.matchWeather = '//div[@id="7d"]/ul/li[{}]/p[1]/text()'
        self.matchMaxTemp = '//div[@id="7d"]/ul/li[{}]/p[@class="tem"]/span/text()'
        self.matchMinTemp = '//div[@id="7d"]/ul/li[{}]/p[@class="tem"]/i/text()'
        self.matchWindDir = '//div[@id="7d"]/ul/li[{}]/p[@class="win"]/em/span[1]/@title'
        self.matchWindSpeed = '//div[@id="7d"]/ul/li[{}]/p[@class="win"]/i/text()'

    def GetPage(self, cityName : str):
        """
        获取当前城市的七日天气的 html 文件
        :param cityName: 中文城市名称
        """
        # 获取指定城市对应 url
        cityCode = self.cityCodes[cityName]
        url = self.urlPrefix.format(cityCode)

        # GET 所需页面
        response = requests.get(url, headers=self.headers)
        
        # 如果 response 的状态值不为 200 则表示城市名不存在
        if response.status_code != 200:
            return None
        
        # 否则返回 html 文件内容
        return response.content.decode("utf-8")
    
    def ParseWeather(self, page : str):
        """
        解析 html 文件获取气温、降水、风速等信息
        :param page: html 页面对象
        """
        # 解析 html
        html = etree.HTML(page, parser=etree.HTMLParser())
        weatherInfo = []
        
        # 枚举每一天
        for count in range(1, 7 + 1):
            # 解析对应信息
            date = html.xpath(self.matchDate.format(str(count)))
            weather = html.xpath(self.matchWeather.format(str(count)))
            maxTemp = html.xpath(self.matchMaxTemp.format(str(count)))
            minTemp = html.xpath(self.matchMinTemp.format(str(count)))
            windDir = html.xpath(self.matchWindDir.format(str(count)))
            windSpeed = html.xpath(self.matchWindSpeed.format(str(count)))

            # 打包进字典
            weatherToday = {
                "date": date[0],
                "weather": weather[0],
                "maxTemp": maxTemp[0],
                "minTemp": minTemp[0].split("℃")[0],
                "windDir": windDir[0],
                "windSpeed": windSpeed[0]
            }

            # 加入列表
            weatherInfo.append(weatherToday)
        
        return weatherInfo

if __name__ == "__main__":
    crawler = WebCrawler("citycode.json")
    res1 = crawler.GetPage("马鞍山")
    if res1 == None:
        print("Error: City not found")
    else:
        res2 = crawler.ParseWeather(res1)
        for each in res2:
            print("Date: " + each["date"])
            for each2 in each.items():
                if each2[0] == "date":
                    continue
                print(each2[0] + ":\t" + str(each2[1]))
            print()

