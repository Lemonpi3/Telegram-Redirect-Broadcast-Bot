# Telegram-Redirect-Broadcast-Bot
Gets messages from groups and redirects them to other groups

### Usage

* First load chatsdb.xlsx with inputs and outputs. Currently suports 1:X input:output ratio to add multiple outputs split them with ';' in this pattern "CHAT 1;CHAT 2". Example:
![](/imgs/SharedScreenshot.jpg)
* Second (you can ignore this step) if you want to get the ids of the groups (I can't load IDs directly from the dataframe to the bot since the api needs to cache the chats) or deleted chatsdb.xlsx run chatdb.py and will automatically fill the corresponding id columns (for multiple ids per row they will be splited with ';' )
* Third run main.py and the bot should be working.
