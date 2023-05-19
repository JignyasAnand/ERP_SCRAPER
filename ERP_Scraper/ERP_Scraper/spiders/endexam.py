import scrapy

class ERP_END(scrapy.Spider):
    name="ende"
    start_urls = ["https://newerp.kluniversity.in/index.php?r=studentinfo%2Fstudentendexamresult%2Fsemendresult"]
    headers2 = {
        "Host": "newerp.kluniversity.in",
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '"Not:A-Brand";v="99", "Chromium";v="112"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "macOS",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "https://newerp.kluniversity.in",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://newerp.kluniversity.in/index.php?r=studentinfo%2Fstudentendexamresult%2Fsemendresult",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close",
    }

    cookies={"SERVERID": "erp",
            "PHPSESSID": "ipab5tdfnhu55rm9vr4p16ult5",
            "_csrf": "5f6e00ec69603cf6767219adf15ccf604bd8598a74afa5cd8c09a30cb8928fe7a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22PsQXOimRjS50c3KZPDkvJxu7Pt70PfUK%22%3B%7D"
             }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # open("op2.json", "w")

    def start_requests(self):
        for i in self.start_urls:
            yield scrapy.Request(i, headers=self.headers2, cookies=self.cookies)

    def parse(self, response, **kwargs):

        # yield {
        #     "name": response.css(".redflag::text").get()
        # }

        # tl=[]
        # el=[]
        # for i in response.css('#dynamicmodel-academicyear option::attr(value)').getall():
        #     tl.append(i)
        # for i in response.css('#dynamicmodel-semester option::attr(value)').getall():
        #     el.append(i)
        csrf = response.xpath('//*[@id="studentconsolidatemarksreport"]/input/@value')[0].get().strip()
        # yield {
        #     "_csrf": csrf,
        #     "Academicyear":tl,
        #     "semester":el,
        # }

        payload={
            "_csrf":csrf,
            "DynamicModel[academicyear]":"14",
            "DynamicModel[semester]":"1"
        }

        url1 = "https://newerp.kluniversity.in/index.php?r=studentinfo%2Fstudentendexamresult%2Fsemendresult"

        yield scrapy.FormRequest(
            url=url1,
            method="POST",
            formdata=payload,
            body=f"_csrf={csrf}%3D%3D&DynamicModel%5Bacademicyear%5D=14&DynamicModel%5Bsemester%5D=2",
            headers=self.headers2,
            cookies=self.cookies,
            callback=self.temp2
        )

    def temp2(self, response, **kwargs):
        print("+_+_"*100)

        table = response.css("table tbody tr")

        for i in table:
            print("++++++"*70)
            # print(i.css("td::text").getall())
            sub_names=i.css("td:nth-child(5)::text").get()
            marks=i.css("td:nth-child(7)::text").get()
            yield {
                "sub":sub_names,
                "marks":marks
            }