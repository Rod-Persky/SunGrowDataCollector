import asyncio
import os
from signal import SIGINT, SIGTERM

from SunGrowDataCollector.CLICollector.Program import Program
from SunGrowDataCollector.CLICollector.RootConfiguration import LoadConfigurationFromIniFile

# Parse command line arguments
import argparse
parser = argparse.ArgumentParser(description='SunGrowDataCollector CLI Collector')
parser.add_argument('--config', type=str, help='Path to the configuration file', required=True)
parser.add_argument('--logconfig', type=str, help='Path to the log configuration file', required=False, default='logging.ini')
args = parser.parse_args()

# Configure logging
import logging.config
if os.path.exists(args.logconfig):
    logging.config.fileConfig(args.logconfig, disable_existing_loggers=True)
else:
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

# Load configuration from file
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