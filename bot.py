import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Wichtig für das Beitritts-Event

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Erfolgreich eingeloggt als {bot.user.name}!')
    print('Der Bot ist ONLINE und postet Begruessungen in den Welcome-Kanal!')

@bot.event
async def on_member_join(member):
    # Deine exakt formatierte Nachricht inklusive der Kanal-Verlinkung am Ende der Zeile
    willkommens_text = (
        f"Welcome {member.mention} to Portfolio Growth\n\n"
        f"📱 | To join VIP Head to <#1553797862385651872>\n\n"
        f"Disclaimer: This is not financial advice\n"
        f"🚫 Please be aware of scammers!"
    )

    # Deine eingetragene Kanal-ID für den Welcome-Kanal
    channel = bot.get_channel(1535388628707184760)
    
    if channel:
        await channel.send(willkommens_text)
        print(f"Erfolgreich Begruessung fuer {member.name} im Welcome-Kanal gepostet.")
    else:
        print("Fehler: Der Kanal konnte nicht gefunden werden. Ggf. fehlen dem Bot Leserechte.")

@bot.command()
async def hallo(ctx):
    await ctx.send(f'Hallo {ctx.author.name}! Ich funktioniere!')

# FÜGE HIER WIEDER DEINEN GEHEIMEN TOKEN EIN
bot.run('MTU1Mzc4OTcyOTA4OTAwMzU0MA.G66W2W._bc-e9DD_sFDkXcdgvNJVHaCpPUrJ9_cCa15YY')