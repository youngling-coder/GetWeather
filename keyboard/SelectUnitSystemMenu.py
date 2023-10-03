from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Create inline unit system selection menu
metricUnitButton = InlineKeyboardButton(text="🌡️ Imperial (°F, mi/h)", callback_data="imperial")
imperialUnitButton = InlineKeyboardButton(text="🌡️ Metric (°C, m/s)", callback_data="metric")
selectUnitSystemMarkup = InlineKeyboardMarkup(inline_keyboard=[[metricUnitButton, imperialUnitButton]])