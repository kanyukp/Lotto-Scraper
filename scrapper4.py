import requests
import re
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver

def parse(url):
    response = webdriver.Chrome(r"G:\VS projects\chromedriver_win32\chromedriver.exe")
    response.get(url)
    sourceCode = response.page_source
    return sourceCode

soup = BeautifulSoup(parse("https://www.njlottery.com/en-us/scratch-offs/01567.html"),'html.parser')

body = soup.find('tbody')

prize_amount=[]
for tr in body.find_all('tr'):
    for td in tr.find_all('td' , {'title' : 'Prize Amount'}):
        prize_amount.append(td.text)

prize_amount = [i[1:] for i in prize_amount]
prize_amount = [j.replace(",", "") for j in prize_amount]
print(prize_amount)

total_prizes=[]
for tr in body.find_all('tr'):
    for td in tr.find_all('td' , {'title' : 'Total Prizes'}):
        total_prizes.append(td.text)

total_prizes = [j.replace(",", "") for j in total_prizes]
print(total_prizes)

prizes_remaining=[]
for tr in body.find_all('tr'):
    for td in tr.find_all('td' , {'title' : 'PRIZES REMAINING'}):
        prizes_remaining.append(td.text)

prizes_remaining = [j.replace(",", "") for j in prizes_remaining]
print(prizes_remaining)

total_printed = body.find('td' , {'id':'totalTicketsPrinted'}).text
total_printed = total_printed.replace(",", "")

p_remain = 0
for i in prizes_remaining:
    p_remain = p_remain + int(i)

p_printed = 0
for i in total_prizes:
    p_printed = p_printed + int(i)

print("REMAINDER")
print(p_printed)
print(p_remain)

print(total_printed)

tix_remain = int(total_printed) - (p_printed - p_remain)
print(tix_remain)

start_expval = 0;
for a,b in zip(prize_amount,total_prizes):
    start_expval = start_expval + (int(a)*int(b)/int(total_printed))

print("Starting expected value")
print(start_expval)

current_expval = 0;
for a,b in zip(prize_amount,prizes_remaining):
    current_expval = current_expval + (int(a)*int(b)/int(tix_remain))


print("Current expected value")
print(current_expval)

   