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

# --- BUTTONS FÜR DIE ROLLENVERGABE MIT DEINEN IDS ---
class RoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # Kein Timeout, damit die Buttons dauerhaft funktionieren

    # Button 1: Video News (Rot)
    @discord.ui.button(label="Video News", style=discord.ButtonStyle.red, custom_id="role_btn_video")
    async def video_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        VIDEO_ROLE_ID = 1557069406788649061  # Deine ID für Video News
        role = interaction.guild.get_role(VIDEO_ROLE_ID)
        
        if not role:
            return await interaction.response.send_message("Fehler: Rolle wurde auf dem Server nicht gefunden.", ephemeral=True)
            
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"Dir wurde die Rolle **{role.name}** entfernt.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"Du hast die Rolle **{role.name}** erhalten!", ephemeral=True)

    # Button 2: Market News (Blau)
    @discord.ui.button(label="Market News", style=discord.ButtonStyle.blurple, custom_id="role_btn_market")
    async def market_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        MARKET_ROLE_ID = 1557069290815885382  # Deine ID für Market News
        role = interaction.guild.get_role(MARKET_ROLE_ID)
        
        if not role:
            return await interaction.response.send_message("Fehler: Rolle wurde auf dem Server nicht gefunden.", ephemeral=True)
            
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"Dir wurde die Rolle **{role.name}** entfernt.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"Du hast die Rolle **{role.name}** erhalten!", ephemeral=True)


@bot.event
async def on_ready():
    # Registriert die Buttons beim Bot-Start, damit sie auch nach einem Server-Neustart direkt wieder reagieren
    bot.add_view(RoleView())
    print(f'Erfolgreich eingeloggt als {bot.user.name}!')
    print('Der Bot ist ONLINE und vergibt jetzt Rollen und Begruessungen!')

@bot.event
async def on_member_join(member):
    # --- 1. AUTOMATISCHE ROLLENVERGABE ---
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

    channel = bot.get_channel(1535388628707184760)
    if channel:
        await channel.send(willkommens_text)
        print(f"Erfolgreich Begruessung fuer {member.name} gepostet.")


# --- ADMIN-BEFEHL ZUM SENDEN DER BUTTON-NACHRICHT ---
@bot.command()
@commands.has_permissions(administrator=True) # Nur Admins dürfen diesen Befehl nutzen
async def setup_ping_roles(ctx):
    beschreibung = (
        "If you'd like to stay up to date on all things trading from my YouTube uploads "
        "to market news, make sure to add your roles.\n\n"
        "**React to this message to get your roles!**"
    )
    
    embed = discord.Embed(
        description=beschreibung,
        color=discord.Color.from_rgb(47, 49, 54) # Dunkles Discord-Design
    )
    
    # Sendet das Embed zusammen mit unserer Button-Ansicht
    await ctx.send(embed=embed, view=RoleView())
    # Löscht deine "!setup_ping_roles" Nachricht, damit der Kanal sauber bleibt
    await ctx.message.delete()


@bot.command()
async def hallo(ctx):
    await ctx.send(f'Hallo {ctx.author.name}! Ich funktioniere!')

# Holt sich den geheimen Token sicher aus den Render-Einstellungen
bot.run(os.environ.get('DISCORD_TOKEN'))

