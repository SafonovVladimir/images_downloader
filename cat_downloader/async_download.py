from asyncio import tasks
import time
import aiohttp
import asyncio
import aiofiles

COUNT_IMAGES = 100
DOWNLOAD_SITE = "https://cataas.com"


async def image_download(session, image):

    async with session.get("/cat") as res:
        ext = res.headers.get("Content-Type").split("/")[1]


        async with aiofiles.open(f"async_images/image{image}.{ext}", "wb") as file:
            print(f"Starting download the image {image}..")
            await file.write(await res.read())
            print(f"The image {image} is downloaded!")


async def main():
    start_time = time.time()
    tasks = []

    async with aiohttp.ClientSession(DOWNLOAD_SITE) as session:
        for image in range(1, COUNT_IMAGES + 1):

            task = asyncio.create_task(image_download(session, image))
            tasks.append(task)
            await asyncio.sleep(0.05)

        await asyncio.gather(*tasks)

    print("Total download time: " f"{str(time.time() - start_time)}")


if __name__ == "__main__":
    asyncio.run(main())
