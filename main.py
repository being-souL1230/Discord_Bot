import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

role_name = "pydev"

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server, {member.name}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention}, please use proper language!")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}!")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    embed = discord.Embed(title=f"User Info - {member}", color=discord.Color.blue())
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Name", value=member.display_name, inline=True)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="Roles", value=len(member.roles), inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"Server Info - {guild.name}", color=discord.Color.green())
    embed.add_field(name="Owner", value=guild.owner, inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Created", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="Channels", value=f"{len(guild.text_channels)} Text, {len(guild.voice_channels)} Voice", inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

    await ctx.send(embed=embed)

@bot.command()
async def clear(ctx, amount: int = 5):
    if amount > 100:
        await ctx.send("You can only delete up to 100 messages at once!")
        return

    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Deleted {len(deleted)-1} messages!", delete_after=3)

@bot.command()
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    if ctx.author.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await ctx.send(f"{member} has been kicked! Reason: {reason}")
    else:
        await ctx.send("You don't have permission to kick members!")

@bot.command()
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    if ctx.author.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await ctx.send(f"{member} has been banned! Reason: {reason}")
    else:
        await ctx.send("You don't have permission to ban members!")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} has been assigned the {role_name} role.")
    else:
        await ctx.send("Role not found")

bot.run("Bot_Token")
