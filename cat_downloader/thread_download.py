import http.client
import threading
import time

COUNT_IMAGES = 1000
DOWNLOAD_URL = "cataas.com"


def image_download(image) -> None:
    conn = http.client.HTTPSConnection(DOWNLOAD_URL)
    conn.request("GET", "/cat")
    res = conn.getresponse()
    ext = res.headers.get("Content-Type").split("/")[1]

    write_image(res, image, ext)


def write_image(res, image, ext) -> None:
    with open(f"thread_images/image{image}.{ext}", "wb") as file:
        file.write(res.read())
        print(f"The image {image} is downloaded!")


def main() -> None:
    threads = []
    start_time = time.time()

    for image in range(1, COUNT_IMAGES + 1):
        t = threading.Thread(target=image_download, args=(image,))
        threads.append(t)
        t.start()
        time.sleep(0.05)

    for thread in threads:
        thread.join()

    print("Total download time: " f"{str(time.time() - start_time)}")


if __name__ == "__main__":
    main()
