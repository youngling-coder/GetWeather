from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Create main bot control menu
shareLocationButton = KeyboardButton(text="🗺 Weather via location", request_location=True)
showDonateOptionsButton = KeyboardButton(text="💰 Donate")
featuredCityListButton = KeyboardButton(text="🏅 Featured places (Available soon...)")
changeUnitTypeButton = KeyboardButton(text="🌡 Units")
setOrRemoveNotificationsButton = KeyboardButton(text="🔔 Notifications (Available soon...)")
botControlMenuMarkup = ReplyKeyboardMarkup(keyboard=[[changeUnitTypeButton, showDonateOptionsButton],
                                                     [featuredCityListButton, setOrRemoveNotificationsButton], [shareLocationButton]],
                                           is_persistent=True, resize_keyboard=True)