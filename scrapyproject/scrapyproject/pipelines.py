# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapyprojectPipeline(object):
    def __init__(self,*args, **kwargs):

        print('4'*50)

    @classmethod
    def from_crawler(cls, crawler):
        print('3'*50)

        return cls(
        unique_id=crawler.settings.get('unique_id'), # this will be passed from django view
                                                      #we can pass whatever we want from jango to scrapy
        timepass=crawler.settings.get('timepass'),
        )

    def process_item(self, item, spider):
        print('6'*50)

        for i in range(20):
            print("helooooooooooooooooooooooo")
        print()
        print("current price in pipeline is ",item['current_price'])
        print()
        if item['current_price']!=-999 and item['current_price']!=-1.00:
            item.save()
        for i in range(20):
            print("dddddonnnnnneeeeeeeooooooooooooooooooooo")
        return item


#first from view.py in gango we have write task = scrapyd.schedule() ..this will run and scrapy task will be assign
#we can check that task sceduling status from local host..but we dont require it in deployment...
#it is for just checking what is status of task
#then scrapy will crawl immediatel after task = scrapyd.schedule() this statement
#first it will go to items.py then call spider class...hence only init()will be executed then comes in pipelines.py and runs from_crawler(cls, crawler) then this method will
#pipleine class will called and will get returned parameter from crawler method.hence only init() will executed havig that parameters
#then main parse class will be calledand finally after yield statement process_item method will excuted and 
#save data in database