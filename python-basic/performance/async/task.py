import asyncio
async def hello():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

async def main():
    task1 = asyncio.create_task(hello())
    task2 = asyncio.create_task(hello())
    await task1
    await task2

asyncio.run(main())