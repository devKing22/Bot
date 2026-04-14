import discord
from discord.ext import commands
import os

token = os.getenv("TOKEN_DC")

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

@bot.command(name='c')
@commands.has_permissions(manage_messages=True)
async def clear_messages(ctx, quantidade: int):
    """
    Comando para limpar mensagens no canal.
    Uso: .c <número>
    """
    if quantidade <= 0:
        await ctx.send("❌ O número deve ser maior que zero.", delete_after=3)
        return

    if quantidade > 400:
        await ctx.send("⚠️ Você pode deletar no máximo 400 mensagens por vez.", delete_after=5)
        return

    deletadas = await ctx.channel.purge(limit=quantidade + 1)

    await ctx.send(f"✅ {len(deletadas)-1} mensagens apagadas.", delete_after=3)

@clear_messages.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❗ Uso correto: !c <número>", delete_after=5)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ O argumento deve ser um número inteiro.", delete_after=5)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("🔒 Você precisa da permissão Gerenciar Mensagens para usar este comando.", delete_after=5)
    else:
        await ctx.send("⚠️ Ocorreu um erro inesperado.")
bot.run('token')
