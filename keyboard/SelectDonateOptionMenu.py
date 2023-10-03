from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Create inline menu for donation options
XMRDonateOptionButton = InlineKeyboardButton(text="💳 XMR Address", callback_data="xmr")
BTCDonateOptionButton = InlineKeyboardButton(text="💳 BTC Address", callback_data="btc")
USDDonateOptionButton = InlineKeyboardButton(text="💳 PayPal", callback_data="usd")
donateOptionsMarkup = InlineKeyboardMarkup(inline_keyboard=[[XMRDonateOptionButton, BTCDonateOptionButton], [USDDonateOptionButton]])