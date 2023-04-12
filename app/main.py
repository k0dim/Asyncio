import sys

import asyncio
import logging

from serializer import get_count, get_json
from models import init_models, close_db, get_session_maker
from migrate import migrate, StarWars

def gen_id(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]

async def sw_migration():

    lst = [i for i in range(1, int(await get_count("count")+1))]
    list_id = list(gen_id(lst, 10))
    logging.info("Сформирован список ID")

    count = 1
    for iter_list in list_id:
        coros = [get_json(id) for id in iter_list]
        results = await asyncio.gather(*coros)
        logging.info(f"Итерация {count} - {iter_list} - Данные получены")

        Session = get_session_maker()
        async with Session() as session:
            await migrate(results, StarWars, session)
        logging.info(f"Итерация {count} - Данные загружены")

        count += 1


async def main():
    await init_models()
    logging.info("Запуск БД")
    await sw_migration()
    logging.info("Конец миграции")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s : %(name)s : %(levelname)s : %(funcName)s : %(message)s")
    logger = logging.getLogger("migrate")

    asyncio.run(main())