import scrapy
from hz_rc_archive.items import HzRcArchiveItem
from hz_rc_archive.itemloaders import RcLoader


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
                self.logger.warning("无法从标题《%s》中提取申报人姓名", title)
                continue
            else:
                date, = rc.css("span").re(r'\[(.*)\]')
                link = rc.css("a").attrib["href"]
            cb_kwargs = dict(date=date)
            yield response.follow(link, callback=self.parse_detail, cb_kwargs=cb_kwargs)

        next_page = response.css("li a.pages_next").attrib["href"]
        next_page_url = response.urljoin(next_page)
        if response.url != next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_detail(self, response, date):
        content = response.css("div.articel-detail-con p:first-child")
        loader = RcLoader(item=HzRcArchiveItem(), selector=content)
        loader.add_css("name", "span:nth-child(1)::text")
        loader.add_value("date", date)
        loader.add_css("company", "span:nth-child(2)::text")
        loader.add_css("level", "span:nth-child(3)::text")
        loader.add_css("qualification", "span:nth-child(4)::text")
        loader.add_value("weblink", response.url)
        yield loader.load_item()
