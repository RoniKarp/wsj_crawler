from utils import scraping_data_from_wsj_by_year, create_pivot_table_from_data

year = input("Enter Year(yyyy):")
print("Start analyses..")
data_file = scraping_data_from_wsj_by_year("trio_gram_spider.py", year, 1,'result/temp/ex2_scraped_data.csv')
print("Scraping complete..")
print("Start pivot..")
result_data_file = create_pivot_table_from_data(data_file)
print("Pivot complete..")
print("The processing data complete, the result store on: {0}".format(result_data_file))
