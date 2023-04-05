from collectors import AbstractCollector, PagesCollector
from parsers import RegexParser
import js2py
from lxml import etree
import dateparser

import http_client
import lxml.html
import re
import async_requests


class BaseNNTimeCollector(PagesCollector):
    def __init__(self, url):
        super(BaseNNTimeCollector, self).__init__()
        self.url = url

    async def process_page(self, page_index):
        result = []
        if page_index > 0:
            self.url += '%02d.htm' % (page_index + 1,)

        html = await http_client.get_text(url=self.url)
        tree = lxml.html.fromstring(html)
        try:
            elements = tree.xpath("//table[@class='data']//td[position() mod 6 = 1]")
            elements.pop(0)

            port_variables = tree.xpath("//script[text()[contains(., '=')]]/text()")[0].replace("\n", "")
            if port_variables[-1] == ";":
                port_variables = port_variables[:-1]
            port_variables = dict((k.strip(), int(v.strip())) for k,v in
                                  (item.split('=') for item in port_variables[:-1].split(';')))

            scripts = tree.xpath("//td/script/text()")
            # dates = tree.xpath("//td/dfn/text()")
            port_list = []

            for script in scripts:
                keys = script.replace('document.write(":"+', '').replace(")", "").split("+")
                port_list += ["".join(str(port_variables[key]) for key in keys)]

            for i in range(0, len(elements) - 1, 1):
                #if elements[i].find("Russian") == -1:
                results.append(f"{elements[i].text}:{port_list[i]}")

        except KeyError:
            pass
        except IndexError:
            pass
        return result


class Collector(BaseNNTimeCollector):
    __collector__ = True

    def __init__(self):
        super(Collector, self).__init__("http://nntime.com/proxy-list-")
