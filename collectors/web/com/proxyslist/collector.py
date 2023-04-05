from collectors import AbstractCollector, PagesCollector

import lxml.html
import http_client
import async_requests


class BaseProxylistsCollector(PagesCollector):
    def __init__(self, url):
        super(BaseProxylistsCollector, self).__init__()
        self.url = url

    async def process_page(self, page_index):
        result = []
        if page_index > 0:
            self.url += '%d' % (page_index + 1,)

        resp = await async_requests.get(url=self.url)
        html = resp.text
        tree = lxml.html.fromstring(html)
        ips = tree.xpath("//table[@id='proxy_list']//td[@class='left_td']/a[contains(@href, '/ip/')]/text()")
        countries = tree.xpath("//table[@id='proxy_list']//td[@class='left_td']/a[contains(@href, '/country/')]/text()")
        type_ = tree.xpath("//table[@id='proxy_list']//td[position() mod 8 = 7]/text()")
        transparency = tree.xpath("//table[@id='proxy_list']//td[position() mod 8 = 6]/text()")

        for i in range(0, len(countries), 1):
            if countries[i].find("Russia") == -1 and transparency[i] != 'Transparent':
                if type_[i].find("http") != -1:
                    result.append(f"http://{ips[i]}")
                else:
                    result.append(f"{type_[i].split(' ')[0].strip()}://{ips[i]}")
        return result


class Collector(BaseProxylistsCollector):
    __collector__ = True
    
    def __init__(self):
        super(Collector, self).__init__("http://proxyslist.com/page/")
