# launcher.py'
import sys
from flask import Flask
import json
from ERP_Scraper.crawl import crawl


app = Flask(import_name="App1")


@app.route("/")
def scrape():
    event={}
    crawl(**event, spider_kwargs={"name22":"2222222"})


if __name__ == "__main__":
    app.run()
