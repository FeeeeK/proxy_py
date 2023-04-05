from checkers.base_checker import BaseChecker, CheckerResult
import aiohttp
from json.decoder import JSONDecodeError

# from proxy_py.settings import CRAWLER_MACHINE_IP, CRAWLER_PROXY_IP


class HTTPBinIPChecker(BaseChecker):
    def __init__(self, timeout=None):
        super(htpbin_ip_checker, self).__init__("http://httpbin.org/ip", timeout=timeout)

    # TODO could cause db errors because of "value,value" kind of possible return @line 22

    async def validate(self, response: aiohttp.ClientResponse, checker_result: CheckerResult) -> bool:
        try:
            json_result = await response.json(content_type=None)
        except JSONDecodeError:
            json_result = ""
        if response.status != 200:
            return False
        elif not json_result:
            return False
        elif 'origin' in json_result:
            CheckerResult.ipv4 = json_result['origin'] #if json_result['origin'].lower().find("unknown") != -1 \
                # else HTTPBinIPChecker.strip_if_multiple_detected(json_result['origin'])
            return True
        return True

    # @staticmethod
    # def strip_if_multiple_detected(ip_string):
    #     if CRAWLER_MACHINE_IP not in ip_string.split(",") and CRAWLER_MACHINE_PROXY not in ip_string.split(","):
    #         return ip_string[0] # TODO re-make
    #     return CRAWLER_MACHINE_IP + "," + CRAWLER_MACHINE_PROXY
