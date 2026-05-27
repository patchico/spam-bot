import discord
from discord.ext import commands
import asyncio

# ─── CONFIG ────────────────────────────────────────────────────────────────────
import os
TOKEN = os.environ.get("TOKEN")    # ← Remplace par ton token Discord
DELAY = 1                  # Délai entre chaque message (en secondes)
# ───────────────────────────────────────────────────────────────────────────────

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

spam_channel = None
spamming = False
spam_task = None
spam_message = ""


@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")
    print(f"   Commandes : !start <message> | !stop")


@bot.command(name="start")
async def start_spam(ctx, *, message=None):
    """Démarre le spam avec le message choisi. Ex: !start hello world"""
    global spam_channel, spamming, spam_task, spam_message

    if spamming:
        await ctx.send("⚠️ Le spam est déjà en cours ! Utilise `!stop` pour l'arrêter.")
        return

    if not message:
        await ctx.send("❌ Tu dois écrire un message ! Exemple : `!start soul answer`")
        return

    spam_channel = ctx.channel
    spam_message = message
    spamming = True

    await ctx.send(f"🚀 Spam démarré : **{spam_message}** — Utilise `!stop` pour arrêter.")
    spam_task = asyncio.create_task(spam_loop())


@bot.command(name="stop")
async def stop_spam(ctx):
    """Arrête le spam."""
    global spamming, spam_task

    if not spamming:
        await ctx.send("ℹ️ Le spam n'est pas en cours.")
        return

    spamming = False
    if spam_task:
        spam_task.cancel()
        spam_task = None

    await ctx.send("🛑 Spam arrêté !")


async def spam_loop():
    global spamming, spam_channel, spam_message
    try:
        while spamming:
            if spam_channel:
                await spam_channel.send(spam_message)
            await asyncio.sleep(DELAY)
    except asyncio.CancelledError:
        pass


bot.run(TOKEN)
