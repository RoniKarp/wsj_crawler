from base_spider import WSJSpider
from utils import generate_map_n_grams_and_date, date_formatter, parse_article_date


class TrioGramSpider(WSJSpider):
    name = "trio-gram_spider"

    def parse_day(self, response):
        for article_section in response.xpath('//*[@id="archivedArticles"]/ul/li'):
            headline_text = article_section.css('h2 a ::text').extract_first()
            date = parse_article_date(response)
            date = date_formatter(date, '%m/%Y')
            yield from generate_map_n_grams_and_date(date, 3, headline_text)
