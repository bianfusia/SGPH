#a script that download input of 2 years value and return csv of all SG public holiday dates
from bs4 import BeautifulSoup
import time
import requests
import csv


#https://www.timeanddate.com/holidays/singapore/2000?hol=1
while True:
    print("Please provide the starting year")
    start_year = input()
    if len(start_year) != 4:
        print("Invalid year. Please try again")
        continue
    start_year = int(start_year)
    print("Please provide the ending year")
    end_year = input()
    if len(end_year) != 4 or start_year > int(end_year):
        print("Invalid year. Please try again")
        continue
    end_year = int(end_year)
    break

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
            day_only = item.findAll("td")[0].get_text()
            name_only = item.findAll("td")[1].get_text()
            writer.writerow([date_only,day_only,name_only])

        time.sleep(10)


print("csv download completed")

with open("sgph.csv", 'r') as readFile:
    data = csv.reader(readFile)
    data_list = []
    single_entries = []
    counter = 0
    year_now = str(start_year) #insert start_year
    for row in data:
            data_list.append(row)

    for row in data_list:
        if row[0] not in single_entries:
            single_entries.append(row[0])
        else:
            texting = "a duplicate date found: " + row[0]
            print(texting)
            with open("sgph.csv", "a", newline='') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow([texting])

        if row[0][-4:] == year_now and row[1] != "Sunday":
            counter += 1
       
        if row[0][-4:] != year_now:
            if counter != 11:
                texting = "please validate this year as total PH is not 11 days: " + year_now
                print(texting)
                with open("sgph.csv", "a", newline='') as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerow([texting])
            if row[1] != "Sunday":
                counter = 1
            else:
                counter = 0
            year_now = row[0][-4:]

        if row == data_list[-1]:
            if counter != 11:
                texting = "please validate this year as total PH is not 11 days: " + year_now
                print(texting)
                with open("sgph.csv", "a", newline='') as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerow([texting])
