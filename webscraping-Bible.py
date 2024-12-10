import random
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request




#create a list of chapters -- choose random chapter number from lsit
chapters = list(range(1,22))

random_chapter = random.choice(chapters)

if random_chapter < 10:
    random_chapter = '0' + str(random_chapter)
else:
    random_chapter = str(random_chapter)

#construct a URL to access the specific chapter form the website
url = 'https://ebible.org/asv/JHN' + random_chapter + '.htm'

#setting "User-Agent Headers"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
req = Request(url, headers=headers)

webpage = urlopen(req).read()

#parsed with HTML
soup = BeautifulSoup(webpage, 'html.parser')

print(soup.title.text)

#find all div elements with the p class
page_verses = soup.findAll('div', class_='p')

#split the text by periods to separate individual verses 
for verses in page_verses:
    verse_list = verses.text.split('.')


#random verse excluding the last 5 verses
mychoice = random.choice(verse_list[:-4 ])

verse = f'Chapter: {random_chapter} Verse: {mychoice}'

print(verse)

import keys
from twilio.rest import Client

client = Client(keys.accountSID, keys.authToken)

TwilioNumber = '+18445540940'

mycellphone = '+13107952930'

textmessage = client.messages.create(to=mycellphone, from_=TwilioNumber, body=verse)
