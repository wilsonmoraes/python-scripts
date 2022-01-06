from uuid import uuid4

import aiohttp
import asyncio
import time
import datetime

start_time = time.time()


async def get_pokemon(session, url):
    async with session.post(
            url,
            json={
                "external_id": str(uuid4()),
                "amount": 10.00,
                "origin": "payment_link",
                "company_id": "999",
                "mcc_code": "333",
                "card": {
                    "card_token": "c2861cda-2f78-4f8b-b08f-931a0938fac6",
                    "security_code": "999",
                    "brand": "visa",
                },
            },
            headers={
                "internal-authentication": "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gVHJlcyIsImlhdCI6MTUxNjIzOTAyMn0.RQD8s5ITJnnzjTUnKGSD1qU31EvbgvdqzqWnhp8x_t98U1btxQKSWWsEx6BYiME2",
                "Content-Type": "application/json"
            },
    ) as resp:
        json = {} if resp.status == 201 else resp.reason
    return resp.status, json


async def main():
    async with aiohttp.ClientSession() as session:

        tasks = []
        success = 0
        errors = 0
        for number in range(0, 5000):
            url = 'https://pp-payments-api-dev.pedepronto.com.br/v2/transactions/'
            tasks.append(asyncio.ensure_future(get_pokemon(session, url)))

        original_pokemon = await asyncio.gather(*tasks)
        for pokemon in original_pokemon:
            if pokemon[0] == 201:
                success = success + 1
            else:
                errors = errors + 1
                print(f"error:{pokemon[1]}")
        print(f"success:{success}, errors:{errors}")


asyncio.run(main())
print(f"{str(datetime.timedelta(seconds=(time.time() - start_time)))} seconds")
