from urllib.parse import urljoin

import scrapy

from utils import generate_map_n_grams_and_date, date_formatter, parse_article_date


class WSJSpider(scrapy.Spider):
    name = "trio-gram_spider"

    def __init__(self, year='2015', month=1, *args, **kwargs):
        super(WSJSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.wsj.com/public/page/archive-%s-1-1.html' % year]
        self.month_to_scraping = int(month)

    def parse(self, response):
        urls = []
        month_counter = 0

        for month in response.css('.archiveMonth'):
            urls.extend(month.css('a::attr(href)').extract())
            month_counter += 1
            if month_counter == self.month_to_scraping:
                break

        for day_url in urls:
            url = urljoin(response.url, day_url)
            print('Scraping: %s' % url)
            yield scrapy.Request(url, callback=self.parse_day)

    def parse_day(self, response):
        for article_section in response.xpath('//*[@id="archivedArticles"]/ul/li'):
            headline_text = article_section.css('h2 a ::text').extract_first()
            date = parse_article_date(response)
            date = date_formatter(date,'%m/%Y')
            yield from generate_map_n_grams_and_date(date, 3, headline_text)
