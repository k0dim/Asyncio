import asyncio
import aiohttp

from config import sslcontext, url


async def get_sw_link(links: list | str = None, client_session: aiohttp.ClientSession = None):
    if isinstance(links, list):
        coros = [client_session.get(link, ssl=sslcontext) for link in links]
    elif isinstance(links, str):
        coros = [client_session.get(links, ssl=sslcontext)]
    
    http_responces = await asyncio.gather(*coros)
    json_coros = [http_responce.json() for http_responce in http_responces]
    
    return await asyncio.gather(*json_coros)


async def get_sw(id: int = None, 
                 client_session: aiohttp.ClientSession = None):
    async with client_session.get(url + f"{id}", ssl=sslcontext) as response:
        return await response.json()


async def get_paramas(client_session: aiohttp.ClientSession = None):
    async with client_session.get(url, ssl=sslcontext) as respones:
        return await respones.json()
