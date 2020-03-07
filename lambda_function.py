import aiohttp
import asyncio

from aws_xray_sdk.core.async_context import AsyncContext
from aws_xray_sdk.core import xray_recorder

xray_recorder.configure(service='repro_xray_issue', context=AsyncContext())


@xray_recorder.capture_async('download_file')
async def download_file(url, session):
    async with session.get(url) as response:
        data = await response.read()
        print(response.status, len(data))


async def download_files():
    urls = [
        'https://file-examples.com/wp-content/uploads/2017/10/file_example_JPG_100kB.jpg',
        'https://file-examples.com/wp-content/uploads/2017/10/file_example_JPG_500kB.jpg',
        'https://file-examples.com/wp-content/uploads/2017/10/file_example_JPG_1MB.jpg',
        'https://file-examples.com/wp-content/uploads/2017/10/file_example_JPG_2500kB.jpg',
    ]
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.create_task(download_file(url, session)))
        for task in tasks:
            await task


def lambda_handler(event, context):
    asyncio.run(download_files())
    return {}
