from aiogram.fsm.state import State,StatesGroup


class Data(StatesGroup):
    date=State()
    region=State()
    month=State()