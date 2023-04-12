import aiohttp
import asyncio
import logging

from api import get_sw_link, get_sw, get_paramas

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s : %(name)s : %(levelname)s : %(funcName)s : %(message)s")
logger = logging.getLogger("migrate")

async def parser(parament: str = None, 
                       json_data: dict = None, 
                       client_session: aiohttp.ClientSession = None) ->list:
    parament_links = json_data.get(parament, [])
    parament_coro = get_sw_link(parament_links, client_session)
    fields = await asyncio.gather(parament_coro)
    parament = fields
    return parament[0]


async def get_json(sw_params: int = None):
    async with aiohttp.ClientSession() as client_session:
        try:
            json_data = await get_sw(sw_params, client_session)

            json_data['films'] = ', '.join([film["title"] for film in await parser('films', json_data, client_session)])
            json_data['homeworld'] = ', '.join([home["name"] for home in await parser('homeworld', json_data, client_session)])
            json_data['species'] = ', '.join([specie["classification"] for specie in await parser('species', json_data, client_session)])
            
            json_data['starships'] = ', '.join([specie["name"] for specie in await parser('starships', json_data, client_session)])
            json_data['vehicles'] = ', '.join([specie["name"] for specie in await parser('vehicles', json_data, client_session)])

            del json_data['created']
            del json_data['edited']
        except (KeyError) as err:
            logging.error(f"Возникло исключение {err}:\t{json_data}")

    return json_data


async def get_count(params: str):
    async with aiohttp.ClientSession() as client_session:
        json_data = await get_paramas(client_session)
        return json_data[params]