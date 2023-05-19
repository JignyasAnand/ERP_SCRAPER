import json

import scrapy

class ERPObj(scrapy.Spider):
    name="errps"
    start_urls=["https://newerp.kluniversity.in/index.php?r=site%2Findexindi"]

    headers={
        "Host": "newerp.kluniversity.in",
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '"Not:A-Brand";v="99", "Chromium";v="112"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "macOS",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://newerp.kluniversity.in/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close",
    }

    cookies = {"SERVERID": "erp",
               "PHPSESSID": "532rdiv8f75s2rd0nf1ohoh6j1",
               "_csrf": "bc06fa195a3e01e825b51cbbfa5e475b444448982fb0f6da298beb488bb70307a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22OgSGZ11uV2K133r8_zf3RRDl48sHzZZU%22%3B%7D"
               }



    def __init__(self, dets,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in dets:
            self.cookies[i]=dets[i]
        print(self.cookies)
        open("op.json", "w")

    def start_requests(self):
        for i in self.start_urls:
            yield scrapy.Request(i, headers=self.headers, cookies=self.cookies)

    def parse(self, response, **kwargs):
        # yield {
        #     "name":response.css(".text-center:nth-child(1) a::text")[0].extract().strip()
        # }

        yield scrapy.Request("https://newerp.kluniversity.in/index.php?r=studentinfo%2Fstudentendexamresult%2Fgetstudentinternalmarks", callback=self.temp)

    def temp(self, response, **kwargs):

        headers2={
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
            "DynamicModel[semester]":"2"
        }

        url1 = "https://newerp.kluniversity.in/index.php?r=studentinfo%2Fstudentendexamresult%2Fgetstudentinternalmarks"

        yield scrapy.FormRequest(
            url=url1,
            method="POST",
            formdata=payload,
            body="_csrf=yrtPXZYEvktqJLruEPWf6C7pKBrk13Iz-hEy69DFl3yF3BwazDWPPjwW8d8jxu3QcZNOKbaFNl_OKUGjqp_NKQ%3D%3D&DynamicModel%5Bacademicyear%5D=14&DynamicModel%5Bsemester%5D=2",
            headers=headers2,
            cookies=self.cookies,
            callback=self.temp2
        )


    def temp2(self, response, **kwargs):
        print("+_+_"*100)

        table = response.css("table tbody tr")

        for i in table:
            print("++++++"*70)
            name=i.css("td::text")[-1].extract()
            tl={}
            if i.css("td a"):
                links = i.css('a::attr(href)').getall()
                texts = i.css('a::text').getall()
                for link, text in zip(links, texts):
                    # print(link)
                    yield response.follow(
                        url=link,
                        callback=self.temp3,
                        cb_kwargs={"sname": name},
                    )
                break
            break
                # print("<>"*50)
            # break

    def temp3(self, response,sname, **kwargs):
        print("<>*60")
        count=0
        text = response.css(".redflag::text")[0].extract().strip()
        for i in response.css("table thead tr th::text").getall():
            if "weighted" in i.lower():
                print("COUNT : ", count)
            count+=1
        marks = response.css(f"td:nth-child({count})::text").get()
        yield {
            "name":sname,
            "component":text,
            "awarded":marks
        }