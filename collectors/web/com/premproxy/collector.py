import re

import async_requests
import lxml.html
from collectors.pages_collector import PagesCollector
from lxml import etree
import jsbeautifier.unpackers.packer as packer


class BaseCollectorPremProxyCom(PagesCollector):
    def __init__(self, url, pages_count):
        super(BaseCollectorPremProxyCom, self).__init__()
        self.url = url
        self.pages_count = pages_count
        self.dynamic_pages_count = False

    async def process_page(self, page_index):
        result = []
        url = self.url + "time-%02d.htm" % (page_index + 1)
        resp = await async_requests.get(url=url)
        html = resp.text
        tree = lxml.html.fromstring(html)
        elements = tree.xpath(".//td[starts-with(@data-label, 'IP:port')]")
        self.pages_count = len(
            tree.xpath(
                r'//*[@id="navbar"][1]/ul/li/a[not(contains(text(), "prev") or contains(text(), "next"))]'
            )
        )
        code_table_url = re.findall(r'script src="(/js(-socks)?/.+?\.js)', html)[0][0]

        code_table = (
            await async_requests.get(f"https://premproxy.com{code_table_url}")
        ).text

        if packer.detect(code_table):
            ports_code_table = {
                match[0]: match[1]
                for match in re.findall(
                    r"\$\('.([a-z0-9]+)'\)\.html\(([0-9]+)\)", packer.unpack(code_table)
                )
            }
        else:
            self.pages_count = page_index - 1
            self.current_page = 0
            return []
        for el in elements:
            element_html = str(etree.tostring(el))
            address, port = re.search(
                r"(?P<address>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\|(?P<port>[a-z0-9]+)",
                element_html,
            ).groups()
            try:
                port = ports_code_table[port]
            except KeyError as ex:
                raise Exception(
                    f"symbol is not present in code table: {str(ex)}. address: {address}"
                ) from ex

            proxy = f"{address}:{port}"
            result.append(proxy)

        return result


class Collector(BaseCollectorPremProxyCom):
    __collector__ = True

    def __init__(self):
        super(Collector, self).__init__("https://premproxy.com/list/", 2)


class CollectorSocksList(BaseCollectorPremProxyCom):
    __collector__ = True

    def __init__(self):
        super(CollectorSocksList, self).__init__("https://premproxy.com/socks-list/", 2)
