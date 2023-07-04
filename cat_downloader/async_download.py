from asyncio import tasks
import aiohttp
import asyncio
import aiofiles

from cat_downloader.sync_download import timer

COUNT_IMAGES = 10
DOWNLOAD_URL = "https://cataas.com"


async def image_download(session, image) -> None:
    async with session.get("/cat") as res:
        ext = res.headers.get("Content-Type").split("/")[1]

        await write_image(res, image, ext)


async def write_image(res, image, ext) -> None:
    async with aiofiles.open(f"async_images/image{image}.{ext}", "wb") as file:
        print(f"Starting download the image {image}..")
        await file.write(await res.read())
        print(f"The image {image} is downloaded!")


@timer
async def main() -> None:
    tasks = []

    async with aiohttp.ClientSession(DOWNLOAD_URL) as session:
        for image in range(1, COUNT_IMAGES + 1):
            task = asyncio.create_task(image_download(session, image))
            tasks.append(task)
            await asyncio.sleep(0.05)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
