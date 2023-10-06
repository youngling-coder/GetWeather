# Importing necessary libraries & modules
import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold, hcode
from keyboard.keyboards import *

from database import Database
from location import Location
from weather_report import WeatherReport

# Set logging level
logging.basicConfig(level=logging.INFO)

# Parsing bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

# Create database instance to handle work with user settings
usersDB = Database()

@dp.callback_query(lambda call: call.data in ["usd", "btc", "xmr"])
async def handleDonations(call: CallbackQuery):

    usersDB.resetCommand(uID=call.message.chat.id)
    
    # Send donation appropriate donation credentials
    match call.data:
        case "usd":
            await call.message.answer("<b>Paypal link:</b> https://www.paypal.com/paypalme/rusticCoder")
        case "xmr":
            await call.message.answer(f"<b>XMR:</b> {hcode('48F313vAnVVdK9SzXUKoVyjeUyZ2Ad3z44PMkJPCa54oDgKDxQsvRwA9d5od7XhwjgUoq4mC6A6XkFmJta4B3NbWUwKGHf6')}")
        case "btc":
            await call.message.answer(f"<b>BTC:</b> {hcode('3NSsKusersDBcWJEoDKHdxZ7uQiDR42MkbVNm26')}")

    await call.answer()

@dp.callback_query(lambda call: call.data == "setUnits")
async def sendUnitSystemOptions(call: CallbackQuery):

    usersDB.resetCommand(uID=call.message.chat.id)
    
    # Asking to select unit system in inline menu when user want to change it
    await call.message.answer("Select unit system you" 
                      f" prefer ({hbold('Metric')} if ignored, or selected before):", reply_markup=selectUnitSystemMarkup)
    await call.answer()

@dp.callback_query(lambda call: call.data == "cancel")
async def cancelAction(call: CallbackQuery):
    
    # Cancel any action
    usersDB.resetCommand(uID=call.message.chat.id)
    await call.message.edit_text(text=hbold("❌ Cancelled!"))
    await call.answer()

@dp.callback_query(lambda call: call.data == "addFeaturedPlace")
async def addFeaturedPlaceHandler(call: CallbackQuery):

    usersDB.setCommand(uID=call.message.chat.id, chain="addFeaturedPlace")
    
    await call.message.answer(text=f"▶ Send me any city or region name to add it to the {hbold('Featured Places')}."
                              "You can add multiple places separating them by colon (':').",
                              reply_markup=cancelMarkup)
    await call.answer()
    
@dp.callback_query(lambda call: call.data == "removeFeaturedPlace")
async def removeFeaturedPlaceHandler(call: CallbackQuery):
    
    usersDB.setCommand(uID=call.message.chat.id, chain="removeFeaturedPlace")

    await call.message.answer(text=f"▶ Send me city or region name from {hbold('Featured Places')} "
                              f"list to remove it/them to the {hbold('Featured Places')}. "
                              "You can remove multiple places separating them by colon (':').",
                              reply_markup=cancelMarkup)
    await call.answer()
    
@dp.callback_query(lambda call: call.data[0] in [str(i) for i in range(0, 5)])
async def getWeatherFeatured(call: CallbackQuery):
    await handleCityWeather(message=call.message, city=call.data[1:])
    await call.answer()
    
@dp.callback_query(lambda call: call.data == "featuredPlaces")
async def askToSendFeaturePlace(call: CallbackQuery):
    
    usersDB.resetCommand(uID=call.message.chat.id)

    places = usersDB.getFeaturedPlaces(call.message.chat.id)

    featuredPlacesMarkup.inline_keyboard = [[addFeaturedPlace], [removeFeaturedPlace]]

    if places:
        index = 0
        for p in places:
            featuredPlacesMarkup.inline_keyboard.insert(index, [InlineKeyboardButton(text=f"🏙 {p}", callback_data=f"{index}{p}")])
            index += 1
    
    await call.message.answer(text=f"{hbold('🏅 Featured places')}", reply_markup=featuredPlacesMarkup)
    
    await call.answer()

