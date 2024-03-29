import asyncio
from signal import SIGINT, SIGTERM

from SunGrowDataCollector.Program import Program
from SunGrowDataCollector.configuration import Configuration

import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


config = Configuration()


async def main():
    program = Program(config)
    try:
        await program.Start()
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        await program.Stop()

def startup():
    loop = asyncio.get_event_loop()
    main_task = asyncio.ensure_future(main())
    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, main_task.cancel)
    try:
        loop.run_until_complete(main_task)
    finally:
        loop.close()
        
if __name__ == "__main__":
    startup()