from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import discord
from discord.ext import commands

# Startet den Mini-Webserver, damit Render stabil bleibt
Thread(target=lambda: HTTPServer(('0.0.0.0', 10000), type('H', (BaseHTTPRequestHandler,), {'do_GET': lambda s: s.send_response(200) or s.end_headers()})).serve_forever(), daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Wichtig für Beitritte (Rolle + Willkommen)

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Erfolgreich eingeloggt als {bot.user.name}!')
    print('Der Bot ist ONLINE und vergibt jetzt Rollen und Begruessungen!')

@bot.event
async def on_member_join(member):
    # --- 1. AUTOMATISCHE ROLLENVERGABE ---
    # Deine eingetragene Rollen-ID
    ROLLEN_ID = 1553811748430155776  
    
    rolle = member.guild.get_role(ROLLEN_ID)
    if rolle:
        try:
            await member.add_roles(rolle)
            print(f"Rolle {rolle.name} erfolgreich an {member.name} vergeben.")
        except discord.Forbidden:
            print(f"Fehler: Der Bot darf die Rolle nicht vergeben! Ziehe die Rolle des Bots in Discord weiter nach oben!")
    else:
        print("Fehler: Die Rollen-ID konnte auf dem Server nicht gefunden werden.")

    # --- 2. DEINE NEUE BEGRÜSSUNGS-NACHRICHT ---
    willkommens_text = (
        f"Welcome {member.mention} to Portfolio Growth\n\n"
        f"Check out <#1548319472081969243> to get to know the community, "
        f"also feel free to send port to <#1548766513517830294> for others to look at and give their thoughts and opinions🤔\n\n"
        f"Disclaimer: This is not financial advice\n"
        f"🚫 Please be aware of scammers!"
    )

    # Dein Welcome-Kanal
    channel = bot.get_channel(1535388628707184760)
    if channel:
        await channel.send(willkommens_text)
        print(f"Erfolgreich Begruessung fuer {member.name} gepostet.")

@bot.command()
async def hallo(ctx):
    await ctx.send(f'Hallo {ctx.author.name}! Ich funktioniere!')

# Holt sich den geheimen Token sicher aus den Render-Einstellungen
bot.run(os.environ.get('DISCORD_TOKEN'))

