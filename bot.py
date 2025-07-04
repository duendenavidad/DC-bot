import discord
from discord.ext import commands
import random

# Descripción del bot
description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

# Configuración de intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Inicialización del bot
bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
   """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def minus(ctx, left: int, right: int):

    await ctx.send(left - right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

@bot.command()
async def mem(ctx):
    """Sends a meme from a predefined folder."""
    with open('images/mem1.jpg', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command()
async def poll(ctx, question: str, *options):    #?poll <pregunta> <opción1> <opción2>
    """Creates a poll with up to 10 options."""
    if len(options) > 10:
        await ctx.send("You can only provide up to 10 options.")
        return

    if len(options) < 2:
        await ctx.send("You need to provide at least two options.")
        return

    poll_message = f"**{question}**\n\n"
    reactions = ['1⃣', '2⃣', '3⃣', '4⃣',
                 '5⃣', '6⃣', '7⃣', '8⃣',
                 '9⃣', '🔟']

    for i, option in enumerate(options):
        poll_message += f"{reactions[i]} {option}\n"

    message = await ctx.send(poll_message)

    for i in range(len(options)):
        await message.add_reaction(reactions[i])

@bot.command()
async def serverinfo(ctx):     #?serverinfo
    """Displays information about the server."""
    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name} Info", description="Server details", color=discord.Color.blue())
    embed.add_field(name="Owner", value=guild.owner, inline=True)
    embed.add_field(name="Member Count", value=guild.member_count, inline=True)
    embed.add_field(name="Created On", value=discord.utils.format_dt(guild.created_at), inline=True)
    embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)

bot.run('')
