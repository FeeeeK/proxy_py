import uvloop
import argparse
import asyncio
import importlib
import sys
import http_client
import traceback

from collectors.web.com.ditatompel.collector import Collector as DitaCollector
from collectors.web.com.nntime.collector import Collector as NNtimeCollector
from collectors.web.name.hidemy.collector import Collector as HideMyNameCollector
from collectors.web.net.proxydb.collector import Collector as ProxyDBCollector
# from collectors.web.top.kabak.collector import Collector as KabakCollector


uvloop.install()
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--collector', action='store', dest='collector', help='Path to collector')
args = parser.parse_args()
collector = globals()[args.collector]()
print(collector)


async def main():
    try:
        res = await collector.process_page(1)
        res = await collector.process_page(2)
        print(res)
        print(len(res))
    except AttributeError:
        try:
            res = await collector.collect()
            print(res)
            print(len(res))
        except Exception:
            traceback.print_exc()
            await http_client.HttpClient.clean()
    except Exception:
        traceback.print_exc()
        await http_client.HttpClient.clean()
    await http_client.HttpClient.clean()


asyncio.run(main())
