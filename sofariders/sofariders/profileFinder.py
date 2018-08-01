from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv


csv_file = open('profileURLs.csv', 'w')
writer = csv.writer(csv_file)

driver = webdriver.Chrome()

# To avoid 250-page limit, scrape first 5000 prfiles from lots of cities instead of only one
print('Scraping list of cities for URLs')
cityurls = []
driver.get('https://www.couchsurfing.com/places')
citylist = driver.find_elements_by_xpath('//section[@class="cs-sitemap-region"]//li//a')
for city in citylist:
    cityurls += [city.get_attribute('href') + '/accommodation']
print("Found " + str(len(cityurls)) + " locations to scrape")

for citypage in cityurls:
    print('Scraping ' + citypage)
    driver.get(citypage)
    wait_urls = WebDriverWait(driver, 10)

    index = 1
    while index <= 200:  # For each page of profiles
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
            wait_button = WebDriverWait(driver, 10)
            next_button = wait_button.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[@aria-label="Next Page"]')))
            next_button.click()

        except Exception as e:
            print(e)
            driver.close()
            csv_file.close()
            break
