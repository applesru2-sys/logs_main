import discord
from discord.ext import commands
import os

# Включаем намерения (intents), чтобы бот видел сообщения и участников
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Создаем бота
bot = commands.Bot(command_prefix=".", intents=intents)

# --- НАСТРОЙКИ КАНАЛОВ ---
# Канал, откуда бот ЧИТАЕТ системные данные (от селф-бота)
LISTEN_CHANNEL_ID = 1500991511385342143
# Канал, куда бот ПИШЕТ красивые отчеты для людей
REPORT_CHANNEL_ID = 1500991763718996249

@bot.event
async def on_ready():
    print(f"✅ Главный бот {bot.user.name} успешно запущен и готов к работе!")

@bot.event
async def on_message(message):
    # ВАЖНО: эта строчка нужна, чтобы другие команды (типа .профиль) тоже работали!
    await bot.process_commands(message)

    # Игнорируем свои же сообщения
    if message.author == bot.user:
        return

    # Если сообщение пришло НЕ в технический канал — просто игнорируем его
    if message.channel.id != LISTEN_CHANNEL_ID:
        return

    # Находим канал, куда будем отправлять красивые отчеты
    report_channel = bot.get_channel(REPORT_CHANNEL_ID)
    if not report_channel:
        print(f"❌ Ошибка: Основной бот не видит канал для отчетов ({REPORT_CHANNEL_ID})")
        return

    # --- ОБРАБОТКА ЗАХОДА ---
    if message.content.startswith("!voice_join|"):
        data = message.content.split('|')
        if len(data) == 4:
            user_id = data[1]
            channel_id = data[2]
            time_start = data[3]

            # Формируем красивое сообщение и отправляем
            text = f"🟢 <@{user_id}> **зашел** в канал <#{channel_id}> в `{time_start}`"
            await report_channel.send(text)

    # --- ОБРАБОТКА ВЫХОДА ---
    elif message.content.startswith("!voice_leave|"):
        data = message.content.split('|')
        if len(data) == 5:
            user_id = data[1]
            channel_id = data[2]
            time_end = data[3]
            seconds_spent = int(data[4])

            # Переводим скучные секунды в удобные минуты и секунды
            minutes = seconds_spent // 60
            seconds = seconds_spent % 60

            text = f"🔴 <@{user_id}> **вышел** из канала <#{channel_id}> в `{time_end}`.\n⏳ Просидел: **{minutes} мин. {seconds} сек.**"
            await report_channel.send(text)


# Получаем токен из настроек BotHost и запускаем бота
TOKEN = os.environ.get("TOKEN")

if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ Ошибка: Токен не найден! Добавь переменную TOKEN в настройки BotHost.")
