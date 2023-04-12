import logging
from models import sessionmaker, ORM_MODEL, StarWars

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s : %(name)s : %(levelname)s : %(funcName)s : %(message)s")
logger = logging.getLogger("migrate")

async def migrate(list_json: list, cls: ORM_MODEL, session: sessionmaker):
    try:
        for json in list_json:
            orm_obj = cls(**json)
            session.add(orm_obj)
            await session.commit()
    except (TypeError) as err:
        logging.error(f"Возникло исключение {err}:\t{json}")

