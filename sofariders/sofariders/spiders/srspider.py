from scrapy import Spider
from sofariders.items import SofaridersItem


class SofaRidersSpider(spider):
    name = 'sofariders_spider'
    allowed_urls = "https://www.couchsurfing.com/"
    start_url = "https://www.couchsurfing.com/places/north-america/united-states/new-york/accommodation"

    def parse(self, response):
        # It turns out this site doesn't keep host results on separate pages, so I'll need to use Selenium to navigate the page.
        # Anyway, determine the number of pages of results there will be:
        # Nothing seems to work because scrapy doesn't get a real page in return.
        # //div[@class ="pagination-label u-text-center"]/text()

    def parseAbout(self, response):  # Surprisingly, this section works!
        # Pull all available information from profile's About page and move on to other pages.
        user_url = response.xpath(
            "//div[@class='profile-sidebar__user-status u-text-center u-clear']//a/@href").extract_first()
        location = response.xpath(
            "//a[@class='profile-sidebar__city text mod-regular mod-block']//text()").extract_first()
        lastLogin = response.xpath(
            "//li[@class='text mod-gray mod-medium']//text()").extract_first().strip()
        referenceSummary = response.xpath(
            "//ul[@class='mod-icon-bullets']//li/strong/text()").extract()[1].strip()
        couchStatus = response.xpath(
            "//h1/span[@class='mod-large']//text()").extract_first().strip()
        verificationStatus = response.xpath(
            "//h3[@class='profile-sidebar__verification-title']//span/text()").extract_first().strip()

        AboutSummary = response.xpath(
            "//ul[@class = 'mod-icon-bullets']/li/text()").extract()
        languages = AboutSummary[1].strip()
        age = int(AboutSummary[2].strip().split(', ')[0])
        sex = AboutSummary[2].strip().split(', ')[1]
        joinDate = AboutSummary[4].strip()
        job = AboutSummary[6].strip()
        education = AboutSummary[8].strip()
        hometown = AboutSummary[10].strip()
        profileCompletion = AboutSummary[12].strip()

        url_MyHome = response.xpath(
            "//a[@class='tab-link' and text()='My Home']//@href").extract_first()

        resultsSoFar = {'user_url': user_url, 'location': location, 'lastLogin': lastLogin,
                        'referenceSummary': referenceSummary, 'couchStatus': couchStatus,
                        'verificationStatus': verificationStatus, 'languages': languages,
                        'age': age, 'sex': sex, 'joinDate': joinDate, 'job': job,
                        'education': education, 'hometown': hometown,
                        'profileCompletion': profileCompletion}

        yield Request(url=url_MyHome, meta=resultssofar, callback=self.parseMyHome)

    def parseMyHome(self, response):
        # Add all information on this page to the meta
        resultsSoFar = results.meta

        url_references = response.xpath(
            "//a[@class='tab-link' and contains(text(),'References')]//@href").extract_first()

        yield Request(url = url_references, meta=resultsSoFar, callback=parseReferences)

    def parseReferences(self, response):
        resultsSoFar = results.meta

        url_friends = response.xpath(
            "//a[@class='tab-link' and contains(text(),'Friends')]//@href").extract()

        yield Request(url=url_friends, meta=resultsSoFar, callback=parseFriends)

    def parseFriends(self, response):
        resultsSoFar = results.meta

        item = SofaridersItem()
        item['responseRate'] = []
        item['user_url'] =  resultsSoFar['user_url'] # Assigned
        item['lastLogin'] =  resultsSoFar['lastLogin']# Assigned
        item['couchStatus'] =  resultsSoFar['couchStatus']# Assigned
        item['location'] = resultsSoFar['location'] # Assigned
        item['verificationStatus'] =  resultsSoFar['verificationStatus']# Assigned
        item['languages'] =  resultsSoFar['languages']# Assigned
        item['age'] =  resultsSoFar['age']# Assigned
        item['sex'] =  resultsSoFar['sex']# Assigned
        item['joinDate'] =  resultsSoFar['joinDate']# Assigned
        item['hometown'] =  resultsSoFar['hometown']# Assigned
        item['profileCompletion'] =  resultsSoFar['profileCompletion']# Assigned
        item['education'] = resultsSoFar['education'] # Assigned
        item['maxGuests'] = []
        item['preferredGender'] = []
        item['lastMinuteOkay'] = []
        item['refs_fromSurfers_pos'] = []
        item['refs_fromSurfers_neg'] = []
        item['refs_fromHosts_pos'] = []
        item['refs_fromHosts_neg'] = []
        item['friends'] = []
        yield item
