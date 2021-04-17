import scrapy


class HzrcSpider(scrapy.Spider):
    name = "hzrc"
    start_urls = [
        "https://rc.hzrs.hangzhou.gov.cn/articles/2.html"
    ]

    def parse(self, response, **kwargs):
        for rc in response.css("div.index-art-list01 ul li"):
            try:
                name, *_ = rc.css("a::text").re(r'^关于(.*?)(申报|[被拟]认定)')
            except ValueError:
                title = rc.css("a::text").get()
                self.logger.warning("Failed to extract name from title: %s", title)
                continue
            else:
                date, = rc.css("span").re(r'\[(.*)\]')
                link = rc.css("a").attrib["href"]

            yield {
                "name": name,
                "date": date,
                "link": response.urljoin(link),
            }

        next_page = response.css("li a.pages_next").attrib["href"]
        next_page_url = response.urljoin(next_page)
        if response.url != next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)

