import json

import scrapy

class ERPObj(scrapy.Spider):
    name="erps"
    start_urls=["https://newerp.kluniversity.in/index.php?r=studentinfo%2Fstudentendexamresult%2Fgetstudentinternalmarks"]

    headers = {
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
        "Referer": "https://newerp.kluniversity.in/index.php?r=studentinfo%2Fstudentendexamresult%2Fgetstudentinternalmarks",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close",
    }

    cookies={"SERVERID": "123",
            "PHPSESSID": "123",
            "_csrf": "123"
             }



    def __init__(self,dets, uid="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(dets)
        for i in dets:
            self.cookies[i]=dets[i]
        self.uid = uid
        # print("Cookies : ",self.cookies)

    def start_requests(self):
        for i in self.start_urls:
            yield scrapy.Request(i, headers=self.headers, cookies=self.cookies)

    def parse(self, response, **kwargs):

        tl=[]
        el=[]
        for i in response.css('select[name="DynamicModel[academicyear]"] option::attr(value)').getall():
            tl.append(i)
        for i in response.css('#dynamicmodel-semester option::attr(value)').getall():
            el.append(i)
        csrf = response.xpath('//*[@id="w0"]/input/@value')[0].get().strip()
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

        url1 = "https://newerp.kluniversity.in/index.php?r=studentinfo%2Fstudentendexamresult%2Fgetstudentinternalmarks"

        yield scrapy.FormRequest(
            url=url1,
            method="POST",
            formdata=payload,
            body=f"_csrf={csrf}%3D%3D&DynamicModel%5Bacademicyear%5D=14&DynamicModel%5Bsemester%5D=2",
            headers=self.headers,
            cookies=self.cookies,
            callback=self.temp2
        )


    def temp2(self, response, **kwargs):

        table = response.css("table tbody tr")

        for i in table:
            name=i.css("td::text")[-1].extract()
            if i.css("td a"):
                links = i.css('a::attr(href)').getall()
                texts = i.css('a::text').getall()
                for link, text in zip(links, texts):
                    yield response.follow(
                        url=link,
                        callback=self.temp3,
                        cb_kwargs={"sname": name},
                    )
                break
            break

    def temp3(self, response,sname, **kwargs):
        count=0
        text = response.css(".redflag::text")[0].extract().strip()
        for i in response.css("table thead tr th::text").getall():
            if "weighted" in i.lower():
                # print("COUNT : ", count)
                count+=1
                break
            count+=1
        marks = response.css(f"td:nth-child({count})::text").get()
        yield {
            "uid":self.uid,
            "comps": {
                "name": sname,
                "component": text,
                "awarded": marks
            }
        }
        # yield {
        #     "uid":self.uid,
        #     "name":sname,
        #     "component":text,
        #     "awarded":marks
        # }