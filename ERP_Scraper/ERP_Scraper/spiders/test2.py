import scrapy

class SP(scrapy.Spider):
    name = "fsp"
    start_urls=["https://www.google.com"]

    def __init__(self, category="",uid="", **kwargs):
        self.basecat=category
        super().__init__()
        print("CAR",uid)
        self.uid = uid
    def parse(self, response, **kwargs):
        print(self.basecat)
        yield {
            "uid":self.uid,
            "name":"test101",
            "bcat":self.basecat
        }