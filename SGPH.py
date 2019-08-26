#a script that download input of 2 years value and return csv of all SG public holiday dates
from bs4 import BeautifulSoup
import time
import requests
import csv


#https://www.timeanddate.com/holidays/singapore/2000?hol=1

print("Please provide the starting year")
start_year = input()
start_year = int(start_year)
print("Please provide the ending year")
end_year = input()
end_year = int(end_year)
#header list to make requests download more human than bot so site dont block scrap
headers = {'user-agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebkit/532.0 (KHTML, like Gecko) Chrome/4.0.201.1 Safari/532.0',}


with open("sgph.csv", "w", newline='') as writeFile:
    writer = csv.writer(writeFile)
    for year in range(start_year, end_year+1):
        year = str(year)
        #get starting url
        sgph = "https://www.timeanddate.com/holidays/singapore/" + year + "?hol=1"

        #parse html with bs4
        r = requests.get(sgph, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

        sgph_table = soup.find("table")
        sgph_table = sgph_table.findAll("tr", {"data-mask" : "1"})

        for item in sgph_table:
            date_only = item.find("th")
            date_only = date_only.get_text() + " " + year
            writer.writerow([date_only])

        time.sleep(10)

print("csv download completed")


