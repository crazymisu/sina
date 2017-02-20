# -*- coding: utf-8 -*-
import scrapy
from sina.items import SinaItem
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class SinaspiderSpider(scrapy.Spider):
    name = "sinaspider"
    allowed_domains = ["news.sina.com"]
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        items=[]
        parent_title=response.xpath("//div[@id='tab01']/div/h3[@class='tit02']/a/text()").extract()
        parent_url=response.xpath("//div[@id='tab01']/div/h3[@class='tit02']/a/@href").extract()
        sub_title=response.xpath("//div[@id='tab01']/div/ul/li/a/text()").extract()
        sub_url=response.xpath("//div[@id='tab01']/div/ul/li/a/@href").extract()

        for i in range(0,len(parent_title)):
            parent_Filename='./Data/'+parent_title[i]

            if(not os.path.exists(parent_Filename)):
                os.makedirs(parent_Filename)

            for j in range(0,len(sub_url)):
                item=SinaItem()

                item['parent_title']=parent_title[i]
                item['parent_url']=parent_url[i]

                if_belong=sub_url[j].startswith(item['parent_url'])

                if(if_belong):
                    sub_Filename=parent_Filename+'/'+sub_title[j]

                    if(not os.path.exists(sub_Filename)):
                        os.makedirs(sub_Filename)

                    item['sub_url']=sub_url[j]
                    item['sub_title']=sub_title[j]
                    item['sub_Filename']=sub_Filename

                    items.append(item)

        for item in items:
            yield scrapy.Request(url=item['sub_url'],meta={'meta_1': item}, callback=self.second_parse)

    def second_parse(self,response):
        meta_1=response.meta['mata_1']

        son_url=response.xpath('//a/@href').extract()

        item=[]
        for i in range(0,len(son_url)):
            if_belong = son_url[i].endswith('.shtml') and son_url[i].startswith(meta_1['parent_url'])

            if(if_belong):
                item = SinaItem()
                item['parent_title'] =meta_1['parent_title']
                item['parent_url'] =meta_1['parent_url']
                item['sub_url'] = meta_1['sub_url']
                item['sub_title'] = meta_1['sub_title']
                item['sub_Filename'] = meta_1['sub_Filename']
                item['son_url'] = son_url[i]
                items.append(item)

        for item in items:
                yield scrapy.Request(url=item['son_url'], meta={'meta_2':item}, callback = self.detail_parse)

    def detail_parse(self, response):
        item = response.meta['meta_2']
        content = ""
        title = response.xpath('//h1[@id="main_title"]/text()')
        content_list = response.xpath('//div[@id="artibody"]/p/text()').extract()

        # 将p标签里的文本内容合并到一起
        for content_one in content_list:
            content += content_one

        item['title']= title
        item['content']= content

        yield item
