@dp.callback_query(lambda call: call.data in ["imperial", "metric"])
async def setSelectedUnitSystem(call: CallbackQuery):
    global unit_system

    usersDB.resetCommand(uID=call.message.chat.id)
    
    # Check which option has been chosen by user
    if call.data == "imperial":

        # If user has chosen imperial unit system then set
        # imperial system as default and show appropriate message
        usersDB.updateUnitSystem(uID=str(call.message.chat.id), unitSystem="imperial")
    elif call.data == "metric":

        # If user has chosen metric unit system then set metric
        # system as default and show appropriate message
        usersDB.updateUnitSystem(uID=str(call.message.chat.id), unitSystem="metric")
    
    await call.message.answer(f"You've chosen {hbold(call.data.capitalize())} as primary unit system! "
                              f"You can change it later using {hbold('🌡 Units')}.",
                              reply_markup=mainMenuMarkup)
        
    await call.answer()


@dp.message(CommandStart())
async def greets(message: Message):
    usersDB.resetCommand(uID=message.chat.id)

    if not usersDB.userExists(uID=message.chat.id):
        usersDB.addNewUser(uID=message.chat.id)
    # Send greeting message when user sends /start to bot
    await message.answer(text=f"Hello, {message.from_user.full_name}! Welcome to {hbold('GetWeather')} Bot!👋"
                         f" Now you can send me any city or region to get latest weather info!",
                         reply_markup=mainMenuMarkup)

@dp.message(lambda message: showDonateOptionsButton.text == message.text)
async def sendDonateOptionsList(message: Message):
    usersDB.resetCommand(uID=message.chat.id)

    # Send thank you message to user and show ways to donate
    await message.answer("We're really glad you decided support our little project! These are the donation options available:", reply_markup=donateOptionsMarkup)


@dp.message(lambda message: showSettingsButton.text == message.text)
async def setNotificationsRequest(message: Message):
    usersDB.resetCommand(uID=message.chat.id)

    # Feature under development
    await message.answer(f"{hbold('⚙ Settings')}", reply_markup=settingsInlineMarkup)

async def handleCityWeather(message: Message, city: str):

    unit_system = usersDB.getUnitSystemFromUser(uID=message.chat.id)
    
    # Create WeatherReport instance to receive and process weather info
    weather = WeatherReport(city=city, unit_system=unit_system)

    # Get weather info and catching errors to res variable
    res = weather.getWeatherData(weather.URL())

    if res:

        # Send appropriate error message to user if there're any errors
        await message.answer(res, reply_markup=mainMenuMarkup)
    else:

        # Get formatted weather info to show it to user
        weather = weather.beautify()

        # Send desired city/region weather to user
        await message.answer(weather, reply_markup=mainMenuMarkup)

@dp.message()
async def handleUserCityInput(message: Message):

    commandChain = usersDB.getCommand(uID=message.chat.id)
    place = message.text
    places = usersDB.getFeaturedPlaces(uID=message.chat.id)
    
    if commandChain == "addFeaturedPlace":
        if place in places:
            await message.answer(text=f"⚠ {hbold(place)} already exists in {hbold('Featured Places')}! "
                                 "Specify a more precise name or add other place.")
        else:
            if len(places) < 5:
                usersDB.setCommand(uID=message.chat.id, chain="")
                usersDB.addPlaceToFeaturedList(uID=message.chat.id, place=place)
                await message.answer(text=f"✅ {hbold(place)} added to the {hbold('Featured Places')}! ")
            else:
                await message.answer(text=f"⚠ List of {hbold('Featured Places')} is full! "
                                     "Delete any place to free up the list.")
    elif commandChain == "removeFeaturedPlace":
        usersDB.setCommand(uID=message.chat.id, chain="")
        usersDB.removePlaceFromFeatured(uID=message.chat.id, place=message.text)
    else:
        if message.location:
            coordinates = (message.location.latitude, message.location.longitude)

            location = Location(coordinates[0], coordinates[1])

            query_url = location.URL()

            city = location.handleCoordinatesAsCityName(query_url=query_url)

        else:
            city = place

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
