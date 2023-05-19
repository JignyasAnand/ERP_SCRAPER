import json
import requests
import crochet

import sqlite

crochet.setup()
from flask import Flask, render_template, jsonify, request, redirect, url_for
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
import time
from uuid import uuid4

from ERP_Scraper.ERP_Scraper.spiders.internals import ERPObj
from ERP_Scraper.ERP_Scraper.spiders.test2 import SP

application = Flask(__name__)

crawl_runner = CrawlerRunner()
dets = {}
sqlobj = sqlite.SQLOBJ()


@application.route("/getdata", methods=['POST'])
def getdata():
    data = request.get_json()
    session_id = str(uuid4())
    data["session_id"]=session_id

    requests.post(request.host_url[:-1] + url_for("scrape"), json=data)
    # print(dets[session_id], session_id)
    return jsonify({"session_id":session_id})


@application.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json()
    session_id = data.get('session_id')

    scrape_with_crochet(data)

    time.sleep(5)


    return jsonify({"name":"hey"})
    # return jsonify(output_data)

@application.route("/results/<var>", methods=["GET"])
def results(var):
    uid, top = var.split("|||")
    res = sqlobj.get(uid, top)
    sqlobj.delete(uid)
    return jsonify(res)

@crochet.run_in_reactor
def scrape_with_crochet(data):
    # print("Session",data)
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)

    eventual = crawl_runner.crawl(ERPObj, dets=data.get('cookies', {}), uid=data.get("session_id"))
    return eventual


def _crawler_result(item, response, spider):
    item = dict(item)
    # print("item",item)
    sqlobj.insert(item["uid"],item["comps"],"internals")



if __name__ == "__main__":
    application.run(debug=True)
