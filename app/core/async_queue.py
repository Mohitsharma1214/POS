import asyncio

class AsyncQueue:
    def __init__(self, maxsize=10):
        self.queue = asyncio.Queue(maxsize=maxsize)

    async def put(self, item):
        await self.queue.put(item)

    async def get(self):
        return await self.queue.get()

    def qsize(self):
        return self.queue.qsize()
