from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import emoji
start_option = KeyboardButton(f'start {emoji.FAST_DOWN_BUTTON}')
time_option = KeyboardButton(f'time {emoji.ALARM_CLOCK}')
info_option = KeyboardButton(f'info {emoji.INFORMATION}')
id_option = KeyboardButton(f'my_id {emoji.CREDIT_CARD}')
play_option = KeyboardButton(f'game {emoji.PLAY_BUTTON}')
rock_paper_scissors_game_option = KeyboardButton(f'/rock_paper_scissors {emoji.ROCK}')
rock_option = KeyboardButton(f'rock {emoji.ROCK}')
paper_option = KeyboardButton(f'paper {emoji.ROLLED_UP_NEWSPAPER}')
scissors_option = KeyboardButton(f'scissors {emoji.SCISSORS}')
quest_option = KeyboardButton(f'quest {emoji.CITYSCAPE}')
return_option = KeyboardButton(f'return {emoji.MAN_WALKING}')
return_option_2 = KeyboardButton(f'return {emoji.MAN_WALKING}')
create_image = KeyboardButton('image_create')
guess_number = KeyboardButton(f'guess_number {emoji.INPUT_NUMBERS}')

kb_main = ReplyKeyboardMarkup(
    keyboard=[
        [start_option, time_option, id_option, info_option],
        [play_option, create_image]
    ],
resize_keyboard = True,
)

kb_main_2 = ReplyKeyboardMarkup(
    keyboard=[
        [rock_paper_scissors_game_option, guess_number],
        [quest_option, return_option],
    ],
resize_keyboard = True,
)

kb_main_3 = ReplyKeyboardMarkup(
    keyboard=[
        [rock_option, paper_option, scissors_option],
        [return_option_2],
    ],
resize_keyboard = True,
)

inline_kb_start_quest = InlineKeyboardMarkup([
    [InlineKeyboardButton('complete quest', callback_data='start_quest')]
])

inline_kb_choice_door = InlineKeyboardMarkup([
    [InlineKeyboardButton(f'{emoji.DOOR + emoji.LEFT_ARROW}', callback_data='left_door')],
    [InlineKeyboardButton(f'{emoji.DOOR + emoji.RIGHT_ARROW}', callback_data='right_door')],
])
inline_kb_left_door = InlineKeyboardMarkup([
    [InlineKeyboardButton(f'{emoji.MUSHROOM + emoji.ANGRY_FACE} Fight the fat angry Mushroom!', callback_data='fight_mushroom')],
    [InlineKeyboardButton(f'{emoji.MAN_RUNNING + emoji.LEFT_ARROW} run run as fast as you can!', callback_data='run_away')],
])
inline_kb_right_door = InlineKeyboardMarkup([
    [InlineKeyboardButton(f'{emoji.CROWN} golden crown', callback_data='golden_crown')],
    [InlineKeyboardButton(f'{emoji.FLAG_CHRISTMAS_ISLAND} pick up gods item {emoji.CHRISTMAS_TREE}', callback_data='pick_up_god_item')],
    [InlineKeyboardButton(f'{emoji.CROSSED_SWORDS} a cool sword!', callback_data='sword_pick_up')]
])
inline_return_to_choice_doors = InlineKeyboardMarkup([
    [InlineKeyboardButton(f'{emoji.SUN_BEHIND_CLOUD} go back', callback_data='return_to_choice_doors')],
])