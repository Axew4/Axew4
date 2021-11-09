import discord
import random
import wikipedia
import json

from discord.ext import commands, tasks
import pypokedex





client = commands.Bot(command_prefix='%')




@client.event
async def on_ready():
    print('ready')




@client.command()
async def pokedex(ctx, *, pkname):
    pk = pypokedex.get(name=pkname)
    em = discord.Embed(title=f'{pk.name}, {pk.dex}', colour=discord.Colour.red())
    em.add_field(name='Pokename types', value=pk.types)
    em.add_field(name='Pokemon height', value=pk.height)
    em.add_field(name='Pokemon weight', value=pk.weight)
    em.add_field(name='Attack', value=pk.base_stats.attack)
    em.add_field(name='Defence', value=pk.base_stats.defense)
    em.add_field(name='Speed', value=pk.base_stats.speed)
    em.add_field(name='HP', value=pk.base_stats.hp)
    em.add_field(name='Special Attack', value=pk.base_stats.sp_atk)
    em.add_field(name='Special Defence', value=pk.base_stats.sp_def)
    em.set_thumbnail(url='https://cdn.discordapp.com/emojis/778740634370179113.png?size=96')
    await ctx.send(embed=em)

@client.command()
async def wiki(ctx, *, research):
    wik = wikipedia.summary(research, 1)
    em = discord.Embed(title=research, description=wik, colour=discord.Colour.red())
    em.set_thumbnail(url='https://cdn.discordapp.com/emojis/652587786011934730.png?size=96')
    await ctx.send(embed=em)

@client.command()
async def server(ctx):
    server = ctx.guild
    em = discord.Embed(title='Some information about this server', colour=discord.Colour.red())
    em.add_field(name='Server name', value=server.name)
    em.add_field(name='Server ID', value=server.id)
    em.add_field(name='Server owner', value=server.owner)

    await ctx.send(embed=em)

@client.command()
async def join(ctx):
    guild = ctx.guild
    channel = discord.utils.get(ctx.guild.voice_channels, name='Music')

    if not channel:
        channel = await guild.create_voice_channel(name='Music')

    await channel.connect()
    await ctx.send('Connected to Music voice channel')

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
        await ctx.send("disconnected")
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@client.command()
async def create(ctx, channeltype, channelname):
    if channeltype == 'voice':
        await ctx.guild.create_voice_channel(name=channelname)
        em = discord.Embed(title='Created voice channel', description=f'Channel name = {channelname}', colour=discord.Colour.red())
        await ctx.send(embed=em)
    if channeltype == 'text':
        await ctx.guild.create_text_channel(name=channelname)
        em = discord.Embed(title='Created text channel', description=f'Channel name = {channelname}', colour=discord.Colour.red())
        await ctx.send(embed=em)
    if channeltype == 'role':
        await ctx.guild.create_role(name=channelname)
        em = discord.Embed(title='Created new role', description=f'Role name = {channelname}', colour=discord.Colour.red())
        await ctx.send(embed=em)




@client.command()
async def hello(ctx):
    user = ctx.author
    em = discord.Embed(title='Hello!', description=f'Hello, {user}', colour=discord.Colour.red())
    link = 'https://cdn.discordapp.com/emojis/778740635049000980.png?size=96'
    em.set_thumbnail(url=link)
    await ctx.send(embed=em)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason):
    await member.kick(reason=reason)
    em = discord.Embed(title=f'{member} kicked', description=f'because {reason}', colour=discord.Colour.red())
    em.set_thumbnail(url='https://cdn.discordapp.com/emojis/778740634999717928.png?size=96')
    await ctx.send(embed=em)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason):
    await member.ban(reason=reason)
    em = discord.Embed(title=f'{member} baned', description=f'because {reason}', colour=discord.Colour.red())
    em.set_thumbnail(url='https://cdn.discordapp.com/emojis/778740634999717928.png?size=96')
    await ctx.send(embed=em)

