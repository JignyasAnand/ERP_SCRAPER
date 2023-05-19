import json
import requests
import crochet
crochet.setup()
from flask import Flask, render_template, jsonify, request, redirect, url_for
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
import time

from ERP_Scraper.ERP_Scraper.spiders.internals import ERPObj

application = Flask(__name__)

crawl_runner = CrawlerRunner()
dets = {}


@application.route("/getdata", methods=['POST'])
def getdata():
    data = request.get_json()
    session_id = data.get('session_id')
    session_data = dets.get(session_id, {})
    session_data['cookies'] = data.get('cookies')
    dets[session_id] = session_data

    requests.post(request.host_url[:-1] + url_for("scrape"), json=data)
    return jsonify(data)


@application.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json()
    session_id = data.get('session_id')
    session_data = dets.get(session_id, {})
    session_data['output_data'] = []
    dets[session_id] = session_data

    scrape_with_crochet(session_id=session_id)

    time.sleep(5)

    output_data = session_data.get('output_data', [])


    del dets[session_id]
    # print(output_data)
    return jsonify(output_data)


@crochet.run_in_reactor
def scrape_with_crochet(session_id):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)

    session_data = dets.get(session_id, {})
    dets[session_id] = session_data

    eventual = crawl_runner.crawl(ERPObj, dets=session_data.get('cookies', {}))
    return eventual


def _crawler_result(item, response, spider):
    session_id = response.meta.get('session_id')
    session_data = dets.get(session_id, {})
    output_data = session_data.get('output_data', [])
    output_data.append(dict(item))
    session_data['output_data'] = output_data
    dets[session_id] = session_data


if __name__ == "__main__":
    application.run(debug=True)
