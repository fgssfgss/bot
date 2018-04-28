### "Железяка"
Simple bot for Jabber, and VK, and Skype, Telegram, Discord.

### New goals
- Full re-design.
- Python 3 only
- Support Modules(Jabber, VK, /*Maybe Skype-over-dbus*/).
- Multithreaded.
- SQLite3 multithread wrapper(Manager with Queue of transanctions, and worker threads, which adds job to Queue).

### Dependencies
- vk_api
- pyTelegramBotAPI
- sqlite3
- discord.py

### How to use
##### Run as:

``python3 main.py config.json``

You can use database.db with some existing phrases. Or create new one(set non existent file in config).
##### Commands:
- !on - enable bot
- !off - disable bot(he will listen for phrases and put them into db)
- !q - generate phrase with some word