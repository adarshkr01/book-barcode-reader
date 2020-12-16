import cv2
import time
import requests
import numpy as np
import pyzbar.pyzbar as pyzbar
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

isbn = ''
cam = cv2.VideoCapture(0)
while True:
    _, frame = cam.read()

    decodedObjects = pyzbar.decode(frame)
    for obj in decodedObjects:
        isbn = obj.data

    cv2.imshow("Scan QR code", frame)

    key = cv2.waitKey(1)
    if isbn != "" or key == 27:
        break

cam.release()
cv2.destroyAllWindows()
print(isbn)
isbn = str(isbn)
URL = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + str(isbn[2:-1])
print(URL)

r = requests.get(url=URL)

data = r.json()

if(not data):
    print("Could not fetch data. Try again!")

else:
    title = data["items"][0]["volumeInfo"]["title"]
    print(title)
    authors = data["items"][0]["volumeInfo"]["authors"][0]
    publisher = data["items"][0]["volumeInfo"]["publisher"]
    publishedDate = data["items"][0]["volumeInfo"]["publishedDate"]
    desc = data["items"][0]["volumeInfo"]["description"]
    pageCount = data["items"][0]["volumeInfo"]["pageCount"]
    avgRating = data["items"][0]["volumeInfo"]["averageRating"]
    image = data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]

    file = open('result.html', 'w')
    file.write(
        f'<html><head><title>Book Details</title><link rel="stylesheet" href="style/style.css" /></head><body><div class="container"><h1>{title}</h1><h3>Author: {authors}</h3><p><img src="{image}" /></p><p><b>Publisher:</b> {publisher}</p><p><b>Published Date:</b> {publishedDate}</p><p><b>Description</b><br />{desc}</p><p><b>Page Count: </b>{pageCount}</p><p><b>Rating: </b>{avgRating}</p></div></body></html>')
    file.close()

    firefox_binary = FirefoxBinary(
        'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
    bot = webdriver.Firefox(firefox_binary=firefox_binary)
    bot.get('file:///C:/Users/ADARSH/Desktop/Project/result.html')
