from pyrogram import Client, filters
import config
import datetime
import Keyboard
import random
# import json
import sqlite3
from Keyboard import kb_main, kb_main_3, kb_main_2
from FusionBrain_AI import generate
import base64
from pyrogram.types import ForceReply

# connect database
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Create the bot instance
bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.API_TOKEN,
    name='Botchik'
)

# Helper: Button filter function for custom filters
def button_filter(button):
    async def func(_, __, msg):
        return msg.text == button.text

    return filters.create(func, "ButtonFilter", button=button)

# Command: /start
@bot.on_message(filters.command('start') | button_filter(Keyboard.start_option))
async def reply_start(bot, message):
    await bot.send_sticker(
        message.chat.id,
        "CAACAgIAAxkBAAENLhBnPhNSct_FCoK6HrLHzzMp8f69ogACAQEAAladvQoivp8OuMLmNDYE",
        reply_markup=Keyboard.kb_main
    )

    # searching for user in database
    cursor.execute("SELECT * FROM users WHERE id = ?", (message.from_user.id,))
    result = cursor.fetchone()

    # if user is not found, create new user in database
    if result is None or message.from_user.id != result[0]:
        cursor.execute("INSERT INTO users (id, int) VALUES (?, ?)", (message.from_user.id, 100))
        connection.commit()


# Command: /game
@bot.on_message(filters.command('game') | button_filter(Keyboard.play_option))
async def games(bot, message):
    # searching for user in database
    cursor.execute("SELECT id, int FROM users WHERE id = ?", (message.from_user.id,))
    result = cursor.fetchone()
    if result is None or message.from_user.id != result[0]:
        await message.reply("You are not registered yet. Please use /start.")
        return

    user_coins = result[1]  # get the int value (second column) if needed

    if user_coins >= 10:
        await message.reply("Choosing game...", reply_markup=Keyboard.kb_main_2)
    else:
        await message.reply("Not enough coins - 10 coins are needed to play!")


# Command: /rock_paper_scissors or button click
@bot.on_message(filters.command('rock_paper_scissors') | button_filter(Keyboard.rock_paper_scissors_game_option))
async def choose_rock_paper_scissors(bot, message):
    await message.reply("Choose Rock, Paper, or Scissors:", reply_markup=kb_main_3)


# Command: /info or info button
@bot.on_message(filters.command('info') | button_filter(Keyboard.info_option))
async def show_info(bot, message):
    await message.reply(
        "/start - Initialize the bot\n"
        "/time - Check the current time\n"
        "/info - List available commands\n"
        "/my_id - Get your Telegram ID\n"
        "/game - Play a game"
    )


# Command: /time
@bot.on_message(filters.command('time') | button_filter(Keyboard.time_option))
async def show_time(bot, message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await message.reply(f"The current time is: {current_time}")


# Command: /my_id
@bot.on_message(filters.command('my_id') | button_filter(Keyboard.id_option))
async def show_my_id(bot, message):
    await message.reply(f"Your ID is: {message.from_user.id}")


# Command: /quest option
@bot.on_message(filters.command('quest') | button_filter(Keyboard.quest_option))
async def kvest(bot, message):
    await message.reply_text('Do you want to explore the world?', reply_markup=Keyboard.inline_kb_start_quest)

# Callback queries (e.g., quest logic)
@bot.on_callback_query()
async def handle_query(bot, query):
    # executing from data_base
    cursor.execute("SELECT id, int FROM has_sword WHERE id = ?", (query.from_user.id,))
    result = cursor.fetchone()

    # Ensure the user has an entry in the "has_sword" dictionary
    if result is None or query.from_user.id != result[0]:
        cursor.execute("INSERT INTO has_sword (id, int) VALUES (?, ?)", (query.from_user.id, 0))
        connection.commit()
    elif query.data == "sword_pick_up":
        # Instead of modifying the tuple, directly update the database
        cursor.execute("UPDATE has_sword SET int = 1 WHERE id = ?", (query.from_user.id,))
        connection.commit()
    try:
        if query.data == "start_quest" or query.data == "return_to_choice_doors":
            await query.message.reply_text(
                'You stand near two doors. Which one will you pick?',
                reply_markup=Keyboard.inline_kb_choice_door
            )
            await bot.answer_callback_query(
                query.id,
                text="You stand near two doors. Which one will you pick?",
                show_alert=True)

        elif query.data == "left_door":
            await query.message.reply_text(
                'A big, fat, angry mushroom looks at you. He is very angry!',
                reply_markup=Keyboard.inline_kb_left_door
            )
            await bot.answer_callback_query(
                query.id,
                text="A big, fat, angry mushroom looks at you. He is very angry!",
                show_alert=True)

        elif query.data == "right_door":
            await query.message.reply_text(
                'You open the right door and see three items. They look awesome!\n'
                'You see a golden crown, a god item, and a sword.',
                reply_markup=Keyboard.inline_kb_right_door
            )
            await bot.answer_callback_query(
                query.id,
                text="You open the right door and see three items. They look awesome!\n",
                show_alert=True,
            )

        elif query.data == "fight_mushroom":
            if result[1] == 0:
                await query.message.reply_text(
                    'You fight the mushroom with bare hands. Of course, you died. What did you expect?\nLoser ending!'
                )
                await bot.answer_callback_query(
                    query.id,
                    text="You fight the mushroom with bare hands. Of course, you died. What did you expect?\nLoser ending!",
                    show_alert=True,
                )
            else:
                await query.message.reply_text('You fight the mushroom with your sword. You win!')
                await bot.answer_callback_query(
                    query.id,
                    text="You fight the mushroom with your sword. You win!",
                    show_alert=True,
                )
                # Update the database directly instead of modifying the tuple
                cursor.execute("UPDATE has_sword SET int = 0 WHERE id = ?", (query.from_user.id,))
                connection.commit()

        elif query.data == "run_away":
            await query.message.reply_text(
                'You run, run, run for days until you get tired,\nand the big mushroom finally catches you and eats you. Stupid ending!'
            )
            await bot.answer_callback_query(
                query.id,
                text='You run, run, run for days until you get tired,\nand the big mushroom finally catches you and eats you. Stupid ending!',
                show_alert=True,
            )

        elif query.data == "sword_pick_up":
            await query.message.reply_text(
                'You pick up the sword. +1 sword',
                reply_markup=Keyboard.inline_return_to_choice_doors
            )
            await bot.answer_callback_query(
                query.id,
                text="You pick up the sword. +1 sword",
                show_alert=True,
            )

        elif query.data == "golden_crown":
            await query.message.reply_text('you become the king and live happily no one knows ending')
            await bot.answer_callback_query(
                query.id,
                text="you become the king and live happily no one knows ending",
                show_alert=True,
            )

        elif query.data == "pick_up_god_item":
            await query.message.reply_text('you touched the god item then died you are not god ending!')
            await bot.answer_callback_query(
                query.id,
                text='you touched the god item then died you are not god ending!',
                show_alert=True,
            )

    except KeyError as e:
        await query.message.reply_text(f"An unexpected error occurred: {e}. Please try again later!")
    except Exception as e:
        await query.message.reply_text(f"An error occurred: {e}")


@bot.on_message(filters.command('image'))
async def create_image(bot, message):
    if len(message.text.split()) > 1:
        query = message.text.replace('/create_image', '')
        await message.reply_text('generating image it will take few minutes...')
        images = await generate(query)
        if images:
            image_data = base64.b64decode(images[0])
            img_num = random.randint(1, 99)
            with open(f'images/image{img_num}.jpg', 'wb') as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id, f'image.jpg',
                                 reply_to_message_id=message.id,
                                 reply_Markup=Keyboard.kb_main,
            )
        else:
            await message.reply_text("ERROR:",
                                     reply_to_message_id=message.id,
                                     reply_markup=Keyboard.kb_main,)
    else:
        await message.reply_text("type your output")
