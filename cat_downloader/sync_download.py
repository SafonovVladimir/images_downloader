import http.client
import time

COUNT_IMAGES = 1000
DOWNLOAD_SITE = "cataas.com"


def download_image(conn, image) -> None:
    conn.request("GET", "/cat")
    res = conn.getresponse()
    ext = res.headers.get("Content-Type").split("/")[1]

    write_image(res, image, ext)


def write_image(res, image, ext) -> None:
    with open(f"sync_images/image{image}.{ext}", "wb") as file:
        file.write(res.read())
        print(f"The image {image} is downloaded!")


def main() -> None:
    start_time = time.time()
    conn = http.client.HTTPSConnection(DOWNLOAD_SITE)

    for image in range(1, COUNT_IMAGES + 1):
        download_image(conn, image)

    print("Total download time: " f"{str(time.time() - start_time)}")


if __name__ == "__main__":
    main()
