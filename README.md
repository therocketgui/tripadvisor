# tripadvisor

What it does:

> Scrape all pages of the feed page, getting 30 result per page (if 50 pages, 30*50 = 1500). 
> Goes to each restaurant page individually, click the website link to retrieve the domain url

> Results:

    "company": "Smokestak",
    "link": "https://www.tripadvisor.co.uk/Restaurant_Review-g186338-d11836064-Reviews-Smokestak-London_England.html",
    "info": {
        "phone": "+44 20 3873 1733",
        "address": "35 Sclater Street, London E1 6LB, England",
        "url": "https://smokestak.co.uk/"
    }

How to use:

> python3.6 tripadvisor.py https://www.tripadvisor.co.uk/Restaurants-g186338-c6-London_England.html
> data will be exported in json inside data.json

Warnings: Scraping data is not legal. This is only for practice purposes. You're responsible for whatever you do with this script...
