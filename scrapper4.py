import requests
import re
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver

def parse(url):
    response = webdriver.Chrome(r"G:\VS projects\chromedriver_win32\chromedriver.exe")
    response.get(url)
    sleep(3)
    sourceCode = response.page_source
    return sourceCode

file = open('ticket_urls.txt' , 'r')
lines = file.readlines()
file.close()
for line in lines:
    soup = BeautifulSoup(parse(line),'html.parser')

    price = soup.find('div', {'class': 'ticket-price'})
    price = price.find('div', {'class' : 'h5'}).text
    price = price.strip()
    price = price[2:]
    price, sep, tail = price.partition('.')

    body = soup.find('tbody')

    prize_amount=[]
    for tr in body.find_all('tr'):
        for td in tr.find_all('td' , {'title' : 'Prize Amount'}):
            prize_amount.append(td.text)

    prize_amount = [i[1:] for i in prize_amount]
    prize_amount = [j.replace(",", "") for j in prize_amount]
    
    prize_amount[-1] = prize_amount[-1].casefold()

    #print("final prize")
    if prize_amount[-1][0] == 'r':
        prize_amount[-1] = price

    #print(prize_amount[-1])
    #print(prize_amount)

    total_prizes=[]
    for tr in body.find_all('tr'):
        for td in tr.find_all('td' , {'title' : 'Total Prizes'}):
            total_prizes.append(td.text)

    total_prizes = [j.replace(",", "") for j in total_prizes]
    #print(total_prizes)

    prizes_remaining=[]
    for tr in body.find_all('tr'):
        for td in tr.find_all('td' , {'title' : 'PRIZES REMAINING'}):
            prizes_remaining.append(td.text)

    prizes_remaining = [j.replace(",", "") for j in prizes_remaining]
    #print(prizes_remaining)

    total_printed = body.find('td' , {'id':'totalTicketsPrinted'}).text
    total_printed = total_printed.replace(",", "")

    p_remain = 0
    for i in prizes_remaining:
        p_remain = p_remain + int(i)

    p_printed = 0
    for i in total_prizes:
        p_printed = p_printed + int(i)

    #print("REMAINDER")
    #print(p_printed)
    #print(p_remain)

    #print(total_printed)
    
    p_difference = p_printed - p_remain

    ratio = p_remain / p_printed

    exp_left = int(total_printed) * ratio


    tix_remain = int(total_printed) - (p_printed - p_remain)
    #print(tix_remain)

    start_expval = 0;
    for a,b in zip(prize_amount,total_prizes):
        start_expval = start_expval + (int(a)*int(b)/int(total_printed))

    #print("Starting expected value")
    #print(start_expval)

    current_expval = 0;
    for a,b in zip(prize_amount,prizes_remaining):
        current_expval = current_expval + (int(a)*int(b)/int(exp_left))


    #print("Current estimated expected value")
    #print(current_expval)

    with open('ticket_expvals.txt', 'a') as f:
        f.write(str(start_expval))
        f.write('\n')
        f.write(str(current_expval))
        f.write('\n')



   