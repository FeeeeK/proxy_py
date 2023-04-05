from collectors import AbstractCollector
from parsers import RegexParser

import http_client


class Collector(AbstractCollector):
    __collector__ = True

    def __init__(self):
        super(Collector, self).__init__()
        self.processing_period = 1 * 60 * 60

    async def collect(self):
        url = "https://getfreeproxylists.blogspot.com/"
        html = await http_client.get_text(url=url)
        return RegexParser().parse(html)
