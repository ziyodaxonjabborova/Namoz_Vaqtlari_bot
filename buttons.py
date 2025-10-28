from aiogram.types import (
    ReplyKeyboardMarkup,KeyboardButton,
    InlineKeyboardButton,InlineKeyboardMarkup
    )
from regions import regions

DATE_BUTTON=ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Day")],
        [KeyboardButton(text="Week")],
        [KeyboardButton(text="Month")]
    ],
    resize_keyboard=True
)

# buttons for regions:

buttons=[]
inline_button=[]
for i, region in enumerate(regions, start=1):
    buttons.append(InlineKeyboardButton(text=f"{region}", callback_data=f"region_{region}"))
    if i % 3 == 0:
        inline_button.append(buttons)
        buttons = []
if buttons:
    inline_button.append(buttons)


REGIONS_BUTTON=InlineKeyboardMarkup(
    inline_keyboard=inline_button
)


        

        
    
    