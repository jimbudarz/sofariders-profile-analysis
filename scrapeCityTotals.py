# Since the initial scrape didn't pull the number of hosts per city, this script can be run separately to pull that data.
from selenium import webdriver
import csv

with open('completecities.txt','r') as finishedCityFile:
    finishedcities = finishedCityFile.readlines()
finishedcities = list(map(lambda x: x.strip('\n'), finishedcities))

# Loop over all cities for which users have been scraped

driver = webdriver.Chrome()
csv_file = open('cityHostNumbers.csv', 'a')
writer = csv.writer(csv_file)

urls = []
citynames = []
citynHosts = []
for city in finishedcities:
    driver.get(city)
    nHosts = driver.find_element_by_xpath('//header[@class="box-header mod-host-search mod-map-search mod-padding-bottom-5 u-clear"]//h2').get_attribute('data-count')
    cityname = driver.find_element_by_xpath('//nav[@class="text mod-regular mod-bold mod-block"]//strong').text.split(' ')[2]
    print(cityname)
    city_deets = {'nHosts':nHosts, 'cityurl':city, 'cityname':cityname}
    writer.writerow(city_deets.values())

driver.close()
csv_file.close()
