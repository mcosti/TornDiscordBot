# Torn Discord Bot

This library is used for fetching [Torn City](https://www.torn.com) user's data and sending them relevant notifications in private messages.

![Torn alerts](https://i.imgur.com/gA09oaW.png)
## Features
- events and messages notifications
- energy, nerve or life full
- arrived at your destination
- cooldowns ended
- got out of jail/hospital
- stock notifications in separate channels

## Installation
You will need a Discord bot and a Firebase realtime database for this.  You can find tutorials online on how to obtain those. 

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pipenv.

```bash
sudo pip3 install pipenv 
# used for package managing, sudo so it's available globally
git clone https://github.com/mcosti/TornDiscordBot
cd TornDiscordBot
pipenv shell
pipenv install
python bot.py
```
Also remember to copy .env.example to .env and fb/db_cert_example.json to fb/db_cert.json and edit it accordingly
## Running as a Linux service
This is useful if you want to have it running non-stop on your Ubuntu server.  

You have to edit discord.service file according to your project setup and location.

```
sudo cp discord.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable discord # if you want it to run at startup
sudo systemctl start discord
```

## Usage
After you have successfully created your bot, added it to your server and ran this script, you can send it a private message "!help" to find out how to use (or just read cogs/settings.py)

## Sentry
You can integrate sentry by simply adding your project DSN to .env. This is very useful for debugging
## Checking logs
```
sudo journalctl -u discord -f
```

## Bugs
- Due to the way async works in Python3, if there is any unhandled exception in the alerts_task it will halt completely, but the bot and the other task (stocks) will keep running. For this you have to restart the server
- HTTP exceptions are not handled

## Todos

- Add testing (I suggest using pytest)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)