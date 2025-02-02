from pyrogram import Client, filters
import config
import datetime
import Keyboard
import random
import json
from Keyboard import kb_main, kb_main_3, kb_main_2
from FusionBrain_AI import generate
import base64
from pyrogram.types import ForceReply

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


# Helper: Read from JSON safely
def read_json(file_name, default_value):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default_value


# Helper: Write to JSON safely
def write_json(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file)


# Command: /start
@bot.on_message(filters.command('start') | button_filter(Keyboard.start_option))
async def reply_start(bot, message):
    await bot.send_sticker(
        message.chat.id,
        "CAACAgIAAxkBAAENLhBnPhNSct_FCoK6HrLHzzMp8f69ogACAQEAAladvQoivp8OuMLmNDYE",
        reply_markup=Keyboard.kb_main
    )

    users = read_json('users.json', {})
    user_id = str(message.from_user.id)

    # Initialize user if not present
    if user_id not in users:
        users[user_id] = 100  # Start with 100 coins
        write_json('users.json', users)  # Save updated data


# Command: /game
@bot.on_message(filters.command('game') | button_filter(Keyboard.play_option))
async def games(bot, message):
    users = read_json('users.json', {})
    user_id = str(message.from_user.id)

    if user_id not in users:
        await message.reply("You are not registered yet. Please use /start.")
        return

    if users[user_id] >= 10:
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
    has_sword = read_json('has_sword.json', {})  # Load sword data
    has_sword_id = str(query.from_user.id)  # Convert user ID to string for JSON compatibility
    # Ensure the user has an entry in the "has_sword" dictionary
    if has_sword_id not in has_sword:
        has_sword[has_sword_id] = 0  # Default value: no sword
        write_json('has_sword.json', has_sword)  # Save newly added user data to the file

    try:
        if query.data == "start_quest" or query.data == "return_to_choice_doors":
            await query.message.reply_text(
                'You stand near two doors. Which one will you pick?',
                reply_markup=Keyboard.inline_kb_choice_door
            )
            # Handle different callback query data
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
            if has_sword[has_sword_id] == 0:
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
                has_sword[has_sword_id] = 0
                write_json('has_sword.json', has_sword)  # Save updated sword data
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
            has_sword[has_sword_id] = 1  # User picks up the sword
            write_json('has_sword.json', has_sword)  # Save updated sword data
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
random_num = random.randint(1, 10)
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
            await message.reply_text('Plz try again')
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
    users = read_json('users.json', {})
    user_id = str(message.from_user.id)

    if user_id not in users:
        users[user_id] = 100  # Initialize with 100 coins

    user_choice = message.text
    bot_choice = random.choice(
        [Keyboard.rock_option.text, Keyboard.paper_option.text, Keyboard.scissors_option.text]
    )

    # Calculate the game result
    if user_choice == bot_choice:
        result = "It's a draw!"
    elif (user_choice == Keyboard.rock_option.text and bot_choice == Keyboard.scissors_option.text) or \
            (user_choice == Keyboard.scissors_option.text and bot_choice == Keyboard.paper_option.text) or \
            (user_choice == Keyboard.paper_option.text and bot_choice == Keyboard.rock_option.text):
        result = "You win!"
        users[user_id] += 10
    else:
        result = "You lose!"
        users[user_id] = max(0, users[user_id] - 10)  # Ensure no negative balance

    # Save updated user data
    write_json('users.json', users)

    # Reply with the game result
    await message.reply(f"{result} The bot chose: {bot_choice}. Your balance: {users[user_id]} coins.")





# Run the bot
bot.run()