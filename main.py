import os
from asyncio import run
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.command import Command
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    # here you can place your guide how to use bot
    await message.reply_video(video="BAACAgIAAxkBAAMlaCRoKIPjkLixufqvSDU7bV7A19sAAhGQAAIVCyFJTFMujEJmVK02BA", show_caption_above_media=True, caption="Привет! Я - бот, который поможет отправлять тебе сообщения с кнопками в любое место!\nЧтобы это сделать, напиши в любом чате это: `@TheInlineButtonBot любое сообщение || текст кнопки - ссылка-кнопки.рф | та же строка - ссылка.рф / следующая строка - ссылка.рф`", parse_mode="markdown")


def get_message_text(text):
    try:
        text = text.split(" || ")[1]

        lines = text.split(" / ")

        builder = InlineKeyboardBuilder()
        for line in lines:
            parts = line.split(" | ")
            row = []
            for part in parts:
                link_text, link_url = part.split(" - ")
                row.append(types.InlineKeyboardButton(text=link_text, url=link_url))
            builder.row(*row)
        return builder
    except:
        pass


@dp.inline_query()
async def show_user_links(inline_query: types.InlineQuery):
    try:
        results = [InlineQueryResultArticle(
            id=str(uuid4()),
            title="Отправить",
            input_message_content=InputTextMessageContent(
                message_text=inline_query.query.split(" || ")[0],
                parse_mode="markdown"
            ),
            reply_markup=get_message_text(inline_query.query).as_markup()
        )]
        await inline_query.answer(results, is_personal=True)
    except:
        pass


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())
