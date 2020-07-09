#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 18:43:10 2018

@author: chrisstrods
"""

try:
    from etl import download_matches as download
    from etl import scrape_at as get_main
    from etl import scrape_fw as get_extra
    from etl import process
    from etl import clean
except ModuleNotFoundError:
    import download_matches as download
    import scrape_at as get_main
    import scrape_fw as get_extra
    import process
    import clean

SYEAR = 2020
EYEAR = 2020
SCODE = 10182
ECODE = 10190


if __name__ == "__main__":
    print("1.GETTING DATAFILES")
    download.main(SYEAR, EYEAR, SCODE, ECODE)
    print("1.SUCCESSFULLY LOADED DATAFILES")
    print("2.SCRAPING AFLTABLES DATA")
    get_main.main(SYEAR, EYEAR)
    print("2.SUCCESSFULLY SCRAPED AFLTABLES DATA")
    print("3.SCRAPING FOOTYWIRE DATA")
    get_extra.main(SCODE, ECODE)
    print("3.SUCCESSFULLY SCRAPED FOOTYWIRE DATA")
    print("4.POST-PROCESSING SCRAPED DATA")
    process.main()
    print("4.SUCCESSFULLY POST-PROCESSED SCRAPED DATA")
    clean.main()
    print("5.STAGING FILE CLEANED")
    print("DATA IS NOW READY FOR ANALYSIS!")
