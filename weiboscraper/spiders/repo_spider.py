import scrapy
import json

from scrapy.selector import Selector
from weiboscraper.items import MDBWeiItem

class RepoSpider(scrapy.Spider):
    name = 'repoweibo'
    start_urls = ['https://passport.weibo.cn/signin/login']
    wurl = None

    def __init__(self, wurl=None, *args, **kwargs):
        super(RepoSpider, self).__init__(*args, **kwargs)
        self.wurl = wurl

    def parse(self, response):
        return scrapy.FormRequest(
            url="https://passport.weibo.cn/sso/login",
            formdata={
                'username': 'xxx',
                'password': 'xxx',
                'savestate': '1',
                'ec': '0',
                'pagerefer': '',
                'entry': '',
                'wentry': '',
                'loginfrom': '',
                'client_id': '',
                'code': '',
                'qq': '',
                'hff': '',
                'hfp': ''},
            callback=self.login_click_parse,
            method='POST'
        )

    def login_click_parse(self, response):
        jsonresponse = json.loads(response.body)
        loginresulturl = jsonresponse["data"]["loginresulturl"] + "&savestate=1&callback=jsonpcallback1480557882151"
        return scrapy.http.Request(url=loginresulturl, callback=self.parse_sso1)

    def parse_sso1(self, response): # go to specific weibo page
        request = scrapy.http.Request(url=self.wurl, callback=self.parse_repopage)
        return request

    def parse_repopage(self, response):
        if response.status == 200:
            #contents = Selector(response).xpath('//div[@class="c"]/div/span[@class="ctt"]')
            contents = Selector(response).xpath('//div[@class="c" and @id]')
            for content in contents:
                item = MDBWeiItem()
                item['id'] = content.xpath('@id').extract()
                item['text'] = content.xpath('.//div/span[@class="ctt"]/text()').extract()
                yield item

            nextPage = response.xpath('//div[@class="pa"]/form/div/a[@href]/@href').extract_first()
            if nextPage is not None:
                nextPage = 'https://weibo.cn' + nextPage
                request = scrapy.http.Request(url=nextPage, callback=self.parse_repopage)
                yield request 
        else:
            print "!!!error status: " + response.status 

            