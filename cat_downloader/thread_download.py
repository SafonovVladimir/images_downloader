import http.client
import threading
import time

COUNT_IMAGES = 1000
DOWNLOAD_SITE = "cataas.com"


def download_image(image) -> None:
    conn = http.client.HTTPSConnection(DOWNLOAD_SITE)
    conn.request("GET", "/cat")
    res = conn.getresponse()
    ext = res.headers.get("Content-Type").split("/")[1]

    write_image(res, image, ext)


def write_image(res, image, ext) -> None:
    with open(f"thread_images/image{image}.{ext}", "wb") as file:
        file.write(res.read())
        print(f"The image {image} is downloaded!")


def main() -> None:
    threads = list()
    start_time = time.time()

    for image in range(1, COUNT_IMAGES + 1):

        t1 = threading.Thread(target=download_image, args=(image,))
        t1.start()
        # time.sleep(0.05)

    for thread in threads:
        thread.join()

    time.sleep(1)
    print("Total download time: " f"{str(time.time() - start_time)}")


if __name__ == "__main__":
    main()
