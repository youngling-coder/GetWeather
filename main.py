# Importing necessary libraries & modules
import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hbold, hcode

from location import Location
from weather_report import WeatherReport

# Set logging level
logging.basicConfig(level=logging.INFO)

# Parsing bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")


# Unit system variable is responsible for the unit system to be used for weather information
unit_system = ""

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

# Create main bot control menu
shareLocationButton = KeyboardButton(text="🗺 Weather via location", request_location=True)
showDonateOptionsButton = KeyboardButton(text="💰 Donate")
featuredCityListButton = KeyboardButton(text="🏅 Featured places (Available soon...)")
changeUnitTypeButton = KeyboardButton(text="🌡 Units")
setOrRemoveNotificationsButton = KeyboardButton(text="🔔 Notifications (Available soon...)")
botControlMenuMarkup = ReplyKeyboardMarkup(keyboard=[[changeUnitTypeButton, showDonateOptionsButton],
                                                     [featuredCityListButton, setOrRemoveNotificationsButton], [shareLocationButton]],
                                           is_persistent=True, resize_keyboard=True)


# Create inline unit system selection menu
metricUnitButton = InlineKeyboardButton(text="🌡️ Imperial (°F, mi/h)", callback_data="imperial")
imperialUnitButton = InlineKeyboardButton(text="🌡️ Metric (°C, m/s)", callback_data="metric")
selectUnitTypeMarkup = InlineKeyboardMarkup(inline_keyboard=[[metricUnitButton, imperialUnitButton]])

# Create inline menu for donation options
XMRDonateOptionButton = InlineKeyboardButton(text="💳 XMR Address", callback_data="xmr")
BTCDonateOptionButton = InlineKeyboardButton(text="💳 BTC Address", callback_data="btc")
USDDonateOptionButton = InlineKeyboardButton(text="💳 PayPal", callback_data="usd")
donateOptionsMarkup = InlineKeyboardMarkup(inline_keyboard=[[XMRDonateOptionButton, BTCDonateOptionButton], [USDDonateOptionButton]])


@dp.callback_query(lambda call: call.data in ["usd", "btc", "xmr"])
async def handleDonations(call: CallbackQuery):

    # Send donation appropriate donation credentials
    match call.data:
        case "usd":
            await call.message.answer("<b>Paypal link:</b> https://www.paypal.com/paypalme/rusticCoder")
        case "xmr":
            await call.message.answer(f"<b>XMR:</b> {hcode('48F313vAnVVdK9SzXUKoVyjeUyZ2Ad3z44PMkJPCa54oDgKDxQsvRwA9d5od7XhwjgUoq4mC6A6XkFmJta4B3NbWUwKGHf6')}")
        case "btc":
            await call.message.answer(f"<b>BTC:</b> {hcode('3NSsKDBcWJEoDKHdxZ7uQiDR42MkbVNm26')}")


@dp.callback_query(lambda call: call.data in ["imperial", "metric"])
async def handleSelectedUnitSystem(call: CallbackQuery):
    global unit_system

    # Check which option has been chosen by user
    if call.data == "imperial":

        # If user has chosen imperial unit system then set
        # imperial system as default and show appropriate message
        unit_system = "imperial"
        await call.message.answer(f"You've chosen {hbold('Imperial')} as primary unit!"
                                  f"\nYou can change it later using {hbold('🌡 Units')}.")
    elif call.data == "metric":

        # If user has chosen metric unit system then set metric
        # system as default and show appropriate message
        unit_system = "metric"
        await call.message.answer(f"You've chosen {hbold('Metric')} as primary unit system!"
                                  f"\nYou can change it later using {hbold('🌡 Units')}.")

    await call.message.answer("✅ Now you can send me any city, region or village to get latest weather info!",
                              reply_markup=botControlMenuMarkup)


@dp.message(CommandStart())
async def greets(message: Message):

    # Send greeting message when user sends /start to bot
    await message.answer(f"Hello, {message.from_user.full_name}! Welcome to {hbold('GetWeather')} Bot!👋\n"
                         f"To start, select unit system:", reply_markup=selectUnitTypeMarkup)


@dp.message(lambda message: changeUnitTypeButton.text == message.text)
async def sendSelectUnitSystemRequest(message: Message):

    # Asking to select unit system in inline menu when user want to change it
    await message.answer("Select unit system you prefer:", reply_markup=selectUnitTypeMarkup)

@dp.message(lambda message: showDonateOptionsButton.text == message.text)
async def sendDonateOptionsList(message: Message):

    # Send thank you message to user and show ways to donate
    await message.answer("We're really glad you decided support our little project! These are the donation options available:", reply_markup=donateOptionsMarkup)


@dp.message(lambda message: setOrRemoveNotificationsButton.text == message.text)
async def setNotificationsRequest(message: Message):

    # Feature under development
    await message.answer(
        "We apologize for the inconvenience, but at the moment, this feature is in the development stage.☹.")


@dp.message(lambda message: featuredCityListButton.text == message.text)
async def sendEditUnitSystemRequest(message: Message):

    # Feature under development
    await message.answer(
        "We apologize for the inconvenience, but at the moment, this feature is in the development stage  ☹.")

async def handleCityWeather(message: Message, city: str):
    if not unit_system:

        # If user hasn't selected any unit system then asking him to do this
        await message.answer("⚠ To start using bot, select unit system:", reply_markup=selectUnitTypeMarkup)
    else:

        # Create WeatherReport instance to receive and process weather info
        weather = WeatherReport(city=city, unit_system=unit_system)

        # Get weather info and catching errors to res variable
        res = weather.getWeatherData(weather.URL())

        if res:

            # Send appropriate error message to user if there're any errors
            await message.answer(res, reply_markup=botControlMenuMarkup)
        else:

            # Get formatted weather info to show it to user
            weather = weather.beautify()

            # Send desired city/region weather to user
            await message.answer(weather, reply_markup=botControlMenuMarkup)

@dp.message()
async def handleUserCityInput(message: Message):

    # Parse city/region name

    if message.location:
        coordinates = (message.location.latitude, message.location.longitude)

        location = Location(coordinates[0], coordinates[1])

        query_url = location.URL()

        city = location.handleCoordinatesAsCityName(query_url=query_url)

    else:
        city = message.text

    if city.startswith("❌"):
        await message.reply(city)
    else:
        await handleCityWeather(message=message, city=city)

async def main() -> None:

    # Start bot
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


# Run main bot function
asyncio.run(main())
