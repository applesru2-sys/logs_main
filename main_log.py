import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

LISTEN_CHANNEL_ID = 1500991511385342143
REPORT_CHANNEL_ID = 1500991763718996249

@bot.event
async def on_ready():
    print("="*40, flush=True)
    print(f"✅ ВНИМАНИЕ! КОД С EMBED-КАРТОЧКАМИ ЗАГРУЖЕН!", flush=True)
    print(f"🤖 Бот {bot.user.name} готов к работе.", flush=True)
    print("="*40, flush=True)

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author == bot.user:
        return

    # Проверка лог-канала
    if message.channel.id == LISTEN_CHANNEL_ID:
        
        # --- ЗАХОД В КАНАЛ (ЗЕЛЕНЫЙ) ---
        if message.content.startswith("!voice_join|"):
            data = message.content.split('|')
            if len(data) == 4:
                report_channel = bot.get_channel(REPORT_CHANNEL_ID)
                if report_channel:
                    user_id = data[1]
                    channel_id = data[2]
                    time_full = data[3]
                    
                    # Берем только время "23:40:38" из строки "04.05.2026 23:40:38"
                    time_only = time_full.split(' ')[1] if ' ' in time_full else time_full
                    
                    # Создаем зеленую карточку
                    embed = discord.Embed(
                        description=f"<@{user_id}> ` зашел в ` <#{channel_id}>\n` Время: ` `{time_only}`",
                        color=discord.Color.green()
                    )
                    
                    await report_channel.send(embed=embed)
                    print("✅ Красивый отчет ЗАХОД отправлен!", flush=True)

        # --- ВЫХОД ИЗ КАНАЛА (КРАСНЫЙ) ---
        elif message.content.startswith("!voice_leave|"):
            data = message.content.split('|')
            if len(data) == 5:
                report_channel = bot.get_channel(REPORT_CHANNEL_ID)
                if report_channel:
                    user_id = data[1]
                    channel_id = data[2]
                    time_full = data[3]
                    seconds_spent = int(data[4])
                    
                    time_only = time_full.split(' ')[1] if ' ' in time_full else time_full
                    minutes = seconds_spent // 60
                    seconds = seconds_spent % 60
                    
                    # Создаем красную карточку
                    embed = discord.Embed(
                        description=f"<@{user_id}> ` вышел из ` <#{channel_id}>\n` Время: ` `{time_only}`\n` Просидел: ` `{minutes} мин. {seconds} сек.`",
                        color=discord.Color.red()
                    )
                    
                    await report_channel.send(embed=embed)
                    print("✅ Красивый отчет ВЫХОД отправлен!", flush=True)

TOKEN = os.environ.get("TOKEN")
if TOKEN:
    bot.run(TOKEN)
