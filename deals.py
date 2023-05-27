from discord.ext import tasks, commands
import asyncio, logging, subprocess
from scrapers import Scrapers


def drop_caches():
    subprocess.run(['sudo', 'sh', '-c', 'echo 3 > /proc/sys/vm/drop_caches'])


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
            
        asyncio.create_task(drop_caches())

    @scrape.before_loop
    async def before_printer(self):
        self.logger.info('DealsCog waiting...')
        await self.bot.wait_until_ready()