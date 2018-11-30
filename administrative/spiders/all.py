# -*- coding: utf-8 -*-
import scrapy
from ..items import AdministrativeItem


class AllSpider(scrapy.Spider):
    name = 'all'
    allowed_domains = ['http://www.stats.gov.cn']
    data_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/"
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html']

    def parse(self, response):
        """
        抓取首页行政区划中省份数据
        :param response:
        :return:
        """
        hrefs = []

        for tr in response.xpath("//tr[@class='provincetr']"):
            for td in tr.xpath("./td"):
                a = td.xpath("./a")
                if not a:
                    continue

                province = td.xpath("./a/text()").extract()[0]
                href = td.xpath("./a/@href").extract()[0]
                code = href[:-5]

                hrefs.append(self.data_url + href)
                yield AdministrativeItem(name=province, code=code)

        for href in hrefs:
            yield scrapy.Request(href, callback=self.parse_city, dont_filter=True)

    @staticmethod
    def code2url(origin):
        """
        根据区划代码生成对应的url
        :param origin:
        :return:
        """
        code = origin
        n = ''
        while len(code) > 2:
            n = n + code[0:2] + '/'
            code = code[2:]

        return n + origin + '.html'

    def parse_city(self, response):
        """
        抓取行政区划中城市数据
        :param response:
        :return:
        """
        hrefs = []
        for tr in response.xpath("//tr[@class='citytr']"):
            td = tr.xpath("./td")[1]

            a = td.xpath("./a")
            if a:
                city = td.xpath("./a/text()").extract()[0]
                href = td.xpath("./a/@href").extract()[0]
                code = href[:-5]
                codes = code.split('/')
                current_code = codes[-1]
                hrefs.append(self.data_url + self.code2url(current_code))
            else:
                tds = tr.xpath("./td/text()")
                city = tds[1].extract()
                current_code = tds[0].extract()[0:4]

            yield AdministrativeItem(name=city, code=current_code)

        for href in hrefs:
            yield scrapy.Request(href, callback=self.parse_county, dont_filter=True)

    def parse_county(self, response):
        """
        抓取行政区划中区/县数据
        :param response:
        :return:
        """
        hrefs = []
        for tr in response.xpath("//tr[@class='countytr']"):
            td = tr.xpath("./td")[1]
            a = td.xpath("./a")
            if a:
                county = td.xpath("./a/text()").extract()[0]
                href = td.xpath("./a/@href").extract()[0]
                code = href[:-5]
                codes = code.split('/')
                current_code = codes[-1]
                hrefs.append(self.data_url + self.code2url(current_code))
            else:
                tds = tr.xpath("./td/text()")
                county = tds[1].extract()
                current_code = tds[0].extract()[0:6]

            yield AdministrativeItem(name=county, code=current_code)

        for href in hrefs:
            yield scrapy.Request(href, callback=self.parse_town, dont_filter=True)

    def parse_town(self, response):
        """
        抓取行政区划中街道/乡镇数据
        :param response:
        :return:
        """
        for tr in response.xpath("//tr[@class='towntr']"):
            td = tr.xpath("./td")[1]

            a = td.xpath("./a")
            if a:
                town = td.xpath("./a/text()").extract()[0]
                href = td.xpath("./a/@href").extract()[0]
                code = href[:-5]
                codes = code.split('/')
                current_code = codes[-1]
            else:
                tds = tr.xpath("./td/text()")
                town = tds[1].extract()
                current_code = tds[0].extract()[0:8]

            yield AdministrativeItem(name=town, code=current_code)
