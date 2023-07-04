import http.client
import time

COUNT_IMAGES = 100
DOWNLOAD_SITE = "cataas.com"


def main():
    start_time = time.time()
    conn = http.client.HTTPSConnection(DOWNLOAD_SITE)

    for image in range(1, COUNT_IMAGES + 1):
        conn.request("GET", "/cat")
        res = conn.getresponse()
        ext = res.headers.get("Content-Type").split("/")[1]

        with open(f"sync_images/image{image}.{ext}", "wb") as file:
            file.write(res.read())
            print(f"The image {image} is downloaded!")

    print("Total download time: " f"{str(time.time() - start_time)}")


if __name__ == "__main__":
    main()