@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name='Muted')

    if not mutedRole:
        mutedRole = await guild.create_role(name='Muted')

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

    await member.add_roles(mutedRole, reason=reason)
    em = discord.Embed(title=f'{member} muted.', description=f'because {reason}', colour=discord.Colour.red())
    em.set_thumbnail(url='https://cdn.discordapp.com/emojis/685891247063433252.png?size=96')
    await ctx.send(embed=em)

@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')

    await member.remove_roles(mutedRole)
    em = discord.Embed(title=f'{member} unmuted', description=f'{member.mention}, Say thanks to {ctx.author.mention}', colour=discord.Colour.red())
    em.set_thumbnail(url='https://cdn.discordapp.com/emojis/778740634747666442.png?size=96')
    await ctx.send(embed=em)

@client.command()
async def flip(ctx):
    fliping = [
        'Head',
        'Tail',
    ]
    em = discord.Embed(title=f'Fliping a coin for {ctx.author}', description=random.choice(fliping), colour=discord.Colour.red())
    em.set_thumbnail(url='https://emoji.gg/assets/emoji/Coin.gif')
    await ctx.send(embed=em)

@client.command()
async def infomember(ctx, member: discord.Member=None):
    if member == None:
        em = discord.Embed(title=f'Useful information about {ctx.author}', colour=discord.Colour.red())
        em.add_field(name='Member name.', value=ctx.author)
        em.add_field(name='Member ID', value=ctx.author.id)
        em.add_field(name='Joined at',  value=ctx.author.joined_at)
        em.set_thumbnail(url='https://cdn.discordapp.com/emojis/775696490676224010.png?size=96')
        await ctx.send(embed=em)
    else:
        em = discord.Embed(title=f'Useful information about {member.mention}', colour=discord.Colour.red())
        em.add_field(name='Member name.', value=member.mention)
        em.add_field(name='Member ID', value=member.id)
        em.add_field(name='Joined at', value=member.joined_at)
        em.set_thumbnail(url='https://cdn.discordapp.com/emojis/775696490676224010.png?size=96')
        await ctx.send(embed=em)





@client.command()
async def repeatmessage(ctx, enabled='start', interval=10, *, message=''):
    if enabled.lower() == 'stop':
        messageInterval.stop()
        await ctx.send('repeatmessage off')
    elif enabled.lower() == 'start':
        messageInterval.change_interval(seconds=int(interval))
        messageInterval.start(ctx, message)
        em = discord.Embed(title=f'Spam started by {ctx.author}', colour=discord.Colour.red())
        em.add_field(name='Message', value=message)
        em.add_field(name='Time', value=f'every {interval} seconds')
        em.add_field(name='Stop', value='%repeatmessage stop')
        em.set_thumbnail(url='https://cdn.discordapp.com/emojis/778740634433486848.png?size=96')
        await ctx.send(embed=em)



@tasks.loop(seconds=10)
async def messageInterval(ctx, message):
    await ctx.send(message)

@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason):
    em = discord.Embed(title=f'{member} warned by {ctx.author}', description=f'reason = {reason}', colour=discord.Colour.red())
    em.set_thumbnail(url='https://cdn.discordapp.com/emojis/778740634999717928.png?size=96')
    await ctx.send(embed=em)
    await member.send(embed=em)

@client.command()
async def info(ctx):
    em = discord.Embed(title='Some useful innovations for axew4', colour=discord.Colour.red())
    em.add_field(name='Owner', value='axew&01#7614')
    em.add_field(name='Invite', value='<https://discord.com/api/oauth2/authorize?client_id=904737136765460561&permissions=536870911991&scope=bot>')
    em.add_field(name='Website', value='<https://sites.google.com/view/axew4/home>')
    em.add_field(name='version', value='0.2')
    em.set_thumbnail(url='https://cdn.discordapp.com/emojis/634009340461973565.png?size=96')
    await ctx.send(embed=em)




client.run(Choose your token)
