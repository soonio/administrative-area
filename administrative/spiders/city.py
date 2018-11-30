# -*- coding: utf-8 -*-
import scrapy
import json


class CitySpider(scrapy.Spider):
    name = 'city'
    allowed_domains = ['http://www.stats.gov.cn']

    start_urls = list(
        map(
            lambda x: "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/" + x,
            [
                '11.html',
                '12.html', '13.html', '14.html', '15.html', '21.html', '22.html', '23.html', '31.html', '32.html', '33.html', '34.html', '35.html', '36.html', '37.html', '41.html', '42.html', '43.html', '44.html', '45.html', '46.html', '50.html', '51.html', '52.html', '53.html', '54.html', '61.html', '62.html', '63.html', '64.html', '65.html'
            ]
        )
    )

    def parse(self, response):
        hrefs = []

        area = open('./area.json', 'r')
        data = json.loads(area.read())
        area.close()

        for tr in response.xpath("//tr[@class='citytr']"):
            td = tr.xpath("./td")[1]

            city = td.xpath("./a/text()").extract()[0]
            href = td.xpath("./a/@href").extract()[0]
            code = href[:-5]
            codes = code.split('/')
            current_code = codes[-1]

            parent = data

            for c in codes[:-1]:
                parent = parent.get(c).get("child")

            parent[current_code] = {
                'name': city,
                'child': {}
            }

            hrefs.append(href)

        area = open('./area.json', 'w')
        area.write(json.dumps(data, ensure_ascii=False))
        area.close()

        print(hrefs)


