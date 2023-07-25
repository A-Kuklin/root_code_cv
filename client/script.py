import os
import asyncio
import json
import random
from dotenv import load_dotenv


load_dotenv()
host = os.getenv('server_host', '127.0.0.1')
port = os.getenv('server_port', 9000)


async def send_data():
    while True:
        plan = random.randint(0, 100)
        fact = random.randint(0, 100)

        data = {
            'plan': plan,
            'fact': fact
        }

        json_data = json.dumps(data)

        reader, writer = await asyncio.open_connection(host, port)

        writer.write(json_data.encode())
        await writer.drain()

        writer.close()
        await writer.wait_closed()

        await asyncio.sleep(10)


async def main():
    print('start_client', flush=True)
    await asyncio.sleep(1)
    while True:
        try:
            await send_data()
        except KeyboardInterrupt:
            break


asyncio.run(main())
