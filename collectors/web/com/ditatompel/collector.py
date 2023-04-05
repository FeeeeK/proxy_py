from collectors import AbstractCollector, PagesCollector
from parsers import RegexParser
import js2py
from lxml import etree
import dateparser

import http_client
import lxml.html
import re
import async_requests


class BaseDitaTompelCollector(PagesCollector):
    def __init__(self, url, pages_count):
        super(BaseDitaTompelCollector, self).__init__()
        self.url = url
        self.pages_count = pages_count
        self.processing_period = 1 * 60 * 60

    @staticmethod
    def parse_from_splash_page(tree):
        # TODO fix ip and port XPATHs
        ips = tree.xpath("//table[@id='proxyList']//tbody/tr/td[position() mod 6 = 1]/text()")
        ports = tree.xpath("//table[@id='proxyList']//tbody/tr/td[position() mod 6 = 1]/span/text()")
        type_ = tree.xpath(
            "//table[@id='proxyList']//tbody//a[contains(@href, 'https://www.ditatompel.com/proxy/type')]/text()"
        )
        country = tree.xpath(
            "//table[@id='proxyList']//tbody//a[contains(@href, 'https://www.ditatompel.com/proxy/country')]/text()"
        )

        return [str(type_[i] + "://" + ips[i] + ports[i]) for i in range(0, len(type_)-1, 1)] # if country[i] != 'RU'

    async def process_page(self, page_index):
        result = []
        if page_index > 0:
            self.url = "http://localhost:8050/render.html?wait=5&filters=none&timeout=15&url=https://www.ditatompel.com/proxy/anonymity/elite"

        resp = await http_client.get_text(url=self.url)
        print(resp)
        tree = lxml.html.fromstring(resp)
        result += self.parse_from_splash_page(tree)
        _script = """
                        local bounds = element:bounds()
                        assert(element:mouse_click{x=bounds.width/3, y=bounds.height/3})
                        return splash:html()
                    end"""
        # and then get every rest of 'em
        for i in range(2, 30, 1):
            # inserting a lua script into the thingie
            script = f"""
                function main(splash)
                    local element = splash:select('li.paginate_button > a.page-link[data-dt-idx="{i}"]')
                    """  # we need to know what page to go to
            url = self.url.split("url")[0] + script + _script + "url" + self.url.split("url")[1]
            # TODO what if there's no ith page?
            resp = await http_client.get_text(url=url)
            tree = lxml.html.fromstring(resp)

            result += self.parse_from_splash_page(tree)
        return result


class Collector(BaseDitaTompelCollector):
    __collector__ = True

    def __init__(self):
        super(Collector, self).__init__("http://localhost:8050/render.html?wait=5&filters=none&timeout=15&url=https://www.ditatompel.com/proxy/anonymity/anon", 2)
