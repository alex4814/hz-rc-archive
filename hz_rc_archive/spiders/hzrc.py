import scrapy


class HzrcSpider(scrapy.Spider):
    name = "hzrc"
    start_urls = [
        "https://rc.hzrs.hangzhou.gov.cn/articles/2.html"
    ]

    def parse(self, response, **kwargs):
        for rc in response.css("div.index-art-list01 ul li"):
            try:
                name, = rc.css("a::text").re(r'^关于(.*?)申报')
                date, = rc.css("span").re(r'\[(.*)\]')
                link = rc.css("a").attrib["href"]
            except ValueError:
                continue

            yield {
                "name": name,
                "date": date,
                "link": response.urljoin(link),
            }

        next_page = response.css("li a.pages_next").attrib["href"]
        next_page_url = response.urljoin(next_page)
        if response.url != next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)

