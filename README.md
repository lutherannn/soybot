# soybot
SoyBot, the lackluster, featureless, discord bot.
# Library Requirements
Install required packages with pip:
	pip install -r requirements.txt
# Also Needed
Discord api key in a file named .env with the entry being: DISCORD\_TOKEN=yourtoken<br>
A file named names.txt for the wheel function, with the names being separated by a new line<br>
A file named responses.txt for the responses to "hey soybot" with the responses separated by a new line<br>
The archive command writes to the local disk, so make sure it has permissions to write to the current working directory, or errors will be thrown
# Install
To install soybot for a dev environment, you can run setup.py and that will guide you through the process<br>
Soybot is formatted in accordance with pep8 standards, this is done by using [black](https://github.com/psf/black)<br>
You can install black by using pip install black, and then add it to your path<br>
To format soybot using black, run black soybot.py, or use it in your text editor of choice.<br>
