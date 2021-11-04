import os
import asyncpg
from discord.ext import commands
import datetime


async def fix_dupes(user):
    user_logs = await bot.db.fetch("""SELECT * FROM pray_logs WHERE username = $1""", user)
    prev_pray_timestamp = None
    dupes = []
    for pray in user_logs:
        if not prev_pray_timestamp:
            diff = prev_pray_timestamp - pray["timestamp"]
            if diff > datetime.timedelta(minutes=5):
                dupes.append(pray)
    print(dupes)


async def setup_db():
    bot.db = await asyncpg.create_pool(dsn=os.getenv("DATABASE_URL"), max_size=5, min_size=1)

prefix = os.getenv('PREFIX')
bot = commands.Bot(command_prefix=prefix)

# set up db
bot.loop.run_until_complete(setup_db())
print('database setup completed.')

# load cogs
cog_list = [f.replace('.py', '') for f in os.listdir('cogs') if f.endswith('.py')]
for cog in cog_list:
    bot.load_extension(f'cogs.{cog}')
    print(f'cog {cog} loaded')

@bot.command(name='fixdupes')
async def fix_dupes(ctx):
    await fix_dupes('aine')
bot.hdb = bot.get_cog('Database')
bot.run(os.getenv('TOKEN'))
