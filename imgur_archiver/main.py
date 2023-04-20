from .id import gen_id
from rich.table import Table
from rich.live import Live
from rich.align import Align
import httpx
import asyncio
import aiofiles
from rich.console import Console

def gen_table(data, width):
    table = Table(style='blue', width=width)

    table.add_column('URL')
    table.add_column('Status')
    table.add_column('Exists')

    for url, data in data.items():
        status = ''
        exists = ''

        # format status
        if data[0] == 0:
            status = '[aqua]Requesting'
        if data[0] == 1:
            status = '[blue]Requested'

        # format exists
        if data[1] == -1:
            exists = 'N/A'
        if data[1] == 0:
            exists = '[red]False'
        if data[1] == 1:
            exists = '[green]True'

        table.add_row(url, status, exists)

    return Align.center(table)

async def main():

    console = Console()
    width = console.width
    height = console.height

    table = {}

    # setup terminal live
    with Live(gen_table(table, width), refresh_per_second=60, screen=True) as live:

        # setup client
        async with httpx.AsyncClient() as client:

            # start download loop
            while True:

                # generate random id
                id = gen_id()
                url = f'https://i.imgur.com/{id}.png'

                # update table
                table[url] = (0, -1)
                live.update(gen_table(table, width))

                # send request to imgur
                res = await client.get(url)

                # update table
                table[url] = (1, -1)
                live.update(gen_table(table, width))

                # if the image doesn't exist, don't write it
                if len(res.content) == 0:
                    table[url] = (1, 0)
                    continue

                # update table
                table[url] = (1, 1)
                live.update(gen_table(table, width))

                # write the content
                async with aiofiles.open(f'{id}.png', 'wb') as file:
                    await file.write(res.content) 

                # file is closed after that due to `with`

                if len(table) >= height - 4:
                    table = {}
                    

def run():
    asyncio.run(main())
