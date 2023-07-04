import http.client
import time
from functools import wraps

COUNT_IMAGES = 10
DOWNLOAD_URL = "cataas.com"


def timer(func):
    @wraps(func)
    def wrapper():
        start_time = time.time()
        retval = func()
        print("Total download time: " f"{str(time.time() - start_time)} secs")
        return retval

    return wrapper


def download_image(conn, image) -> None:
    conn.request("GET", "/cat")
    res = conn.getresponse()
    ext = res.headers.get("Content-Type").split("/")[1]

    write_image(res, image, ext)


def write_image(res, image, ext) -> None:
    with open(f"sync_images/image{image}.{ext}", "wb") as file:
        file.write(res.read())
        print(f"The image {image} is downloaded!")


@timer
def main() -> None:
    conn = http.client.HTTPSConnection(DOWNLOAD_URL)

    for image in range(1, COUNT_IMAGES + 1):
        download_image(conn, image)


if __name__ == "__main__":
    main()
