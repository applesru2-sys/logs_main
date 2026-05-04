import discord
from discord.ext import commands
import os

# 1. Включаем права (intents)
intents = discord.Intents.default()
intents.message_content = True # ВАЖНО: Без этого бот не увидит текст сообщения!
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

# --- НАСТРОЙКИ КАНАЛОВ ---
LISTEN_CHANNEL_ID = 1500991511385342143 # Отсюда ЧИТАЕМ (сообщения селф-бота)
REPORT_CHANNEL_ID = 1500991763718996249 # Сюда ПИШЕМ (красивые отчеты)

@bot.event
async def on_ready():
    print(f"✅ Главный бот {bot.user.name} запущен! Жду логи от селф-бота...")

@bot.event
async def on_message(message):
    # Разрешаем боту обрабатывать другие команды (например, .профиль)
    await bot.process_commands(message)

    # Игнорируем свои же сообщения
    if message.author == bot.user:
        return

    # Если сообщение пришло НЕ в канал для логов — пропускаем
    if message.channel.id != LISTEN_CHANNEL_ID:
        return

    # Находим канал, куда будем отправлять красивые отчеты
    report_channel = bot.get_channel(REPORT_CHANNEL_ID)
    if not report_channel:
        print(f"❌ Ошибка: Не могу найти канал для отчетов ({REPORT_CHANNEL_ID})")
        return

    # --- ОБРАБОТКА ЗАХОДА ---
    if message.content.startswith("!voice_join|"):
        data = message.content.split('|')
        if len(data) == 4:
            user_id = data[1]
            channel_id = data[2]
            time_start = data[3]

            text = f"🟢 <@{user_id}> **зашел** в канал <#{channel_id}> в `{time_start}`"
            await report_channel.send(text)
            print(f"Успешно отправлен отчет о заходе юзера {user_id}")

    # --- ОБРАБОТКА ВЫХОДА ---
    elif message.content.startswith("!voice_leave|"):
        data = message.content.split('|')
        if len(data) == 5:
            user_id = data[1]
            channel_id = data[2]
            time_end = data[3]
            seconds_spent = int(data[4])

            minutes = seconds_spent // 60
            seconds = seconds_spent % 60

            text = f"🔴 <@{user_id}> **вышел** из канала <#{channel_id}> в `{time_end}`.\n⏳ Просидел: **{minutes} мин. {seconds} сек.**"
            await report_channel.send(text)
            print(f"Успешно отправлен отчет о выходе юзера {user_id}")


# Получаем токен из настроек BotHost и запускаем
TOKEN = os.environ.get("TOKEN")

if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ Ошибка: Токен не найден! Проверь настройки BotHost.")
