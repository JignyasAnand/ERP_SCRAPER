import scrapy

class SP(scrapy.Spider):
    name = "fsp"
    start_urls=["https://www.google.com"]

    def __init__(self, category="", **kwargs):
        self.basecat=category
        super().__init__()
    def parse(self, response, **kwargs):
        print(self.basecat)
        yield {
            "name":"test101",
            "bcat":self.basecat
        }