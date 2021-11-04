import os
import asyncpg
from discord.ext import commands
import datetime


async def fix_dupes(user):
    user_logs = await bot.db.fetch("""SELECT * FROM pray_logs WHERE username = $1 ORDER BY timestamp DESC""", user)
    prev_pray_timestamp = None
    dupes = []
    for pray in user_logs:
        if prev_pray_timestamp:
            diff = prev_pray_timestamp - pray["timestamp"]
            if diff < datetime.timedelta(minutes=2):  # not 5 because theres lag
                dupes.append(pray["timestamp"])
        prev_pray_timestamp = pray["timestamp"]
    for timestamp in dupes:
        await bot.db.execute("""DELETE FROM pray_logs WHERE username = $1 AND timestamp = $2""", user, timestamp)
    print(user, len(dupes))


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
async def fix_dupes_but_not_the_real_one(ctx):
    if ctx.author.id == 656373241144934420:
        users = await bot.db.fetch("""SELECT username FROM users""")
        for user in users:
            await fix_dupes(user["username"])
bot.hdb = bot.get_cog('Database')
bot.run(os.getenv('TOKEN'))
