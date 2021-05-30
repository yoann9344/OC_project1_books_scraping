import os
import asyncio
from pathlib import Path

from tqdm import tqdm

from .pages import Thing
from .factories import serializer_factory, storage_factory


class InterruptionHandler():
    interrupted = False

    # Link sigint to this method to handle interruptions
    # signal(SIGINT, InterruptionHandler.sigint)
    @classmethod
    def sigint(cls, *args, **kwargs):
        cls.interrupted = True

    @classmethod
    def check_interruption(cls, progress_bar):
        if cls.interrupted:
            progress_bar.refresh()
            print()
            print('Excution interrupted.')
            print('Do you want to exit ? [y]/n ', end='')
            answer = input()
            if answer in ('', 'y'):
                exit(0)
            else:
                progress_bar.reset()
                cls.interrupted = False
        return


class Scraper():
    def __init__(self, serializer_format, service_name):
        self.serializer = serializer_factory.create(serializer_format)
        self.storage = storage_factory.create(service_name)

    async def get_thing(self, thing_url, thing_name=None):
        thing = await Thing(thing_url, title=thing_name)
        info = thing.get_info()
        return info

    async def get_all_things_from_url_list(
        self,
        things_url,
        path: Path
    ):
        tasks = []
        for thing_url, thing_name in things_url:
            tasks.append(
                self.get_thing(thing_url, thing_name=thing_name))

        things_info = []
        progress_bar = tqdm(total=len(things_url))
        for task in asyncio.as_completed(tasks):
            info = await task
            things_info.append(info)
            progress_bar.update()
        # TODO to handle sigint, need to check if all tasks
        # are finished
        InterruptionHandler.check_interruption(progress_bar)

        things_info_serialized = self.serializer.serialize(
            things_info,
            headers=Thing.headers,
        )
        path_info = path / f'info.{self.serializer.extension}'
        self.storage.save(
            path=path_info,
            data=things_info_serialized,
        )
