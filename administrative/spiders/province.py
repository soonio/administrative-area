# -*- coding: utf-8 -*-
import scrapy
from json import dumps


class ProvinceSpider(scrapy.Spider):
    name = 'province'
    allowed_domains = ['http://www.stats.gov.cn']

    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/"
    start_url = "index.html"
    start_urls = [url + start_url]

    def parse(self, response):
        hrefs = []
        data = {}
        for tr in response.xpath("//tr[@class='provincetr']"):
            for td in tr.xpath("./td"):
                a = td.xpath("./a")
                if not a:
                    continue

                province = td.xpath("./a/text()").extract()[0]
                href = td.xpath("./a/@href").extract()[0]
                code = href[:-5]
                hrefs.append(href)
                data[code] = {
                    'name': province,
                    "child": {}
                }

        with open('./area.json', 'w') as area:
            if data:
                area.write(dumps(data, ensure_ascii=False))

        print(hrefs)
