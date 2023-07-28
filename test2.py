import asyncio


async def coroutine1():
    ...


async def coroutine2():
    ...


async def main():
    # Запуск обоих корутин
    coroutines = await asyncio.gather(coroutine1(), coroutine2())
    print(type(coroutines))
    done, pending = await asyncio.wait([coroutine1(), coroutine2()])
    print(type(done))
    # for task in done:


# Обработка завершенных корутин

asyncio.run(main())
