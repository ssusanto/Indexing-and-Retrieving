#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 14:52:35 2018

@author: sebastiansusanto
"""
from bs4 import BeautifulSoup as bs
import os
import nltk.stem.porter as porter

#Global Variables
key_dict = {}
count = 0

#Open the stopwords, strips it and returns a list of words
def stopwords():
    with open("stopwords.txt", "r", encoding = "utf-8") as file:
        stopwords_lst = [word.strip() for word in file]

    return stopwords_lst


def openFile(filename):
    global count
    #Create inverted index file
    with open(filename, "r", encoding = "utf-8") as html_doc:
        soup = bs(html_doc, "html.parser")
        #content of the HTML after being processed by beautiful soup
        body = soup.body
        text_format = body.get_text()


    text_list = text_format.split()

    cleansed_list = []

    for word in text_list:
        text = word.strip().lower()

        #Removing commented HTML that aren't filtered by split and strip
        #I assume that a letter with less than 14 to be a normal English word
        #Do not append words that are in stopwords
        if len(text) <= 14 and text not in stopwords_list:
            cleansed_list.append(text)

    #Stem each word
    stemmer = porter.PorterStemmer()
    stem_list = [stemmer.stem(word) for word in cleansed_list]

    #Add Keys into dictionary, with each value containing the filename, then the count of words
    for word in list(set(stem_list)):
        if word not in key_dict:
            key_dict[word] = []
        word_count = stem_list.count(word)
        key_dict[word].append([filename, word_count])


    #Create document index file: docs.dat

    #Obtaining the document length
    document_length = len(stem_list)
    document_title = soup.title.string

    with open(index_filename, "r", encoding = "utf-8") as file:
        content = file.readlines()

    html_link = content[count].strip()
    semicolon_index = html_link.find(":")
    html_link = html_link[semicolon_index:]


    with open("doc.dat", "a", encoding = "utf-8") as file:
        file.write("Document Length: "+str(document_length)+ "\n")
        file.write("Title of the Document: "+ document_title+ "\n")
        file.write("URL of the Document: "+ html_link+ "\n\n")

    count += 1



#main
stopwords_list = stopwords()

path = input("Please enter the path containing the crawled HTML pages to be parsed and indexed: ")
index_filename = input("Please enter the name of the file mapping page filenames to URLs: ")
os.chdir(path)

#Get only the files that has txt
files = []
item_list = os.listdir(path)
for file in item_list:
    if ".txt" in file:
        files.append(file)

#test = openFile("0.txt")

for file in files:
    openFile(file)

#Create the inverted index file, invindex.dat: For each term, this file records a list of documents that contain this term, as well as how many times the term appeared in each document
with open("invindex.dat", "w", encoding = "utf-8") as file:
    for item in key_dict.items():
        file.write(item[0]+": ")
        file.write(str(item[1]))
        file.write("\n\n")






#/Users/sebastiansusanto/Documents/info-i427/webCrawler/dfs