import discord
from discord.ext import commands
import asyncio
import youtube_dl

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command(name='ready')
@commands.has_permissions(manage_roles=True)
async def on_ready(ctx):
    print(f'Bot {bot.user.name} ready!')
    pass


@bot.command(name='join')
@commands.has_permissions(manage_roles=True)
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command(name='leave')
@commands.has_permissions(manage_roles=True)
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command(name='resume')
@commands.has_permissions(manage_roles=True)
async def resume(ctx):
    ctx.voice_client.resume()
    pass


@bot.command(name='mute', help='Mutes a user for a specified amount of minutes')
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, minutes: int, *, reason: str = 'No reason provided'):
    mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
    if not mute_role:
        mute_role = await ctx.guild.create_role(name='Muted')
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, send_messages=False, connect=False)

    await member.add_roles(mute_role)
    await ctx.send(f'{member.mention} has been muted for {minutes} minutes for reason: {reason}')

    await asyncio.sleep(minutes * 60)  # sleep for the specified amount of minutes
    await member.remove_roles(mute_role)
    await ctx.send(f'{member.mention} has been unmuted')


@bot.command(name='unmute', help='Unmutes a user')
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.remove_roles(mute_role)
    await ctx.send(f'{member.mention} has been unmuted')


@bot.command(name='play')
async def play(ctx, *, query):
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel!")
        return

    elif not ctx.guild.voice_client:
        await ctx.author.voice.channel.connect()

    url = f"ytsearch:{query}"
    player = discord.FFmpegPCMAudio(url)
    ctx.voice_client.play(player)


bot.run('')

