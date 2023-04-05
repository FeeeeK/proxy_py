from collectors import AbstractCollector, PagesCollector
from parsers import RegexParser

import http_client
import lxml.html


class Collector(AbstractCollector):
    __collector__ = True

    def __init__(self):
        super(Collector, self).__init__()
        self.processing_period = 30 * 60

    async def collect(self):
        result = []
        _backup_script = """
        function main(splash)
            local get_rect_mate = splash:jsfunc([[
                function () {
                    var btn = document.querySelector("ul.pagination > button.btn-outline-secondary").getClientRects()[0];
                    return {"x": btn.left, "y": btn.top}
                }
            ]])
            splash:set_viewport_full()
            splash:wait(0.1)
            local dimensions = get_rect_mate()
            if isempty(dimensions) then
                dimensions = {}
                dimensions["x"] = 0
                dimensions["y"] = 0
            end
            splash:mouse_click(dimensions.x, dimensions.y)
            splash:wait(0.5)
            return splash:html()
        end
        """

        _script = """
        function main(splash)
            local element = splash:select('ul.pagination > button.btn-outline-secondary')
            local bounds = element:bounds()
            assert(element:mouse_click{x=bounds.width/3, y=bounds.height/3})
            return splash:html()
        end
        """
        url = "http://localhost:8050/render.html?wait=2&filters=none&timeout=10&url=http://proxydb.net/?protocol=http&protocol=https&anonlvl=2&anonlvl=3&anonlvl=4&country="
        first_element_from_prev_page = 'adwdawds'

        while True:
            html = await http_client.get_text(url)
            tree = lxml.html.fromstring(html)

            if first_element_from_prev_page != 'adwdawds':
                url = "http://localhost:8050/render.html?wait=2&filters=none&timeout=10&lua_source={}&url=http://proxydb.net/?protocol=http&protocol=https&anonlvl=2&anonlvl=3&anonlvl=4&country=".format(
                    _script
                )
            country_selector = tree.xpath("//table[contains(@class, 'table')]//td[position() mod 11 = 3]//abbr/text()")
            elements = tree.xpath("//table[contains(@class, 'table')]//td[position() mod 11 = 1]/a/text()")
            proto = tree.xpath("//table[contains(@class, 'table')]//td[position() mod 11 = 5]/text()")
            # print(len(elements))
            # print(len(country_selector))
            if elements[0] == first_element_from_prev_page:
                # print("Broke cycle")
                break
            # 11
            for i in range(0, len(elements) - 1, 1):
                # if country_selector[i].find("RU") != -1:
                result.append("{}://{}".format(proto[i],
                                               ''.join(''.join(elements[i].strip().split('\t')).split('\n'))))
            # ul.pagination > button.btn-outline-secondary
            first_element_from_prev_page = elements[0]
        return result
