from eyespider.items import EyespiderItem
import datetime
import scrapy
import urlparse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field


class coverSpider(scrapy.Spider):
	name = "pyimagesearch-cover-spider"
	start_urls = ["https://en.wikipedia.org/wiki/Eye_color"]
	allowed_domains = ['wikipedia.org']
	#rules = (Rule(LinkExtractor(), callback='parse_item', follow=True), )


	def parse(self, response):
		item = EyespiderItem()
		#imgs = response.css('img').xpath('@src[contains(.,"EYE") or contains(.,"eye") or contains(.,"Eye") or contains(.,"iris") or contains(.,"pupil")]' ).extract()
		imgs = response.css('img').xpath('@src').extract()

		words = ["eye", "iris", "pupil", "hetero", "cornea", "amber", "blue", "green", "hazel", "stroma", "retina"]

		keywords = []
		keywordsUpper = []
		keywordsFirstLetterUpper = []

		for i in range(len(words)):
			keyword = words[i]
			keywordUpper = keyword.upper()
			keywordFirstLetterUpper = keyword[0].upper() + keyword[1:]

			keywords.append(keyword)
			keywordsUpper.append(keywordUpper)
			keywordsFirstLetterUpper.append(keywordFirstLetterUpper)
			
		allImgs = []
		urls = []
		for i in range(len(words)):
			kw = response.css('img[alt*="' + keywords[i] + '"], img[src*=" '+ keywords[i] +'"]').xpath('@src').extract()
			kwu = response.css('img[alt*="' + keywordsUpper[i] + '"], img[src*=" '+ keywordsUpper[i] +'"]').xpath('@src').extract()
			kwflu = response.css('img[alt*="' + keywordsFirstLetterUpper[i] + '"], img[src*=" '+ keywordsFirstLetterUpper[i] +'"]').xpath('@src').extract()
			u = response.css('a[href*="' + keywords[i] + '"]').xpath('@href').extract()
			uu = response.css('a[href*="' + keywordsUpper[i] + '"]').xpath('@href').extract()
			uufw = response.css('a[href*="' + keywordsUpper[i] + '"]').xpath('@href').extract()

			if(kw):
				allImgs.append(kw)
			if(kwu):
				allImgs.append(kwu)

			if(kwflu):
				allImgs.append(kwflu)

			if(u):
				urls.append(u)
			if(uu):
				urls.append(uu)
			if(uufw):
				urls.append(uufw)

		#alts = response.css('img[alt*="eye"], img[src*="Hetero"]').xpath('@src').extract()
		#item['image_urls'] = ["http:" + x for x in imgs]
		#yield item

		for i in range(len(allImgs)):
			for j in range(len(allImgs[i])):
				try:
					yield EyespiderItem(image_urls=[urlparse.urljoin(response.url, allImgs[i][j].strip() )])
					#yield EyespiderItem(image_urls=[imgs[i].strip() ])
					#print "aaaa"
				except:
					print "bad image"
		"""
		for i in range(len(imgs)):
			#imgs[i] = "http:" + imgs[i]

			try:
				yield EyespiderItem(image_urls=[urlparse.urljoin(response.url, imgs[i].strip() )])
				#yield EyespiderItem(image_urls=[imgs[i].strip() ])
				print "aaaa"
			except:
				print "bad image"
		"""
		for i in range(len(urls)):
			for j in range(len(urls[i])):
				#print urls[i][j]
				try:
					yield scrapy.Request(urlparse.urljoin(response.url, urls[i][j].strip()), callback=self.parse)
				except:
					print "bad url"
		#for url in response.css('a').xpath('@href').extract():
		#print url

		#for url in response.xpath('//a/@href').extract():
		#	print url
			#url = "http:" + url		
			#try:
			#	yield scrapy.Request(urlparse.urljoin(response.url, url.strip()), callback=self.parse)
			#except:
			#	print "bad url"
		
		#for i in range(len(url)):
		#yield scrapy.Request(url[3], self.parse_page)
		#return item
