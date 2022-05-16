# soybot
SoyBot, the lackluster, featureless, discord bot.
# Library Requirements
discord-py, aiohttp, dotenv, udpy<br>
Install required packages with pip:
	pip install -r requirements.txt
# Also Needed
Discord api key in a file named .env with the entry being: DISCORD\_TOKEN=yourtoken<br>
A file named names.txt for the wheel function, with the names being separated by a new line<br>
A file named responses.txt for the responses to "hey soybot" with the responses separated by a new line<br>
The archive command writes to the local disk, so make sure it has permissions to write to the current working directory, or errors will be thrown
