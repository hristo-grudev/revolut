import json

import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import RevolutItem
from itemloaders.processors import TakeFirst


class RevolutSpider(scrapy.Spider):
	name = 'revolut'
	start_urls = ['https://www.revolut.com/page-data/en-BG/news/page-data.json']

	def parse(self, response):
		data = json.loads(response.text)
		for post in data['result']['data']['newsroomJson']['Global']:
			title = post['title']
			date = post['date']
			url = 'https://www.revolut.com/page-data/en-BG/news/' + post['url'] + '/page-data.json'
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date, 'title': title})

	def parse_post(self, response, date, title):
		data = json.loads(response.text)
		description = remove_tags(data['result']['data']['article']['article']['content'])

		item = ItemLoader(item=RevolutItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
