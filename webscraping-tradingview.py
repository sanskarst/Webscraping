from urllib.request import urlopen, Request
from bs4 import BeautifulSoup




##############FOR MACS THAT HAVE ERRORS LOOK HERE################
## https://timonweb.com/tutorials/fixing-certificate_verify_failed-error-when-trying-requests_html-out-on-mac/

############## ALTERNATIVELY IF PASSWORD IS AN ISSUE FOR MAC USERS ########################
##  > cd "/Applications/Python 3.6/"
##  > sudo "./Install Certificates.command"


url = 'https://www.webull.com/quote/us/gainers/pre'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

		
req = Request(url, headers=headers)

webpage = urlopen(req).read()

soup = BeautifulSoup(webpage, 'html.parser')

print(soup.title.text)


#SOME USEFUL FUNCTIONS IN BEAUTIFULSOUP
#-----------------------------------------------#
# find(tag, attributes, recursive, text, keywords)
# findAll(tag, attributes, recursive, text, limit, keywords)

#Tags: find("h1","h2","h3", etc.)
#Attributes: find("span", {"class":{"green","red"}})
#Text: nameList = Objfind(text="the prince")
#Limit = find with limit of 1
#keyword: allText = Obj.find(id="title",class="text")

stock_data = soup.findAll('div',attrs={"class": "table-cell"})

print(stock_data[22])

for row in range(0,55,11):
    symboname = stock_data[row+1].text.replace('\n','')
    percentchange = stock_data[row+3].text.replace('\n','')
    lastprice = float(stock_data[row+4].text.replace('\n',''))
    percentcalc = float(percentchange.strip('%').strip('+'))
    currentprice = ((lastprice) * ((percentcalc)/100))+(lastprice)

    print(f"Name of stock: {symboname}")
    print(f"% Change in 1 Day: {percentchange}")
    print(f"Last Price: ${lastprice:.2f}")
    print(f"Current Price: ${currentprice:,.2f}")
    print()
    input()

