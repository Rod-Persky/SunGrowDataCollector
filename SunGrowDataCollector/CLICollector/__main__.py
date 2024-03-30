import asyncio
from signal import SIGINT, SIGTERM

from SunGrowDataCollector.CLICollector.Program import Program
from SunGrowDataCollector.CLICollector.RootConfiguration import LoadConfigurationFromIniFile

import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

import argparse
parser = argparse.ArgumentParser(description='SunGrowDataCollector CLI Collector')
parser.add_argument('--config', type=str, help='Path to the configuration file', required=True)
args = parser.parse_args()

config = LoadConfigurationFromIniFile(args.config)


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