# This script uses Selenium to scrape a list of users from each city,
# create a list of URLs for their profiles, and take any data avaialable
# about them from the search page alone. This uses Selenium because search
# pages are dynamically loaded using AJAX. 


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import random

driver = webdriver.Chrome()

# Create/load files to store data
csv_file = open('profileURLs.csv', 'a')
writer = csv.writer(csv_file)
#with open('completecities.txt','r') as finishedCityFile:
#    finishedcities = finishedCityFile.readlines()
#finishedcities = list(map(lambda x: x.strip('\n'), finishedcities))

# To avoid 250-page limit, scrape first 5000 prfiles from lots of cities instead of only one
print('Scraping list of cities for URLs')
cityurls = []
driver.get('https://www.couchsurfing.com/places')
citylist = driver.find_elements_by_xpath('//section[@class="cs-sitemap-region"]//li//a')
for city in citylist:
    cityurls += [city.get_attribute('href') + '/accommodation']
random.shuffle(cityurls)
print("Found " + str(len(cityurls)) + " locations to scrape")

for citypage in cityurls:
    print('Scraping ' + citypage)

    # Check list of cities already fetched and skip if it's already in the data
    with open('completecities.txt','r') as finishedCityFile:
        finishedcities = finishedCityFile.readlines()
    finishedcities = list(map(lambda x: x.strip('\n'), finishedcities))
    print("Cities finished: " + str(len(finishedcities)) + " of " + str(len(cityurls)))
    if citypage in finishedcities:
        print("This city has already been done")
        continue

    # Load the current city's results page
    driver.get(citypage)
    wait_urls = WebDriverWait(driver, 10)

    index = 1
    while index <= 50:  # Fetch information from each set of results and then move on to the next set
        try:
            url_list = []
            # Click Next Page button
            print('Scraping page ' + str(index))
            index += 1
            # Make a dictionary of user profiles and information available on results page:
            userboxes = wait_urls.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="user-card__content mod-host"]')))
            #print(str(len(userboxes)) + ' userboxes on this page')
            for userbox in userboxes:  # For each profile URL on this page of results
                # Extract useful information from each user's box
                user_url = userbox.find_elements_by_xpath(
                    ".//a[@class='user-card__profile-link']")[0].get_attribute('href')
                responseSpeed = userbox.find_element_by_xpath('.//span[@class="user-card__response-time text mod-gray"]').text
                refsandfriends = userbox.find_element_by_xpath('.//div[@class="user-card__stats"]/div').text
                #nRefs = refsandfriends.split('\n')[0]
                #nFriends = refsandfriends.split('\n')[1]
                try:
                    languages = userbox.find_element_by_xpath('.//span[@class="user-card__languages mod-1-line"]').text
                except:
                    languages = ''
                couchStatus = userbox.find_element_by_xpath('//span[contains(.,"Guests")]').text
                # Make a dictionary for each user profile:
                user_deets = {'user_url':user_url, 'responseSpeed':responseSpeed,'refsandfriends':refsandfriends, 'languages':languages, 'couchStatus':couchStatus}
                writer.writerow(user_deets.values())
            time.sleep(10)
            wait_button = WebDriverWait(driver, 5)
            next_button = wait_button.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[@aria-label="Next Page"]')))
            next_button.click()

        except Exception as e:
            print(e)
            driver.close()
            csv_file.close()
            break
    with open('completecities.txt','a') as finishedCityFile:
        finishedCityFile.write(citypage + '\n')
