import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Токени боти наватон (@mustafosho_bot):
TOKEN = "8694219744:AAHBjQaQO4zJ2loC3qqyenmWoCTYyLsQ-bE"

# 1. Юзернейм ва ID-и канали умумӣ
PUBLIC_CHANNEL_USERNAME = "cinematj07_bot"  # Бе аломати @
PUBLIC_CHANNEL_ID = -1003776440965      # ID-и канали умумӣ

# 2. ID-и канали махфӣ
PRIVATE_CHANNEL_ID = -1004360285326

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функцияи санҷиши обуна (акнун тавассути ID тафтиш мекунад)
async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=PUBLIC_CHANNEL_ID, user_id=user_id)
        return member.status in ["creator", "administrator", "member"]
    except Exception as e:
        print(f"Хатогии санҷиши обуна: {e}")
        return False

@dp.message(CommandStart())
async def start_handler(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    msg_id_str = command.args # Рақами паёми кино аз канали махфӣ

    if not msg_id_str:
        await message.answer("Ассалому алайкум! Барои тамошои кино тугмаро дар канал пахш кунед.")
        return

    # Санҷиши обуна ба канали умумӣ
    is_sub = await check_subscription(user_id)

    if is_sub:
        try:
            msg_id = int(msg_id_str)
            await message.answer("🎬 Марҳамат, кинои шумо:")
            
            # Бот киноро аз канали махфӣ ба корбар copy мекунад
            await bot.copy_message(
                chat_id=user_id,
                from_chat_id=PRIVATE_CHANNEL_ID,
                message_id=msg_id
            )
        except Exception as e:
            await message.answer("❌ Кино ёфт нашуд ё хатогӣ рух дод.")
            print(f"Хатогии фиристодани кино: {e}")
    else:
        bot_username = (await bot.get_me()).username
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Обуна шудан ба канал", url=f"https://t.me/{PUBLIC_CHANNEL_USERNAME}")],
            [InlineKeyboardButton(text="🔄 Тафтиши обуна", url=f"https://t.me/{bot_username}?start={msg_id_str}")]
        ])
        await message.answer(
            "❌ Барои тамошои кино аввал ба канали мо обуна шавед ва баъд тугмаи «Тафтиши обуна»-ро пахш кунед:",
            reply_markup=keyboard
        )

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот фаъол шуд...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
