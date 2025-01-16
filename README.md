### cpmessage
Receive Webhooks from Streamer Copilot and send Formatted Message to Telegram.


#### Screenshot

![grafik](https://github.com/user-attachments/assets/d3ebd9c5-d7a5-4e95-bf54-4697aa3a5198)


## 1. Prerequisites 

There are a few requirements for cpmessage which are listed below.

1. **VPS:** Virtual private server or other computer that is publicly accessible via a web domain.
2. **Telegram Bot:** Create a Telegram bot via [BotFather](https://t.me/BotFather) and obtain your bot token.
3. **Chat ID:** Use the [@userinfobot](https://t.me/userinfobot) on Telegram to find your User ID = chat ID.

---
## 2. Installation
### 2.1 Clone the Repository 
```
git clone https://github.com/DoktorShift/cpmessage.git
cd cpmessage
```

---
### 2.2 Installing Dependencies in a Virtual Environment
The dependencies are installed in a virtual environment so that they are isolated from the system. Even “pip” is not installed on every system from the outset, so here are a few preparations.
```bash
sudo apt-get update
sudo apt install python3-venv
sudo apt install python3-pip
```
Now we set up a virtual environment, activate it and install the dependencies in it.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
__Note:__ You can deactivate the editing mode of the virtual environment. It remains valid for the application. To reactivate the editing mode for the virtual environment, e.g. to update a dependency, you must first select the folder to which the virtual environment applies and then activate the virtual environment. 
```bash
# deactivate venv editing
deactivate
# activate venv editing
cd ~/naughtify
source venv/bin/activate
```

---
### 2.3 Configure the Environment
Settings are applied and parameters are transferred here.
1. Copy the `.env` and open it.
```bash
wget https://raw.githubusercontent.com/DoktorShift/cpmessage/refs/heads/main/example.env
mv example.env .env
sudo nano .env
```
2. Fill in for BOT Token & Chat ID:
- Telegram Bot Token
- Chat ID (User ID)

These are heavily needed

### 3. Start the app
```bash
python3 app.py
```

🥳
