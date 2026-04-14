import os
import discord
from discord.ext import commands
import aiohttp

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openrouter/elephant-alpha"

# 🚨 SUBSTITUA PELO ID DO SEU CANAL
CANAL_PERMITIDO = 1493367407396389095

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

async def ask_openrouter(question: str) -> str:
    # ... (a função permanece a mesma) ...
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": question}],
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(OPENROUTER_URL, headers=headers, json=payload) as resp:
            if resp.status != 200:
                error_text = await resp.text()
                return f"❌ Erro na API: {resp.status}\n{error_text[:200]}"
            data = await resp.json()
            try:
                return data["choices"][0]["message"]["content"]
            except (KeyError, IndexError):
                return "⚠️ Resposta inesperada da API."

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

@bot.command(name="i")
async def ask(ctx, *, pergunta: str):
    """
    Comando .i <pergunta> – pergunta para a IA.
    Exemplo: .i Qual o sentido da vida?
    """
    # 🚨 VERIFICAÇÃO DO CANAL
    if ctx.channel.id != CANAL_PERMITIDO:
        await ctx.send("❌ Este comando só pode ser usado em um canal específico.", delete_after=5)
        return

    async with ctx.typing():
        resposta = await ask_openrouter(pergunta)

    # ... (o resto do código permanece o mesmo) ...
    if len(resposta) <= 2000:
        await ctx.reply(resposta)
    else:
        for i in range(0, len(resposta), 2000):
            await ctx.send(resposta[i:i+2000])

bot.run(DISCORD_TOKEN)
