from deals import DealsCog
from discord.ext import commands
import discord, configparser, os, logging
from dotenv import load_dotenv

CONFIG = 'config.ini'
CONFIG_DISCORD = 'Discord'
CONFIG_DISCORD_SERVERS = 'servers'
CONFIG_DISCORD_CHANNELS = 'channels'
LOG_FILE = 'discord.log'
LOGGER = 'discord'
TOKEN = 'TOKEN'

# https://discordpy.readthedocs.io/en/stable/api.html

class DealsBot(commands.Bot):
    def __init__(self, servers, channels, logger, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.servers = servers
        self.channels = channels
        self.logger = logger
        self.allowed_channels = []

    async def on_ready(self):
        self.logger.info(f'Logged in as {self.user}')
        for guild in self.guilds:
            if guild.name in self.servers: # check if whitelisted server
                self.logger.info(f'Connected to server: {guild}')
                for channel in guild.channels:
                    for c in self.channels:
                        if c in channel.name: # check if whitelisted channel
                            if channel.type.name == 'text' or channel.type.name == 'news':
                                self.logger.info(f'Found channel for posting deals: {channel.name}')
                                await channel.send('Successfully connected!')
                                self.allowed_channels.append(channel)
                                break
        await self.add_cog(DealsCog(self))

def main ():
    logger = logging.getLogger(LOGGER)
    load_dotenv()
    config = configparser.ConfigParser()
    servers = []
    channels = []
    try:
        config.read(CONFIG)
        ss = config.get(CONFIG_DISCORD, CONFIG_DISCORD_SERVERS).split(',')
        for s in ss:
            servers.append(s.strip())
        cc = config.get(CONFIG_DISCORD, CONFIG_DISCORD_CHANNELS).split(',')
        for c in cc:
            channels.append(c.strip())
    except:
        logger.info('Failed to parse config.ini')
        exit(1)
    handler = logging.FileHandler(filename=LOG_FILE, encoding='utf-8', mode='a')
    allowed_mentions = discord.AllowedMentions(everyone=True)
    client = DealsBot(servers, channels, logger, intents=None, command_prefix='!', allowed_mentions=allowed_mentions)    
    client.run(os.getenv(TOKEN), log_handler=handler, log_level=logging.INFO)

if __name__ == "__main__":
    main()