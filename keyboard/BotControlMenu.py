from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Create main bot control menu
shareLocationButton = KeyboardButton(text="🗺 Weather via location", request_location=True)
showDonateOptionsButton = KeyboardButton(text="💰 Donate")
featuredCityListButton = KeyboardButton(text="🏅 Featured places (Available soon...)")
changeUnitSystemButton = KeyboardButton(text="🌡 Units")
setOrRemoveNotificationsButton = KeyboardButton(text="🔔 Notifications (Available soon...)")
botControlMenuMarkup = ReplyKeyboardMarkup(keyboard=[[changeUnitSystemButton, showDonateOptionsButton],
                                                     [featuredCityListButton, setOrRemoveNotificationsButton], [shareLocationButton]],
                                           is_persistent=True, resize_keyboard=True)