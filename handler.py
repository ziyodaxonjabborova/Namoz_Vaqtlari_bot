from aiogram import Router,F
from aiogram.filters import Command,CommandStart
from aiogram.types import Message,ReplyKeyboardRemove,CallbackQuery,InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import requests

from datetime import date,datetime

from buttons import DATE_BUTTON,REGIONS_BUTTON
from states import Data
from regions import regions


router=Router()

@router.message(CommandStart())
async def start_handler(message:Message,state:FSMContext):
    
    await state.set_state(Data.date)
    await message.answer("Quyidagilardan birini tanlang: ",reply_markup=DATE_BUTTON)
    
    
@router.message(Data.date)
async def get_date(message:Message,state:FSMContext):
    if message.text not in ('Day','Week','Month'):
        await message.answer("❌ Iltimos Tugmalar orqali tanlang!")
    else:
        await state.update_data(date=message.text)
        await state.set_state(Data.region)
        clear_message=await message.answer(text=f"✅ Tanlandi: {message.text}",reply_markup=ReplyKeyboardRemove())
        await clear_message.delete()
        await message.answer(
    "📍 Quyidagi ro‘yxatdan o‘zingizga mos hududni tanlang 👇",
    reply_markup=REGIONS_BUTTON,
    parse_mode="Markdown"
)


@router.callback_query(F.data.startswith("region"))

async def get_region(call: CallbackQuery, state: FSMContext):
    region = call.data.split("_")[-1]
    data = await state.get_data()
    selected_date = data.get("date") 
    
    # buttons for Months
    MONTH_BUTTON=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Yanvar",callback_data=f"month_{region}_1"),
             InlineKeyboardButton(text="Fevral",callback_data=f"month_{region}_2"),
             InlineKeyboardButton(text="Mart",callback_data=f"month_{region}_3"),
             ],

            [InlineKeyboardButton(text="Aprel",callback_data=f"month_{region}_4"),
             InlineKeyboardButton(text="May",callback_data=f"month_{region}_5"),
             InlineKeyboardButton(text="Iyun",callback_data=f"month_{region}_6"),
             ],

            [InlineKeyboardButton(text="Iyul",callback_data=f"month_{region}_7"),
             InlineKeyboardButton(text="Avgust",callback_data=f"month_{region}_8"),
             InlineKeyboardButton(text="Sentyabr",callback_data=f"month_{region}_9"),
             ],

            [InlineKeyboardButton(text="Oktyabr",callback_data=f"month_{region}_10"),
             InlineKeyboardButton(text="Noyabr",callback_data=f"month_{region}_11"),
             InlineKeyboardButton(text="Dekabr",callback_data=f"month_{region}_12"),
             ],

        ]
    )

    if selected_date=="Day":
        url = f"https://islomapi.uz/api/present/day?region={region}"
        response = requests.get(url).json()

        times = response.get("times")
        region_name = response.get("region")

        today_date = date.today().strftime("%d-%B, %A") 
        text = (
            f"🕌 *Namoz vaqtlari — {region_name}*\n"
            f"📅 *{today_date.capitalize()}*\n\n"
            f"🌅 *Bomdod:* {times.get('tong_saharlik')}\n"
            f"🌞 *Quyosh:* {times.get('quyosh')}\n"
            f"☀️ *Peshin:* {times.get('peshin')}\n"
            f"🌤 *Asr:* {times.get('asr')}\n"
            f"🌇 *Shom:* {times.get('shom_iftor')}\n"
            f"🌙 *Xufton:* {times.get('hufton')}"
        )

        await call.message.answer(text, parse_mode="Markdown")
        
    elif selected_date == "Week":
        url = f"https://islomapi.uz/api/present/week?region={region}"
        response = requests.get(url).json()

       
        if not response or not isinstance(response, list):
            await call.message.answer("❌ Ma'lumot topilmadi.")
            return

        text = f"🕌 *{region}* — *Haftalik namoz vaqtlari*\n\n"

        
        for day_info in response:
            weekday = day_info.get("weekday")
            date_ = day_info.get("date")
            times = day_info.get("times", {})

            text += (
                f"📅 *{weekday}* — `{date_}`\n"
                f"🌅 Bomdod: `{times.get('tong_saharlik')}`\n"
                f"☀️ Quyosh: `{times.get('quyosh')}`\n"
                f"🏙 Peshin: `{times.get('peshin')}`\n"
                f"🌇 Asr: `{times.get('asr')}`\n"
                f"🌆 Shom: `{times.get('shom_iftor')}`\n"
                f"🌙 Xufton: `{times.get('hufton')}`\n\n"
            )

        await call.message.answer(text, parse_mode="Markdown")
        
    else:
        await call.message.answer("📅 Quyidagi ro‘yxatdan o‘zingizga kerakli *oyni* tanlang 👇",
                                  parse_mode="Markdown",reply_markup=MONTH_BUTTON)
        await state.set_state(Data.month)
        
    
@router.callback_query(F.data.startswith("month"))

async def get_month(call: CallbackQuery,state:FSMContext):
    month=int(call.data.split("_")[-1])
    region=call.data.split("_")[-2]
    
    data = requests.get(f"https://islomapi.uz/api/monthly?region={region}&month={month}").json()
    

    text = f"🕌 *{region}* — *{month}*-oy uchun namoz vaqtlari:\n\n"

    for day in data:
        iso_date = day["date"]
        vaqtlar = day["times"]

    
        sana_obj = datetime.fromisoformat(iso_date.replace("Z", ""))
        sana = sana_obj.strftime("%d-%B-%Y, %A")


        text += (
            f"📅 *{sana}*\n"
            f"🌅 Bomdod: `{vaqtlar['tong_saharlik']}`\n"
            f"🌞 Quyosh: `{vaqtlar['quyosh']}`\n"
            f"☀️ Peshin: `{vaqtlar['peshin']}`\n"
            f"🌤 Asr: `{vaqtlar['asr']}`\n"
            f"🌇 Shom: `{vaqtlar['shom_iftor']}`\n"
            f"🌙 Xufton: `{vaqtlar['hufton']}`\n\n"
        )

    await call.message.answer(text, parse_mode="Markdown")