import discord
import dotenv
from discord.ext import commands
from discord.ui import Button, View
import os
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz  # Pour gérer le fuseau horaire
from keep_alive import keep_alive # Importez la fonction keep_alive
from discord import TextChannel

load_dotenv()
# Démarrer le serveur Flask
# Remplace par l'URL de ton bot sur Replit

url = "https://012d4050-113d-4cac-820a-0fe238cffdcd-00-ro1uaqbbv5u5.picard.replit.dev/"

# Choisir un fuseau horaire (par exemple UTC) timezone = pytz.timezone(UTC)
my_secret = os.environ['DISCORD_TOKEN']

CHANNEL_ID = 1298577064877883399

intents = discord.Intents.default()
intents.message_content = True      # Pour lire le contenu des messages
intents.members = True              # Pour détecter les membres (join/leave)
intents.guilds = True               # Pour accéder aux infos des serveurs
scheduler = AsyncIOScheduler()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1298577064877883395)  # Remplace par ton vrai ID de salon

    # Vérifie si le salon est un salon texte
    if isinstance(channel, TextChannel):
        # Si le salon est valide, on envoie le message
        await channel.send(
            f"👋 Bienvenue {member.mention} sur le serveur !\n"
        )
        await member.send(
        f"Salut ! Je suis un robot asiatique comme tu l'auras vu à ma photo , un bot conçu pour t'aider et maintenir l'ordre sur le serveur. 😊"
    )
    await member.send(
        f"👋 Bienvenue {member.mention} sur le serveur !\n"
        f"📜 N’oublie pas de lire les règles ci-dessous 👇"
    )

        # 2. Message avec les règles
    embed = discord.Embed(
        title="📜 RÈGLES DU SERVEUR",
        description="""
        **1. Respect total** — Pas d'insultes, propos haineux ou discriminatoires.
        **2. Pas de spam** — Évitez les messages inutiles ou répétés.
        **3. Pas de pub** — Les liens ou pubs sans autorisation sont interdits.
        **4. Canaux adaptés** — Utilisez les bons salons pour vos messages.
        **5. Pas de NSFW** — Contenu choquant/interdit = ban direct.
        **6. Suivre les ordres du staff** — Le staff a toujours le dernier mot.

        ⚠️ Enfreindre les règles peut entraîner un mute, un kick ou un ban.

        ✅ Cliquez sur le bouton ci-dessous pour accepter les règles.
        """,

        color=discord.Color.red()
    )
    embed.set_footer(text="Merci de lire les règles ! ❤️")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1298577064877883399/1359593110866231517/discord-bot-list-icon-filled-256.png?ex=67f80b41&is=67f6b9c1&hm=2eeab713683bde7bfe1533d31c8c7116203d5172a8f84b9a537a1cb65b3b2c42&")  # exemple de logo Discord
    # Crée un bouton
    bouton = Button(label="✅ J'accepte", style=discord.ButtonStyle.success)

    # Fonction appelée quand on clique sur le bouton
    async def bouton_callback(interaction):
        await interaction.response.send_message("Bienvenue sur le serveur ! 🎉", ephemeral=True)

    bouton.callback = bouton_callback

    # Affiche le bouton avec le message
    view = View()
    view.add_item(bouton)
    await member.send(embed=embed, view=view)
        
@bot.command()
async def règles(ctx):
    embed = discord.Embed(
        title="📜 RÈGLES DU SERVEUR",
        description="""
        **1. Respect total** — Pas d'insultes, propos haineux ou discriminatoires.
        **2. Pas de spam** — Évitez les messages inutiles ou répétés.
        **3. Pas de pub** — Les liens ou pubs sans autorisation sont interdits.
        **4. Canaux adaptés** — Utilisez les bons salons pour vos messages.
        **5. Pas de NSFW** — Contenu choquant/interdit = ban direct.
        **6. Suivre les ordres du staff** — Le staff a toujours le dernier mot.

        ⚠️ Enfreindre les règles peut entraîner un mute, un kick ou un ban.
        
        ✅ Cliquez sur le bouton ci-dessous pour accepter les règles.
        """,
        
        color=discord.Color.red()
    )
    embed.set_footer(text="Merci de lire les règles ! ❤️")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1298577064877883399/1359593110866231517/discord-bot-list-icon-filled-256.png?ex=67f80b41&is=67f6b9c1&hm=2eeab713683bde7bfe1533d31c8c7116203d5172a8f84b9a537a1cb65b3b2c42&")  # exemple de logo Discord
    # Crée un bouton
    bouton = Button(label="✅ J'accepte", style=discord.ButtonStyle.success)

    # Fonction appelée quand on clique sur le bouton
    async def bouton_callback(interaction):
        await interaction.response.send_message("Bienvenue sur le serveur ! 🎉", ephemeral=True)

    bouton.callback = bouton_callback

    # Affiche le bouton avec le message
    view = View()
    view.add_item(bouton)
    await ctx.send(embed=embed, view=view)
    
@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")
    scheduler.start()
    print("⏰ Planificateur démarré")
    # Ajoute le job quotidien à 10h (heure de Paris)
    scheduler.add_job(send_daily_message, 'cron', hour=10, minute=0, timezone=pytz.timezone('Europe/Paris'))

async def send_daily_message():
    channel = bot.get_channel(CHANNEL_ID)
    if isinstance(channel, discord.TextChannel):
        await channel.send("Bonjour tout le monde ! ☀️")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, raison=None):
    await member.kick(reason=raison)
    await ctx.send(f"{member} a été expulsé.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, raison=None):
    await member.ban(reason=raison)
    await ctx.send(f"{member} a été banni.")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong 🏓 ! Les intents sont actifs.")

print(os.getenv("DISCORD_TOKEN"))

keep_alive()
bot.run(my_secret)