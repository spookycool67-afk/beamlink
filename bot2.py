import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Ready")

@bot.command(name="444")
async def four_four_four(ctx):
    e = discord.Embed(
        title="444s #1",
        description="Loaded Sites:\n🟦🟦🟦🟦🟦⬛⬛⬛ 70%",
        color=0x00FFFF
    )
    e.set_image(url="https://cdn.discordapp.com/attachments/1541216461480271912/1541218341811781722/IMG_4545.png?ex=6a8ccaef&is=6a8b796f&hm=f044b7f64e76c49e029b9cf5856c8d433fe5306706ffca82a993714f70bcfbe8&")
    
    b = discord.ui.Button(label="DASHBOARD", style=discord.ButtonStyle.link, url="https://444-beamsite.netlify.app")
    v = discord.ui.View()
    v.add_item(b)
    
    await ctx.send(embed=e, view=v)

bot.run("YOUR_BOT_TOKEN_HERE")
