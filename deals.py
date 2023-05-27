from discord.ext import tasks, commands
import asyncio, logging, psutil
from scrapers import Scrapers

class DealsCog(commands.Cog):
    def __init__(self, bot):
        self.logger = logging.getLogger('discord')
        self.bot = bot
        self.scrapers = Scrapers()
        self.scrape.start()

    def cog_unload(self):
        self.logger.info('DealsCog unloading')
        self.scrape.cancel()

    @tasks.loop(seconds=30)
    async def scrape(self):
        self.logger.info('DealsCog started')
        PROCNAME = "chromium"

        # self.logger.info(f"Checking proc")
        # for proc in psutil.process_iter():
        #     # check whether the process name matches
        #     if proc.name() == PROCNAME:
        #         self.logger.info(PROCNAME)
        #         proc.kill()

        self.logger.info(f"Checking proc")
        for proc in psutil.process_iter():
            # Check whether the process name matches
            if proc.name() == PROCNAME:
                self.logger.info(f"Terminating process: {proc.name()} (PID: {proc.pid})")
                proc.terminate()
        
        # try:
        #     adealsweden = self.scrapers.scrape_adealsweden()
        #     if self.scrapers.adealsweden_old:
        #         for channel in self.bot.allowed_channels:
        #             for adeal in adealsweden:
        #                 await channel.send(f'@everyone new deal from adealsweden.com\n{adeal.name}\n{adeal.price}\n{adeal.url}')
        #                 await asyncio.sleep(2)
        # except Exception as e:
        #     self.logger.error(f'Failed to scrape: adealsweden.com')
        #     self.logger.error(e)
        # try:
        #     swedroid = self.scrapers.scrape_swedroid()
        #     if self.scrapers.swedroid_old:
        #         for channel in self.bot.allowed_channels:
        #             for droid in swedroid:
        #                 url = droid.url.split('?')[0]
        #                 await channel.send(f'@everyone new deal from swedroid.se\n{url}')
        #                 await asyncio.sleep(2)
        # except Exception as e:
        #     self.logger.error(f'Failed to scrape: swedroid.se')
        #     self.logger.error(e)
        
        
        
        try:
            amazon = self.scrapers.scrape_amazon()
            if self.scrapers.amazon_old:
                for channel in self.bot.allowed_channels:
                    for amaz in amazon:
                        await channel.send(f'@everyone product on amazon.se\n{amaz.name}\n{amaz.price}\n{amaz.url}\n{amaz.hagglezon}')
                        await asyncio.sleep(3)
        except Exception as e:
            self.logger.error(f'Failed to scrape: amazon.se')
            self.logger.error(e)

    @scrape.before_loop
    async def before_printer(self):
        self.logger.info('DealsCog waiting...')
        await self.bot.wait_until_ready()