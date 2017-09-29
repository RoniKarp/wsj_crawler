from utils import scraping_data_from_wsj_by_year, input_year, reset_result_folder

reset_result_folder()
from_year = input_year("Enter From Year(yyyy):")
to_year = input_year("Enter To Year(yyyy):")
year_list=range(int(from_year),int(to_year)+1)
print("Start analyses..")
for year in year_list:
    print(year)
    scraping_data_from_wsj_by_year("article_info_spider.py", year, 12,'result/temp/ex1_scraped_data.csv')
print("Scraping complete..")
