# administrative-area

基于scrapy，抓取国家行政区划

## 命令

### 启动爬虫爬取数据
```bash
scrapy crwal all
```

### 自动生成一个spider
```bash
scrapy genspider all "http://www.stats.gov.cn"
```

## 注意事项

- 安装scrapy需要安装Twisted，pip安装的twisted有点问题，可以直接下载twisted最新的安装包，解压后，使用python setup.py install进行安装

- 使用scrapy命令时，可能会报缺少incremental， 所有incremental也要提前安装

- 在爬取子级页面的时候，可能出现“Filtered offsite request to” 

```
# 使用 dont_filter设置不过滤即可
yield Request(url, callback=self.parse_item, dont_filter=True)
```