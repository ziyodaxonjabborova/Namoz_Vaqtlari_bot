from aiogram import Router,F
from aiogram.filters import Command,CommandStart
from aiogram.types import Message,ReplyKeyboardRemove,CallbackQuery
from aiogram.fsm.context import FSMContext
import requests

from datetime import date

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

        # Agar ma'lumot topilmasa
        if not response or not isinstance(response, list):
            await call.message.answer("❌ Ma'lumot topilmadi.")
            return

        text = f"🕌 *{region}* — *Haftalik namoz vaqtlari*\n\n"

        # API haftalik natijani list shaklida qaytaradi
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
        
    
    
    

