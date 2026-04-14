import discord
from discord.ext import commands
import os
import dotenv

# Carregar variáveis de ambiente
dotenv.load_dotenv()

# Substitua com seu token do bot
TOKEN_DO_SEU_BOT = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

# Comando clear: apenas usuários com a role específica podem usar
@bot.command()
@commands.has_role("1493360768190517498")  # Substitua pelo ID do cargo (role) desejado
async def clear(ctx, quantidade: int = None):
    if quantidade is None:
        await ctx.send("🔴 Por favor, especifique quantas mensagens deseja limpar. Ex: `!clear 10`")
        return

    if quantidade < 1 or quantidade > 100:
        await ctx.send("🔴 A quantidade deve estar entre 1 e 100.")
        return

    # Deleta as mensagens (incluindo a do comando)
    await ctx.channel.purge(limit=quantidade + 1)
    await ctx.send(f"🗑️ Foram deletadas **{quantidade}** mensagens.", delete_after=5)

# Inicia o bot
bot.run(TOKEN_DO_SEU_BOT)
