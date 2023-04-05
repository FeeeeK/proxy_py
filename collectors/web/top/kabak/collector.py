from collectors import PagesCollector

import http_client
import lxml.html


class BaseKabakCollector(PagesCollector):
    def __init__(self, url):
        super(BaseKabakCollector, self).__init__()
        self.url = url
        self.processing_period = 2 * 60 * 60
        
    async def process_page(self, page_index):
        result = []
        if page_index > 0:
            self.url += f"?page={page_index}"

        resp = await http_client.get_text(url=self.url)
        tree = lxml.html.fromstring(resp)
        ips = [item for item in
               tree.xpath("//div[@class='tb-body']/div[@class='tb-tr']/div[contains(@class, 'ip')]/text()") if
               item != ' ']
        ports = tree.xpath("//div[@class='tb-body']/div[@class='tb-tr']/div[contains(@class, 'ip')]/em/text()")
        type_ = tree.xpath("//div[@class='tb-body']/div[@class='tb-tr']/div[contains(@class, 'type')]/text()")
        countries = tree.xpath("//div[@class='tb-body']/div[@class='tb-tr']/div[contains(@class, 'land')]/span/a/@href")

        for i in range(0, len(ports)-1, 1):
            result.append(f"{type_[i].strip().lower()}://{ips[i]}:{ports[i]}")
        return result


class Collector(BaseKabakCollector):
    __collector__ = True
    
    def __init__(self):
        super(Collector, self).__init__("https://kabak.top/free-proxy")
