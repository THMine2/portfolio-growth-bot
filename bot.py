from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import discord
from discord.ext import commands

# --- VERBESSERTER WEBSERVER FÜR MONITORING (Verarbeitet GET und HEAD) ---
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot ist online!")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

# Startet den Server auf Port 10000 für Render
Thread(target=lambda: HTTPServer(('0.0.0.0', 10000), MyHandler).serve_forever(), daemon=True).start()

# --- BOT CONFIGURATION ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Wichtig für automatische Rollenvergabe & Begrüßung

bot = commands.Bot(command_prefix='!', intents=intents)

# --- BUTTONS FÜR DIE ROLLENVERGABE (Dauerhaft aktiv dank timeout=None) ---
class RoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # Button 1: Video News (Rot)
    @discord.ui.button(label="Video News", style=discord.ButtonStyle.red, custom_id="role_btn_video")
    async def video_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        VIDEO_ROLE_ID = 1557069406788649061  
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
        MARKET_ROLE_ID = 1557069290815885382  
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
    # Registriert die Buttons im internen Speicher des Bots, damit sie persistent bleiben
    bot.add_view(RoleView()) 
    print(f'Erfolgreich eingeloggt als {bot.user.name}!')
    print('Der Bot ist ONLINE und vergibt jetzt Rollen und Begruessungen!')

@bot.event
async def on_member_join(member):
    # --- 1. AUTOMATISCHE ROLLENVERGABE BEI RECHTSKRÄFTIGEM BEITRITT ---
    AUTOMATISCHE_ROLLEN_ID = 1553811748430155776  
    role = member.guild.get_role(AUTOMATISCHE_ROLLEN_ID)
    if role:
        try:
            await member.add_roles(role)
            print(f"Rolle {role.name} automatisch an {member.name} vergeben.")
        except discord.Forbidden:
            print("Fehler: Die Rolle des Bots steht in den Server-Einstellungen nicht hoch genug!")
    else:
        print("Fehler: Die automatische Willkommens-Rollen-ID wurde nicht gefunden.")

    # --- 2. DEINE NEUE WUNSCH-BEGRÜSSUNGSNACHRICHT ---
    willkommens_text = (
        f"Welcome {member.mention} to Portfolio Growth\n\n"
        f"Check out <#1553797862385651872> to level up!\n\n"
        f"Disclaimer: This is not financial advice\n"
        f"🚫 Please be aware of scammers!"
    )

    # ID deines Welcome-Kanals
    channel = bot.get_channel(1535388628707184760)
    if channel:
        await channel.send(willkommens_text)
        print(f"Erfolgreich Begruessungsnachricht fuer {member.name} gesendet.")

# --- ADMIN-BEFEHL FÜR DAS EINRICHTEN DER ROLLEN-BUTTONS ---
@bot.command()
@commands.has_permissions(administrator=True)
async def setup_ping_roles(ctx):
    beschreibung = (
        "If you'd like to stay up to date on all things trading from my YouTube uploads "
        "to market news, make sure to add your roles.\n\n"
        "**React to this message to get your roles!**"
    )
    embed = discord.Embed(description=beschreibung, color=discord.Color.from_rgb(47, 49, 54))
    
    # Sendet das schicke Embed mit den interaktiven Buttons darunter
    await ctx.send(embed=embed, view=RoleView())
    # Löscht deine "!setup_ping_roles" Nachricht aus dem Kanal für ein sauberes Bild
    await ctx.message.delete()

# ---KLEINER FUNKTIONSTEST-BEFEHL ---
@bot.command()
async def hallo(ctx):
    await ctx.send(f'Hallo {ctx.author.name}! Ich funktioniere einwandfrei!')

# Startet den Bot über die Umgebungsvariable von Render
bot.run(os.environ.get('DISCORD_TOKEN'))
