from base_spider import WSJSpider
from utils import csv_writer, date_formatter, parse_article_date


class ArticleInfoSpider(WSJSpider):
    name = "article_info_spider"

    def parse_day(self, response):
        date = parse_article_date(response)
        filename = "ex1_result/" + date_formatter(date, '%Y/%m/%d') + ".csv"
        date = date_formatter(date, '%d/%m/%Y')

        articles_info = []
        for article in response.xpath('//*[@id="archivedArticles"]/ul/li'):
            article_tuple = self.build_article_tuple(article, date)
            articles_info.append(article_tuple)

        csv_title = ('date', 'Headline', 'url')
        csv_writer(csv_title, articles_info, filename)

        return None

    def build_article_tuple(self, article, date):
        headline = article.css('h2 a ::text').extract_first()
        headline = str(headline).encode('utf-8')
        url = article.css('h2 a::attr(href)').extract_first()
        day = date
        article_tuple = (day, headline, url)
        return article_tuple
