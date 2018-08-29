# Hospitality Exchange Profile Analysis

## Objective
Find out the problems with the community and why it's hard to find a host
## Info available
Current status, membership length, age, languages, hometown, profile completion, education, lots of unstructured profile information, home/couch details, references, friends.)
## Info unavailable
Private messages, request numbers and acceptances/denials.
## Questions
How many members are freeloaders? What traits correspond to reviews? How often is a bad review the last event? What proportion of reviews are bad? Where are the most frequent hosts located and where are the most frequent travelers from?

## Workflow:
1. Scrape each city's host results with scrapeSearchPages.py
2. Scrape total number of hosts in each city with scrapeSearchPages.py (quick, will be merged with scrapeSearchPages.py)
3. Scrape individuals' details from user profiles with Scrapy (in 'sofariders' directory, run "scrapy crawl sofariders_spider")
4. Load, merge, clean and analyze data with SofaRidersEDA.ipynb

### Use at your own risk. I will not take any responsibility for the use or misuse of these scripts. Scraping websites may not be permitted in your jurisdiction.
