from scrapy import Spider, Request
from sofariders.items import SofaridersItem
import numpy as np
from urllib.parse import urljoin


class SofaRidersSpider(Spider):
    name = 'sofariders_spider'
    allowed_urls = ["https://www.couchsurfing.com/"]
    start_urls = ["https://www.couchsurfing.com/places/north-america/united-states/new-york/accommodation"]


    def parse(self, response):
        responseRate = 0
        resultsSoFar = {'responseRate': responseRate}

        urls = ['https://www.couchsurfing.com/people/veysel-tunca',
                'https://www.couchsurfing.com/people/ryany',
                'https://www.couchsurfing.com/people/swaroop-bose',
                'https://www.couchsurfing.com/people/bennyroyce-royon']

        for url in urls:
            yield Request(url=url, meta=resultsSoFar, callback=self.parseAbout)

    def parseAbout(self, response): # Parse the information from profile's About page.
        resultsSoFar = response.meta

        resultsSoFar['user_url'] = response.xpath("//div[@class='profile-sidebar__user-status u-text-center u-clear']//a/@href").extract_first()
        resultsSoFar['location'] = response.xpath("//a[@class='profile-sidebar__city text mod-regular mod-block']//text()").extract_first()
        resultsSoFar['lastLogin'] = response.xpath("//div[@class='multicolumn-column mod-3-5']/ul/li/text()[contains(.,'Last')]").extract_first().strip()
        resultsSoFar['referenceSummary'] = response.xpath("//ul[@class='mod-icon-bullets']//li/strong/text()").extract()[1].strip()
        resultsSoFar['couchStatus'] = response.xpath("//div[@class='multicolumn-column mod-3-5']/h1/span//text()").extract_first().strip()
        resultsSoFar['verificationStatus'] = response.xpath("//h3[@class='profile-sidebar__verification-title']//span/text()").extract_first().strip()

        AboutSummary = response.xpath("//ul[@class = 'mod-icon-bullets']/li/text()").extract()
        AboutSummary = list(map(lambda x: x.strip(), AboutSummary))
        resultsSoFar['languages'] = AboutSummary[1].strip()
        resultsSoFar['age'] = int(AboutSummary[2].strip().split(', ')[0])
        resultsSoFar['sex'] = AboutSummary[2].strip().split(', ')[1]
        resultsSoFar['joinDate'] = AboutSummary[4].strip()
        resultsSoFar['job'] = AboutSummary[6].strip()
        resultsSoFar['education'] = AboutSummary[8].strip()
        resultsSoFar['hometown'] = AboutSummary[len(AboutSummary)-3].strip()
        resultsSoFar['profileCompletion'] = AboutSummary[len(AboutSummary)-1].strip()

        url_MyHome = response.xpath("//a[@class='tab-link' and text()='My Home']//@href").extract_first()

        print(50 * '=')
        print(resultsSoFar)
        print(50 * '=')

        item = SofaridersItem()
        item['responseRate'] = []
        item['user_url'] = resultsSoFar['user_url']  # Assigned
        item['lastLogin'] = resultsSoFar['lastLogin']  # Assigned
        item['couchStatus'] = resultsSoFar['couchStatus']  # Assigned
        item['location'] = resultsSoFar['location']  # Assigned
        item['verificationStatus'] = resultsSoFar['verificationStatus']  # Assigned
        item['languages'] = resultsSoFar['languages']  # Assigned
        item['age'] = resultsSoFar['age']  # Assigned
        item['sex'] = resultsSoFar['sex']  # Assigned
        item['joinDate'] = resultsSoFar['joinDate']  # Assigned
        item['hometown'] = resultsSoFar['hometown']  # Assigned
        item['profileCompletion'] = resultsSoFar['profileCompletion']  # Assigned
        item['education'] = resultsSoFar['education']  # Assigned
        item['maxGuests'] = []
        item['preferredGender'] = []
        item['lastMinuteOkay'] = []
        item['refs_fromSurfers_pos'] = []
        item['refs_fromSurfers_neg'] = []
        item['refs_fromHosts_pos'] = []
        item['refs_fromHosts_neg'] = []
        item['friends'] = []

        yield item

        #yield Request(url=response.urljoin(url_MyHome), meta=resultsSoFar, callback=self.parseMyHome)

    def parseMyHome(self, response):
        # Add all information on this page to the meta
        resultsSoFar = response.meta

        url_references = response.xpath(
            "//a[@class='tab-link' and contains(text(),'References')]//@href").extract_first()

        yield Request(url=response.urljoin(url_references), meta=resultsSoFar, callback=self.parseReferences)

    def parseReferences(self, response):
        resultsSoFar = response.meta

        url_friends = response.xpath(
            "//a[@class='tab-link' and contains(text(),'Friends')]//@href").extract()

        yield Request(url=response.urljoin(url_friends), meta=resultsSoFar, callback=self.parseFriends)

    def parseFriends(self, response):
        resultsSoFar = response.meta

        item = SofaridersItem()
        item['responseRate'] = []
        item['user_url'] = resultsSoFar['user_url']  # Assigned
        item['lastLogin'] = resultsSoFar['lastLogin']  # Assigned
        item['couchStatus'] = resultsSoFar['couchStatus']  # Assigned
        item['location'] = resultsSoFar['location']  # Assigned
        item['verificationStatus'] = resultsSoFar['verificationStatus']  # Assigned
        item['languages'] = resultsSoFar['languages']  # Assigned
        item['age'] = resultsSoFar['age']  # Assigned
        item['sex'] = resultsSoFar['sex']  # Assigned
        item['joinDate'] = resultsSoFar['joinDate']  # Assigned
        item['hometown'] = resultsSoFar['hometown']  # Assigned
        item['profileCompletion'] = resultsSoFar['profileCompletion']  # Assigned
        item['education'] = resultsSoFar['education']  # Assigned
        item['maxGuests'] = []
        item['preferredGender'] = []
        item['lastMinuteOkay'] = []
        item['refs_fromSurfers_pos'] = []
        item['refs_fromSurfers_neg'] = []
        item['refs_fromHosts_pos'] = []
        item['refs_fromHosts_neg'] = []
        item['friends'] = []

        yield item
