import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

# Bot tokeni
API_TOKEN = "8237038808:AAHoVW7UOOTvCy5gARbBZd-PC55lNSokWo0"

# Guruh IDlari
CHECK_GROUP_ID = -1002607719842   # Tekshirish uchun guruh
POST_GROUP_ID = -1002509537965    # Ma'lumot yuboriladigan guruh
OWNER_ID = 7817943416             # Guruh egasi

# Logging
logging.basicConfig(level=logging.INFO)

# Bot va dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# States
class Registration(StatesGroup):
    ism = State()
    familiya = State()
    otasi = State()
    tugilgan_sana = State()
    tugilgan_joy = State()
    mahalla = State()
    lavozim = State()
    rais = State()
    xotin_qiz = State()
    inspektor = State()
    rasm = State()

# Start komandasi
@dp.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await message.answer("Assalomu alaykum! Yetakchilarni ro‘yxatdan o‘tkazish botiga xush kelibsiz. Keling, boshlaymiz. Ismingizni kiriting:")
    await state.set_state(Registration.ism)

@dp.message(Registration.ism)
async def process_ism(message: Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await message.answer("Familiyangizni kiriting:")
    await state.set_state(Registration.familiya)

@dp.message(Registration.familiya)
async def process_familiya(message: Message, state: FSMContext):
    await state.update_data(familiya=message.text)
    await message.answer("Otasining ismini kiriting:")
    await state.set_state(Registration.otasi)

@dp.message(Registration.otasi)
async def process_otasi(message: Message, state: FSMContext):
    await state.update_data(otasi=message.text)
    await message.answer("Tug‘ilgan sana (YYYY-MM-DD) formatida kiriting:")
    await state.set_state(Registration.tugilgan_sana)

@dp.message(Registration.tugilgan_sana)
async def process_tugilgan_sana(message: Message, state: FSMContext):
    await state.update_data(tugilgan_sana=message.text)
    await message.answer("Tug‘ilgan joyingiz (viloyat, tuman/shahar):")
    await state.set_state(Registration.tugilgan_joy)

@dp.message(Registration.tugilgan_joy)
async def process_tugilgan_joy(message: Message, state: FSMContext):
    await state.update_data(tugilgan_joy=message.text)
    await message.answer("Hozir faoliyat olib borayotgan mahallangiz:")
    await state.set_state(Registration.mahalla)

@dp.message(Registration.mahalla)
async def process_mahalla(message: Message, state: FSMContext):
    await state.update_data(mahalla=message.text)
    await message.answer("Lavozimingiz:")
    await state.set_state(Registration.lavozim)

@dp.message(Registration.lavozim)
async def process_lavozim(message: Message, state: FSMContext):
    await state.update_data(lavozim=message.text)
    await message.answer("Mahalla raisining ismi, familiyasi, otasining ismi va telefon raqami:")
    await state.set_state(Registration.rais)

@dp.message(Registration.rais)
async def process_rais(message: Message, state: FSMContext):
    await state.update_data(rais=message.text)
    await message.answer("Mahalla xotin-qizlar faolining ismi, familiyasi, otasining ismi va telefon raqami:")
    await state.set_state(Registration.xotin_qiz)

@dp.message(Registration.xotin_qiz)
async def process_xotin_qiz(message: Message, state: FSMContext):
    await state.update_data(xotin_qiz=message.text)
    await message.answer("Profilaktika inspektorining telefon raqami:")
    await state.set_state(Registration.inspektor)

@dp.message(Registration.inspektor)
async def process_inspektor(message: Message, state: FSMContext):
    await state.update_data(inspektor=message.text)
    await message.answer("Rasmiy suratni jo‘nating:")
    await state.set_state(Registration.rasm)

@dp.message(Registration.rasm, F.photo)
async def process_rasm(message: Message, state: FSMContext):
    await state.update_data(rasm=message.photo[-1].file_id)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Tekshirish", callback_data="check_group")]])
    await message.answer("✅ Ma'lumotlar qabul qilindi. Endi guruh a'zoligini tekshiramiz:", reply_markup=keyboard)

@dp.callback_query(F.data == "check_group")
async def check_group(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    member = await bot.get_chat_member(CHECK_GROUP_ID, user_id)
    if member.status in ["member", "administrator", "creator"]:
        data = await state.get_data()
        caption = (
            f"📝 Yangi ro‘yxatdan o‘tgan yetakchi:\n\n"
            f"👤 {data['ism']} {data['familiya']} {data['otasi']}\n"
            f"🎂 {data['tugilgan_sana']}\n"
            f"📍 {data['tugilgan_joy']}\n"
            f"🏠 Mahalla: {data['mahalla']}\n"
            f"💼 Lavozim: {data['lavozim']}\n"
            f"👔 Rais: {data['rais']}\n"
            f"👩‍🦰 Xotin-qizlar faoli: {data['xotin_qiz']}\n"
            f"👮‍♂️ Inspektor: {data['inspektor']}"
        )
        await bot.send_photo(POST_GROUP_ID, data['rasm'], caption=caption)
        await callback.message.answer("🎉 TABRIKLAYMAN! RO‘YXATDAN O‘TDINGIZ, SHAXSINGIZ TASDIQLANDI.")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔑 Fayllarning parollari", callback_data="show_passwords")]])
        await callback.message.answer("Quyidagi tugma orqali parollarni ko‘rishingiz mumkin:", reply_markup=keyboard)
    else:
        join_btn = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔗 Guruhga a'zo bo‘lish", url="https://t.me/+vKvbXb3Dg_kzMTdi")]])
        await callback.message.answer("❌ Siz hali guruhga a'zo emassiz. Iltimos, avval guruhga qo‘shiling.", reply_markup=join_btn)

@dp.callback_query(F.data == "show_passwords")
async def show_passwords(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Profilaktik hisobda", callback_data="p1")],
        [InlineKeyboardButton(text="Probatsiya hisobda", callback_data="p2")],
        [InlineKeyboardButton(text="Qolgan toifalar", callback_data="p3")]
    ])
    await callback.message.answer("BARCHA MA'LUMOTLAR QUYIDAGI PAROL BILAN PAROLLANGAN", reply_markup=keyboard)

@dp.callback_query(F.data.in_(["p1", "p2", "p3"]))
async def passwords(callback: CallbackQuery):
    if callback.data == "p1":
        await callback.message.answer("Profilaktik hisobda parol: yetakchi1")
    elif callback.data == "p2":
        await callback.message.answer("Probatsiya hisobda parol: yetakchi2")
    elif callback.data == "p3":
        await callback.message.answer("Shu tariqa barcha toifalar paroli: yetakchi1-10 gacha.\n\nE'TIBORINGIZ UCHUN RAHMAT!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
