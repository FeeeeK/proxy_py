from models import db, CollectorState
from proxy_py import settings

import os
import asyncio
import importlib.util


collectors = {}

_collectors_dirs = settings.COLLECTORS_DIRS
if type(_collectors_dirs) is not list:
    _collectors_dirs = [_collectors_dirs]

for collectors_dir in _collectors_dirs:
    for root, dirs, files in os.walk(collectors_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                module_name = os.path.splitext(file_path)[0].replace('/', '.')
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                collector_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(collector_module)

                if hasattr(collector_module, "Collector"):
                    if hasattr(collector_module.Collector, "__collector__") \
                            and collector_module.Collector.__collector__:
                        collectors[module_name] = collector_module.Collector()


# init db

for module_name, Collector in collectors.items():
    try:
        asyncio.get_event_loop().run_until_complete(db.get(
            CollectorState.select().where(
                CollectorState.identifier == module_name
            )
        ))
    except CollectorState.DoesNotExist:
        asyncio.get_event_loop().run_until_complete(db.create(
            CollectorState,
            identifier=module_name,
            processing_period=Collector.processing_period,
            last_processing_time=0,
        ))


# def get_collector_state(module_name: str):
#     try:
#         collector_state = asyncio.get_event_loop().run_until_complete(db.get(
#             CollectorState.select().where(
#                 CollectorState.identifier == module_name
#             )
#         ))
#     except CollectorState.DoesNotExist:
#         raise CollectorNotFoundException()
#
#     return collector_state


def get_collector_of_module_name(module_name: str):
    if module_name not in collectors:
        raise CollectorNotFoundException(
            "Probably some collector exists in database but not in filesystem. "
            "module_name = {}".format(module_name)
        )

    return collectors[module_name]


async def load_collector(state: CollectorState):
    collector = get_collector_of_module_name(state.identifier)
    await collector.load_state(state)
    return collector


async def save_collector(state: CollectorState):
    collector = get_collector_of_module_name(state.identifier)
    await collector.save_state(state)
    await db.update(state)


class CollectorNotFoundException(BaseException):
    pass
