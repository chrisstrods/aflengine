#!/usr/bin/env python3
## -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 20:54:07 2018

@author: chrisstrods

This script downloads all of the HTML files from AFLtable and
Footywire from within the given parameters, in order to be scraped
"""

from bs4 import BeautifulSoup
from os.path import dirname, abspath
import urllib, os, json
import sys

# startyear - earliest year to get
# endyear - lastest year to get
def getPageNames(startyear, endyear):  # Gets JSON list of URLS
    base = 'https://afltables.com/afl/seas/'
    end = ".html"
    matchlist = dict()
    year = endyear
    d = dirname(dirname(abspath(__file__)))

    # make a list of all the years
    n = startyear
    years = list()
    while (n <= endyear):
        years.append(n)
        n += 1

    # delete any years we are redownloading
    try:
        with open(d + "/matchfiles/afltables/matchlist.json", 'r') as datafile:
            data = json.load(datafile)
            for n in years:
                try:
                    if data[str(n)]:
                        data.pop(str(n))
                except KeyError:
                    pass
            with open(d + "/matchfiles/afltables/matchlist.json", 'a') as datafile:
                json.dump(data, datafile)
    except (FileNotFoundError, IOError):
        pass

    # loops backwards from endyear to startyear
    while (year >= startyear):
        url = base + str(year) + end

        # get page containing all match links in the season
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')

        matches = list()

        # Get all links on the page
        for a in soup.findAll('a', href=True):

            # If link text is 'match stats' then it links to a game, so
            # record that URL in the list
            if (a.text == "Match stats"):
                matchstring = "https://afltables.com/afl/" + str(a['href'])[3:]
                matches.append(matchstring)
                matchlist.update({year: matches})
        sys.stdout.write("\rSuccessfully downloaded match codes for " + str(year) + " season")
        year -= 1

    # When all seasons are done, output to JSON list
    with open(d + "/matchfiles/afltables/matchlist.json", 'w') as fout:
        json.dump(matchlist, fout)

    return matchlist


# Get main match files from JSON list and store the html files in fodler
def getPages(syear, eyear):
    d = dirname(dirname(abspath(__file__)))

    # load list from JSON file
    with open(d + "/matchfiles/afltables/matchlist.json", 'r') as fin:
        data = json.load(fin)

    # Iterate through each year in the list
    for year, mlist in data.items():
        # print("Downloading " + str(year) + " season")
        # Create folder for that year if it doesn't exist
        if not os.path.exists(d + "/matchfiles/afltables/" + year):
            os.makedirs(d + "/matchfiles/afltables/" + year)
        # Iterate through each match in the year

        for matchurl in mlist:
            code = str(matchurl).rpartition('/')[2]
            if not os.path.exists(d + "/matchfiles/afltables/" + year + "/" + code):
                urllib.request.urlretrieve(matchurl,
                                           d + "/matchfiles/afltables/" + year + "/" + code)
                sys.stdout.write("Successfully downloaded matches for " + str(year) + " season\r")
            # else:
            #    print("Match: " + code + " already exists. Skipping")


# get the pages with odds and fantasy data from footywire
def getExtraPages(scode, ecode):
    d = dirname(dirname(abspath(__file__)))
    # print("Getting matches from " + str(scode) + " to " + str(ecode))
    if not os.path.exists(d + "/matchfiles/footywire/"):
        os.makedirs(d + "/matchfiles/footywire/")
    for t in range(scode, ecode + 1):
        errors = 0
        if (t > 9297 or t < 6370 and t != 6079 and t != 6162):
            try:
                url1 = 'http://www.footywire.com/afl/footy/ft_match_statistics?mid=' + str(t)
                url2 = 'http://www.footywire.com/afl/footy/ft_match_statistics?mid=' + str(t) + '&advv=Y'
                urllib.request.urlretrieve(url1,
                                           d + "/matchfiles/footywire/footywire" + str(t) + ".html")
                urllib.request.urlretrieve(url2,
                                           d + "/matchfiles/footywire_adv/footywire_adv" + str(t) + ".html")
                sys.stdout.write("Successfully downloaded match #" + str(t) + "\r")
            except IndexError:
                print("There was an index error with match #" + str(t))
                errors += 1
        else:
            sys.stdout.write("Skipping game #" + str(t) + "\r")
            continue
    print("There were " + str(errors) + " errors in the retrieval of extra data")


# If run from command line, takes year ranges as parameters, otherwise
# uses defaults
def main(syear, eyear, scode, ecode):
    # first game 2010 is 4961, don't go back any further as info
    # is redundant

    # 4961 - earliest game
    # 9512 - GF2017
    # 9648 - End Round 16 2018

    try:
        print("Getting list of URLS from AFLtables")
        getPageNames(syear, eyear)
    except Exception as e:
        print(e)
        print("There was an error getting list of URLS from\
               AFLtables, try checking that the year parameters are \
               valid, and that you are connected to the internet")
        return

    try:
        print("Download HTML files from AFLTables")
        getPages(syear, eyear)
    except:
        print("There was an error downloading file from AFLtables, \
               try checking that the year parameters are valid, and \
               that you are connected to the internet")
        return

    try:
        print("Download HTML files from Footywire")
        getExtraPages(scode, ecode)
    except:
        print("There was an error downloading files from Footywire, \
              try checking that the year parameters are valid, and \
              that you are connected to the internet")
        return

# main(2019,2019,9748,9756)
