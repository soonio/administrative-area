# -*- coding: utf-8 -*-
import scrapy
import json


class CountySpider(scrapy.Spider):
    name = 'county'
    allowed_domains = ['http://www.stats.gov.cn']

    start_urls = ["http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/53/5301.html"]

    def parse(self, response):
        for tr in response.xpath("//tr[@class='countytr']"):
            td = tr.xpath("./td")[1]
            a = td.xpath("./a")
            if a:
                county = td.xpath("./a/text()").extract()[0]
                href = td.xpath("./a/@href").extract()[0]
                code = href[:-5]
                codes = code.split('/')
                current_code = codes[-1]
            else:
                tds = tr.xpath("./td/text()")
                county = tds[1].extract()
                current_code = tds[0].extract()[0:6]

            print(county, current_code)
            exit()


