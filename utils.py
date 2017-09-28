import csv
import errno
import os
import re
import pandas as pd
from dateutil.parser import parse
from nltk import ngrams


def date_formatter(date, date_format):
    dt = parse(date)
    date = dt.strftime(date_format)
    return date


def generate_map_n_grams_and_date(date, n, sentence):
    trigram = ngrams(sentence.split(), n)
    for gram in trigram:
        gram = re.sub("\(", "3-gram_", str(gram))
        gram = re.sub(r'[\'|)]', "", gram)
        gram = re.sub(", ", "_", gram)

        yield {'date': date,
               'gram': gram,
               }


def reset_file(file):
    try:
        os.remove(file)
    except OSError:
        pass


def scraping_data_from_wsj_by_year(spider_name, year_to_scraping, month_to_scraping, scraped_data_file):
    reset_file(scraped_data_file)
    os.system('scrapy runspider {0} -o {1} -L ERROR -a year={2} -a month={3}'.
              format(spider_name, scraped_data_file, year_to_scraping, month_to_scraping))
    return scraped_data_file


def create_pivot_table_from_data(file):
    result_file = 'result/result.csv'
    reset_file(result_file)
    df = pd.read_csv(file)
    df.pivot_table(index='date', columns='gram', aggfunc=len, fill_value=0).to_csv(result_file)
    return result_file


def csv_writer(title, data, filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(title)
        writer.writerows(data)


def parse_article_date(response):
    date = response.xpath('//*[@id="archivedArticles"]/h3/text()').extract_first()
    date = date[17:]
    return date


def input_year(message):
    while True:
        try:
            user_input = int(input(message))
            if user_input not in range(2010, 2017):
                raise ValueError('The year should be between 2010-2017')
        except ValueError as e:
            print(e)
            continue
        else:
            return user_input
            break
