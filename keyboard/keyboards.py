from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

# Create main bot control menu
shareLocationButton = KeyboardButton(text="🗺 Weather via location", request_location=True)
showDonateOptionsButton = KeyboardButton(text="💰 Donate")
showSettingsButton = KeyboardButton(text="⚙ Settings")

mainMenuMarkup = ReplyKeyboardMarkup(keyboard=[[showSettingsButton, showDonateOptionsButton], [shareLocationButton]],
                                           is_persistent=True, resize_keyboard=True)

# Create inline unit system selection menu
metricUnitButton = InlineKeyboardButton(text="🌡️ Imperial (°F, mi/h)", callback_data="imperial")
imperialUnitButton = InlineKeyboardButton(text="🌡️ Metric (°C, m/s)", callback_data="metric")
selectUnitSystemMarkup = InlineKeyboardMarkup(inline_keyboard=[[metricUnitButton, imperialUnitButton]])

# Create inline menu for donation options
XMRDonateOptionButton = InlineKeyboardButton(text="💳 XMR Address", callback_data="xmr")
BTCDonateOptionButton = InlineKeyboardButton(text="💳 BTC Address", callback_data="btc")
USDDonateOptionButton = InlineKeyboardButton(text="💳 PayPal", callback_data="usd")
donateOptionsMarkup = InlineKeyboardMarkup(inline_keyboard=[[XMRDonateOptionButton, BTCDonateOptionButton], [USDDonateOptionButton]])

# Create inline settings inline markup
changeUnitSystemButton = InlineKeyboardButton(text="🌡 Unit system", callback_data="setUnits")
featuredPlacesListButton = InlineKeyboardButton(text="🏅 Featured places", callback_data="featuredPlaces")
# setNotificationsButton = InlineKeyboardButton(text="🔔 Notifications", callback_data="setNotifications")
settingsInlineMarkup = InlineKeyboardMarkup(inline_keyboard=[[changeUnitSystemButton], [featuredPlacesListButton]])

# Create featured places control inline markup
addFeaturedPlace = InlineKeyboardButton(text="➕ Add Featured Place", callback_data="addFeaturedPlace")
removeFeaturedPlace = InlineKeyboardButton(text="❌ Remove Featured Place", callback_data="removeFeaturedPlace")
featuredPlacesMarkup = InlineKeyboardMarkup(inline_keyboard=[[addFeaturedPlace], [removeFeaturedPlace]])

# Create cancel menu inlilne markup
cancelButton = InlineKeyboardButton(text="🔙 Cancel", callback_data="cancel")
cancelMarkup = InlineKeyboardMarkup(inline_keyboard=[[cancelButton]])