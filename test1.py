import time
import multiprocessing

start = time.perf_counter()


def please_sleep(n):
    print("Sleeping for {} seconds".format(n))
    time.sleep(n)
    print("Done Sleeping for {} seconds".format(n))


processes = []

for i in range(1, 3):
    p = multiprocessing.Process(target=please_sleep, args=[i])
    p.start()
    processes.append(p)

for p in processes:
    p.join()

finish = time.perf_counter()
print("Finished in {} seconds".format(finish - start))
