import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Request

class AldiSpider(scrapy.Spider):
	# A crawler to parse items from the Aldi Groceries section
	name = 'aldispider'
	start_urls = ['https://www.aldi.com.au/']

	def parse(self, response):
		print("Processing:" + response.url)
		# Extract urls for groceries menu items
		next_urls = response.xpath('//div[@class="main"]/nav/ul/li[2]/div[2]/ul/li[not(contains(@class, "is-closed"))]/div/a/@href').extract()
		# Loop through each item to create parse the pages
		for next_url in next_urls:
			yield Request(response.urljoin(next_url), callback = self.parse_product_page)
			
	def parse_product_page(self, response):
		# Loop through each product tile on the page
		for aldi_products in response.css("div.tx-aldi-products"):
			prod = aldi_products.css("a")
			
			for prod_sel in prod:
				# Selector tags for each field
				TITLE_SELECTOR ='div.box--description--header::text'
				IMAGE_SELECTOR = 'div.box--image-container > img'
				PACKSIZE_SELECTOR = 'div.box--price > span.box--amount::text'
				BASEPRICE_SELECTOR = 'div.box--price > span.box--baseprice::text'
				price_val = prod_sel.css('div.box--price > span.box--value::text').extract_first()
				price_decimal = prod_sel.css('div.box--price > span.box--decimal::text').extract_first()

				try:	
					product_title = ' '.join(prod_sel.css(TITLE_SELECTOR).extract()).strip()
					product_image = prod_sel.css(IMAGE_SELECTOR).xpath('@src').get()
					packsize = prod_sel.css(PACKSIZE_SELECTOR).extract_first()
					price = ''.join(filter(None, [price_val, price_decimal]))
					if not price.startswith('$'):
						price += 'c'
					price_per_unit = prod_sel.css(BASEPRICE_SELECTOR).extract_first()

					# Yield the result to the feed
					yield {
						"Product_title" : product_title,
						"Product_image" : product_image,
						"Packsize" : packsize,
						"Price" : price,
						"Price per unit" : price_per_unit
					}
				except Exception as e:
					print(e)

# Define settings for the crawler
process = CrawlerProcess(settings={
    "FEEDS": {
    	"products.csv": {"format" : "csv"},
    },
})

process.crawl(AldiSpider)
process.start()
