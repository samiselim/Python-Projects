## Author : Sami Abdelaziz Abdelhamid Ali Selim

import requests
from bs4 import BeautifulSoup
import csv
# date = '2023-09-30'
date = input("Please Enter Date in this format YYYY-MM-DD : ")
#Requesting Web-page 
page = requests.get(f"https://www.filgoal.com/matches/?date={date}")

def main(page):
    src = page.content    #byte code of this page 
    soup = BeautifulSoup(src , "lxml")  #Parsing The conent to HTML code using Parser lxml 
    championchips = soup.find_all("div",{'class':'mc-block'})
    
    
    championchips_titles = []
    teams_A = []
    teams_B = []
    match_time = []
    match_result_teamA = []
    match_result_teamB = []
    header = ['النتيحة' , 'موعد المباراة' , 'الفريق الثانى' , 'الفريق الاول' , 'البطولة']

    for champ in championchips[1:]:
        teams1 =champ.find_all("div" , {"class":"f"})
        teams2 =champ.find_all("div" , {"class":"s"})
        hours = champ.find_all('div' , {'class':'match-aux'})

        for team in teams1:
            championchips_titles.append(champ.contents[1].find("span").text.strip())
            teams_A.append(team.find("strong").text.strip())
            match_result_teamA.append(team.find("b").text.strip())
            
        for team in teams2:
            teams_B.append(team.find("strong").text.strip())
            match_result_teamB.append(team.find("b").text.strip())
        
        for i in range(len(hours)):
            match_time.append(hours[i].contents[len(hours[i])-2].text[14:].strip())   

    match_result = [f"{x} - {i}" for i,x in zip(match_result_teamA , match_result_teamB)]    

    match_details = {'النتيحة':match_result , 'موعد المباراة':match_time , 'الفريق الثانى':teams_B , 'الفريق الاول':teams_A , 'البطولة':championchips_titles}
    keys = match_details.keys()
    # print(keys)


    # ## Before Wrtiting Data we should concatinate results with each other using Zip function

    rows = [list(element) for element in zip(match_result , match_time , teams_B ,teams_A ,championchips_titles)]

   
   
    with open(f"Filgoal-Matchs-{date}.csv" ,mode = "w" ,newline='') as file:
        writer =csv.writer(file)
        writer.writerow(list(match_details.keys()))
        writer.writerows(rows)
    print(f"CSV file Filgoal-Match{date}' created successfully.")
main(page)