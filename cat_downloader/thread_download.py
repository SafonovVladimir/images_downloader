import http.client
import threading
import time

from cat_downloader.sync_download import write_image, timer

COUNT_IMAGES = 10
DOWNLOAD_URL = "cataas.com"


def image_download(image) -> None:
    conn = http.client.HTTPSConnection(DOWNLOAD_URL)
    conn.request("GET", "/cat")
    res = conn.getresponse()
    ext = res.headers.get("Content-Type").split("/")[1]

    write_image(res, image, ext)


@timer
def main() -> None:
    threads = []

    for image in range(1, COUNT_IMAGES + 1):
        t = threading.Thread(target=image_download, args=(image,))
        threads.append(t)
        t.start()
        time.sleep(0.05)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
