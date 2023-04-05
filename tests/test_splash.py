from lxml import etree

import http_client
import lxml.html
import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
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
                    splash:mouse_click(dimensions.x, dimensions.y)
                    return splash:html()
                end
                """
        url = "http://localhost:8050/render.html?timeout=10&url=http://proxydb.net/?protocol=http&protocol=https&anonlvl=2&anonlvl=3&anonlvl=4&country="
        first_element_from_prev_page = 'adwdawds'

        while True:
            html = await
            http_client.get_text(url)
            tree = lxml.html.fromstring(html)

            if first_element_from_prev_page != 'adwdawds':
                url = "http://localhost:8050/render.html?timeout=10&lua_source={}&url=http://proxydb.net/?protocol=http&protocol=https&anonlvl=2&anonlvl=3&anonlvl=4&country=".format(
                    _script
                )

            country_selector = tree.xpath("//table[@class[contains(., 'table')]]//td//abbr/text()")
            elements = tree.xpath("//table[@class[contains(., 'table')]]//td/text()")
            if elements[0] == first_element_from_prev_page:
                break
            # 11
            for i in range(0, len(elements) - 1, 11):
                if country_selector[i // 11 + 2].find("RU") != -1:
                    results.append("{}://{}".format(''.join(elements[i + 4].text.strip().split('\t')),
                                                    elements[i].strip()))
            # ul.pagination > button.btn-outline-secondary
            first_element_from_prev_page = elements[0]
        self.assertTrue(result)
        print(result)



if __name__ == '__main__':
    unittest.main()
