from discord.ext import tasks, commands
import asyncio, logging
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

    @tasks.loop(seconds=5)
    async def scrape(self):
        self.logger.info('DealsCog started')
        try:
            adealsweden = self.scrapers.scrape_adealsweden()
            if self.scrapers.adealsweden_old:
                for channel in self.bot.allowed_channels:
                    for adeal in adealsweden:
                        await channel.send(content=f'@everyone new deal from adealsweden.com\n{adeal.name}\n{adeal.price}\n{adeal.url}')
                        await asyncio.sleep(2)
        except:
            self.logger.error(f'Failed to scrape: adealsweden.com')
        try:
            swedroid = self.scrapers.scrape_swedroid()
            if self.scrapers.swedroid_old:
                for channel in self.bot.allowed_channels:
                    for droid in swedroid:
                        url = droid.url.split('?')[0]
                        await channel.send(content=f'@everyone new deal from swedroid.se\n{url}')
                        await asyncio.sleep(2)
        except:
            self.logger.error(f'Failed to scrape: swedroid.se')
        try:
            amazon = self.scrapers.scrape_amazon()
            if self.scrapers.amazon_old:
                for channel in self.bot.allowed_channels:
                    for amaz in amazon:
                        print(amaz.url)
                        await channel.send(content=f'@everyone product on amazon.se\n{amaz.name}\n{amaz.price}\n{amaz.url}')
                        await asyncio.sleep(2)
        except:
            self.logger.error(f'Failed to scrape: amazon.se')

    @scrape.before_loop
    async def before_printer(self):
        self.logger.info('DealsCog waiting...')
        await self.bot.wait_until_ready()