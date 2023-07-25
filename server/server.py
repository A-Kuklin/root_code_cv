import os
import json
import asyncio
import asyncpg
from dotenv import load_dotenv
from pydantic import BaseModel


class DataEntry(BaseModel):
    plan: int
    fact: int


async def handle_client(reader, writer):
    # dsn = os.getenv('docker_db_url') if os.getenv('docker_flag') else os.getenv('db_url')
    conn = await asyncpg.connect(dsn=os.getenv('db_url'))

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id SERIAL PRIMARY KEY,
            datetime TIMESTAMPTZ NOT NULL,
            plan INT NOT NULL,
            fact INT NOT NULL
        )
    ''')

    addr = writer.get_extra_info('peername')
    print(f'Установлено соединение с клиентом: {addr[0]}:{addr[1]}', flush=True)
    try:
        while True:
            data = await reader.read(100)
            if not data:
                break

            entry = DataEntry.model_validate(json.loads(data.decode('utf-8')))
            await conn.execute(
                'INSERT INTO data (datetime, plan, fact) VALUES (NOW(), $1, $2)',
                entry.plan,
                entry.fact
            )

    except ConnectionError as e:
        print(f'Ошибка при получении данных от клиента: {str(e)}', flush=True)
    finally:
        writer.close()
        print(f'Соединение с клиентом {addr[0]}:{addr[1]} закрыто', flush=True)


async def data_listener():
    host = os.getenv('server_host', '127.0.0.1')
    port = os.getenv('server_port', 9000)
    server = await asyncio.start_server(handle_client, host, port)
    print(f'Сервер запущен на {host}:{port}', flush=True)

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    load_dotenv()
    print('start_server', flush=True)
    asyncio.run(data_listener())
