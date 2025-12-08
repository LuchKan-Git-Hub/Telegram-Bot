<a href="https://python-telegram-bot.org">
  <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh2mF9vSCghP634W8z8FshKsP0U4wSqwHucKBd01ezVWG3Hsr0Mh1ZhcnpXIMPruAD8GeUS5MjyfLjNhXYhu7VyGVT4l6rVTNGHY1j4_4GBkQhztWTIfwCkb4-7g_MBtL2cqJ_G4lYOtiRw/s1600/photo_2019-07-01_18-49-10.jpg" alt="Python Telegram Bot Logo" style="width:300px; border-radius:15px;">
</a>

# Telegram Bot

Welcome to the **Telegram Bot** repository! 🎉  

This project simplifies and enhances your interaction with Telegram. It automates tasks, provides fun features, and gives you a hands-on way to explore Python and bot development.  

It’s also a **learning-friendly open-source project**, perfect for beginners or anyone curious about Python, async programming, and Telegram API.

---

## Features 🚀
- **Custom Commands:** `/start`, `/info`, `/game`, `/time`, `/my_id`, `/image`, `/rock_paper_scissors`, `/quest`, and more.
- **Interactive Games:** Rock-Paper-Scissors, guess-the-number, and small quests with multiple endings.
- **AI Image Generation:** Generate images using `FusionBrain_AI`.
- **User Tracking:** Manages users with SQLite, including coins and inventory.
- **Buttons & Inline Keyboards:** Easy-to-use interactive buttons, so users don’t have to type commands.
- **Beginner-Friendly Code:** Modular, commented, and easy to read for anyone learning Python.

---

## Built With 🛠️
- **[Pyrogram](https://docs.pyrogram.org/):** Powers bot interaction with Telegram API.
- **SQLite Database:** Stores user info, coins, and inventory in a lightweight SQL database.
- **Fusion Brain AI:** Provides image generation functionality.
- **Kandinsky.py:** Optional for advanced AI features.
- **Python 3.10+**: Uses async features and modern Python libraries.

---

## Configuration ⚙️
1. Open Telegram and search for **BotFather** to create a new bot and get your **API token**.
2. Insert the token in `config.py`:

```python
API_ID = YOUR_API_ID
API_HASH = "YOUR_API_HASH"
API_TOKEN = "YOUR_BOT_TOKEN"
