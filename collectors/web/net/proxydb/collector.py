# from collectors import PagesCollector
# from parsers import RegexParser

# import async_requests
# import lxml.html


# class ProxyDBCollector(PagesCollector):
#     async def process_page(self, page_index):
#         result = []
#         response = await async_requests.post(
#             url="https://proxydb.net/?" % (page_index * 64),