query_text = "Type your input to generate"
@bot.on_message(button_filter(Keyboard.create_image))
async def image_command(bot, message):
    await message.reply(query_text,
                        reply_markup=ForceReply(True))

query_text_2 = "Guess the number"
@bot.on_message(button_filter(Keyboard.guess_number))
async def image_command(bot, message):
    await message.reply(query_text_2,
                        reply_markup=ForceReply(True)),
random_num = random.randint(1, 100)
@bot.on_message(filters.reply)
async def reply(bot, message):
    if message.reply_to_message.text == query_text:
        query = message.text
        await message.reply_text('generating image it will take few minutes...')

        images = await generate(query)
        if images:
            image_data = base64.b64decode(images[0])
            img_num = random.randint(1, 99)
            with open(f'images/image{img_num}.jpg', 'wb') as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id, f'images/image{img_num}.jpg',
                                 reply_to_message_id=message.id,
                                 reply_markup=Keyboard.kb_main,
            )
        else:
            await message.reply_text("ERROR:",
                                     reply_to_message_id=message.id,
                                     reply_markup=Keyboard.kb_main)
    elif message.reply_to_message.text == query_text_2:
        if message.text == str(random_num):
                await message.reply_text(f"you right the number {random_num} is right one")
        else:
            # create the number is smaller or the number is bigger
            if random_num > int(message.text):
                await message.reply_text('The number is bigger')
            else:
                await message.reply_text('The number is smaller')
    else:
        print(message.reply_to_message.text,query_text_2)
# Command: /return
@bot.on_message(filters.command('return') | button_filter(Keyboard.return_option))
async def returns(bot, message):
    await message.reply("Returned to the main menu.", reply_markup=Keyboard.kb_main)


# Rock-Paper-Scissors game logic
@bot.on_message(button_filter(Keyboard.rock_option) |
                button_filter(Keyboard.paper_option) |
                button_filter(Keyboard.scissors_option))
async def choice_rps(bot, message):
    cursor.execute("SELECT id, int FROM users WHERE id = ?", (message.from_user.id,))
    result = cursor.fetchone()

    # Convert tuple values to variables
    user_id, user_balance = result

    user_choice = message.text
    bot_choice = random.choice(
        [Keyboard.rock_option.text, Keyboard.paper_option.text, Keyboard.scissors_option.text]
    )

    # Calculate the game result
    if user_choice == bot_choice:
        results = "It's a draw!"
    elif (user_choice == Keyboard.rock_option.text and bot_choice == Keyboard.scissors_option.text) or \
            (user_choice == Keyboard.scissors_option.text and bot_choice == Keyboard.paper_option.text) or \
            (user_choice == Keyboard.paper_option.text and bot_choice == Keyboard.rock_option.text):
        results = "You win!"
        user_balance += 10
    else:
        results = "You lose!"
        user_balance = max(0, user_balance - 10)  # Ensure no negative balance

    # Save updated user data
    cursor.execute("UPDATE users SET int = ? WHERE id = ?", (user_balance, user_id))
    connection.commit()

    # Reply with the game result
    await message.reply(f"{results} The bot chose: {bot_choice}. Your balance: {user_balance} coins.")

# Run the bot
bot.run()