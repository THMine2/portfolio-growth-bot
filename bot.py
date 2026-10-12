from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import discord
from discord.ext import commands

# Startet den Mini-Webserver für das Monitoring
Thread(target=lambda: HTTPServer(('0.0.0.0', 10000), type('H', (BaseHTTPRequestHandler,), {'do_GET': lambda s: s.send_response(200) or s.end_headers()})).serve_forever(), daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Wichtig für Beitritte (Rolle + Willkommen)

bot = commands.Bot(command_prefix='!', intents=intents)

# --- BUTTONS FÜR DIE ROLLENVERGABE (Hier fest definiert, damit es nicht abstürzt) ---
class RoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

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
    bot.add_view(RoleView()) # Registriert die Buttons fehlerfrei
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
        except discord.Forbidden:
            print("Fehler: Bot-Rolle muss in Discord weiter nach oben gezogen werden!")

    # --- 2. DEINE NEUE GEWÜNSCHTE BEGRÜSSUNGS-NACHRICHT ---
    willkommens_text = (
        f"Welcome {member.mention} to Portfolio Growth\n\n"
        f"Check out <#1553797862385651872> to level up!\n\n"
        f"Disclaimer: This is not financial advice\n"
        f"🚫 Please be aware of scammers!"
    )

    channel = bot.get_channel(1535388628707184760)
    if channel:
        await channel.send(willkommens_text)

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_ping_roles(ctx):
    beschreibung = (
        "If you'd like to stay up to date on all things trading from my YouTube uploads "
        "to market news, make sure to add your roles.\n\n"
        "**React to this message to get your roles!**"
    )
    embed = discord.Embed(description=beschreibung, color=discord.Color.from_rgb(47, 49, 54))
    await ctx.send(embed=embed, view=RoleView())
    await ctx.message.delete()

@bot.command()
async def hallo(ctx):
    await ctx.send(f'Hallo {ctx.author.name}! Ich funktioniere!')

bot.run(os.environ.get('DISCORD_TOKEN'))

