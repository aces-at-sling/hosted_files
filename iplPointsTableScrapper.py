from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
import json

matches = []
wins = []
losses = []
tied = []
nr = []
pts = []
nrr = []
data = {}

data["type"] = "com.aces.iplapp.IplPointsTable"

page = requests.get("https://www.cricbuzz.com/cricket-series/5945/indian-premier-league-2023/points-table")

teamShortName = {"Mumbai Indians": "MI", "Royal Challengers Bangalore": "RCB", "Punjab Kings": "PBKS", "Rajasthan Royals": "RR", "Delhi Capitals": "DC", "Sunrisers Hyderabad": "SRH", "Chennai Super Kings":"CSK", "Kolkata Knight Riders": "KKR", "Lucknow Super Giants":"LSG", "Gujarat Titans":"GT"}

soup = BeautifulSoup(page.text)
#print(soup.prettify())

tbl = soup.find("table",class_="table cb-srs-pnts")
#print(tbl.prettify())

col_names = [x.get_text() for x in tbl.find_all(class_="cb-srs-pnts-th")]
total_cols = len(col_names)

team_names = [x.get_text() for x in tbl.find_all('td',class_="cb-srs-pnts-name")]

pnt_tbl = [x.get_text() for x in tbl.find_all('td',class_="cb-srs-pnts-td")]

np_pnt_tbl = (np.array(pnt_tbl)).reshape(len(team_names),7)

matches = map(int,np_pnt_tbl[:,0])
wins = map(int,np_pnt_tbl[:,1])
losses = map(int,np_pnt_tbl[:,2])
pts = map(int,np_pnt_tbl[:,5])
nrr = map(float,np_pnt_tbl[:,6])

arr = []

for i in range(len(matches)):
    temp = {}
    temp["teamName"] = teamShortName[str(team_names[i])]
    temp ["matches"] = matches[i]
    temp["wins"] = wins[i]
    temp["losses"] = losses[i]
    temp["totalPoints"] = pts[i]
    temp["netRunRate"] = nrr[i]
    print temp
    arr.append(temp)
data["PointsTable"] = arr
json_data = json.dumps(data)
file1 = open('iplPointsTable.json','w')
file1.write(json_data)
