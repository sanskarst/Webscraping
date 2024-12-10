# pip install requests (to be able to get HTML pages and load them into Python)
# pip install bs4 (for beautifulsoup - python tool to parse HTML)


from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

##############FOR MACS THAT HAVE CERTIFICATE ERRORS LOOK HERE################
## https://timonweb.com/tutorials/fixing-certificate_verify_failed-error-when-trying-requests_html-out-on-mac/

##############FOR PCs THAT HAVE CERTIFICATE ERRORS LOOK HERE################
## https://support.chainstack.com/hc/en-us/articles/9117198436249-Common-SSL-Issues-on-Python-and-How-to-Fix-it

############## ALTERNATIVELY IF PASSWORD IS AN ISSUE FOR MAC USERS ########################
##  > cd "/Applications/Python 3.6/"
##  > sudo "./Install Certificates.command"



url = 'https://www.worldometers.info/coronavirus/country/us'
# Request in case 404 Forbidden error
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

table_rows = soup.findAll("tr")

#deathratio = total death/total cases
#testratio = total test/population

state_death_ratio = ""
state_best_testing = ""
state_worst_testing = ""
highest_death_ratio = 0.0
best_test_ratio = 0.0
worst_test_ratio = 1000.0



for row in table_rows[2:53]:
    td = row.findAll("td")
    
    state = td[1].text
    totaldeaths = td[3].text
    totalcases = td[2].text
    death_ratio = int(totaldeaths.replace(',',''))/int(totalcases.replace(',',''))
    totaltest = td[10].text
    population = td[12].text
    testratio = int(totaltest.replace(',',''))/int(population.replace(',',''))
    #print(state)
    #print(f"Death Ratio: {death_ratio}%")
    #print(f"Test Ratio: {testratio}%")

    if death_ratio >highest_death_ratio:
        highest_death_ratio = death_ratio
        state_death_ratio = state

    if testratio > best_test_ratio:
        best_test_ratio = testratio
        state_best_testing = state

    if testratio < worst_test_ratio:
        worst_test_ratio = testratio
        state_worst_testing = state

print(f"State with highest death ratio is: {state_death_ratio}")
print(f"Death Ratio: {highest_death_ratio}")
print()
print(f"State with the best testing ratio is: {state_best_testing}")
print(f"Test Ratio: {best_test_ratio:.2%}")
print()
print()
print(f"State with the worst testing ratio is: {state_worst_testing}")
print(f"Test ratio: {worst_test_ratio:.2%}")
print()
