import os
import asyncpg
from keep_alive import keep_alive
from discord.ext import commands
print("1")
async def setup_db():
  print(3)
  bot.db = await asyncpg.create_pool(dsn=os.getenv("DATABASE_URL"), max_size=5, min_size=1)
  print(4)

prefix = os.getenv('PREFIX')
bot = commands.Bot(command_prefix=prefix)
        
print(2)
# set up db
bot.loop.run_until_complete(setup_db())
print('database setup completed.')

# load cogs
cog_list = [f.replace('.py', '') for f in os.listdir('cogs') if f.endswith('.py')]
for cog in cog_list:
  bot.load_extension(f'cogs.{cog}')
  print(f'cog {cog} loaded')
  
bot.hdb = bot.get_cog('Database')
  
# keep_alive()
bot.run(os.getenv('TOKEN'))
