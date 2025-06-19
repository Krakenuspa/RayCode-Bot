import discord
from discord.ext import commands
from discord import app_commands
import os.path

DEBUG = False

DATA_FILE = "./data.txt"
SYMBOLS_PATH = "./symbols/"
DEFAULT_SYMBOLS  = "dot\ndash\nletter_separator\nword_separator"
CHARACTER_LIMIT = 2000

ENCODE_TWITCH = "twitch_encode"
ENCODE_DISCORD = "discord_encode"
DECODE = "decode"

with open(DATA_FILE, "r") as f:
        l = [line.rstrip() for line in f]
f.close()

TOKEN_STABLE = l[0]
TOKEN_DEBUG  = l[1]

DEBUG_SERVER_ID = l[2]
ALLOWED_SERVER_IDS = l[3:]

symbols_dict = {}

encode_dict = {
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
    " ": "/"
}

decode_dict = {
    ".-"    : "a",
    "-..."  : "b",
    "-.-."  : "c",
    "-.."   : "d",
    "."     : "e",
    "..-."  : "f",
    "--."   : "g",
    "...."  : "h", 
    ".."    : "i", 
    ".---"  : "j", 
    "-.-"   : "k",
    ".-.."  : "l",
    "--"    : "m",
    "-."    : "n",
    "---"   : "o",
    ".--."  : "p",
    "--.-"  : "q",
    ".-."   : "r",
    "..."   : "s",
    "-"     : "t",
    "..-"   : "u",
    "...-"  : "v",
    ".--"   : "w",
    "-..-"  : "x",
    "-.--"  : "y",
    "--.."  : "z",
    "/"     : " "
}

def encode_msg(msg: str, twitch: bool, guild_id: int) -> str:
    if msg == "": return "Can't encode empty message."
    msg = msg.lower()
    result_string = ""
    i = 0

    used_to_dict = symbols_dict[guild_id][ENCODE_TWITCH] if twitch else symbols_dict[guild_id][ENCODE_DISCORD]

    while i < len(msg):
        if msg[i] not in encode_dict: return f"Can't encode message because it contains un-assigned character: {msg[i]}"
        for symbol in encode_dict[msg[i]]:
            result_string += " " + used_to_dict[symbol]
        if (msg[i] != " ") and ((i+1) != len(msg)) and (msg[i+1] != " "):
            result_string += " " + used_to_dict[" "]
        i+=1

    return result_string

def decode_msg(msg: str, guild_id: int) -> str:
    if msg == "": return "Can't decode empty message."
    result_string = ""
    current_letter_morse = ""
    symbol_list = msg.split(" ")

    used_from_dict = symbols_dict[guild_id][DECODE]

    for symbol in symbol_list:

        if (symbol == symbols_dict[guild_id][ENCODE_TWITCH][" "]) or (symbol == symbols_dict[guild_id][ENCODE_TWITCH]["/"]) or (symbol == symbols_dict[guild_id][ENCODE_DISCORD][" "]) or (symbol == symbols_dict[guild_id][ENCODE_DISCORD]["/"]):
            result_string += decode_dict[current_letter_morse]
            current_letter_morse = ""

            if (symbol == symbols_dict[guild_id][ENCODE_TWITCH]["/"]) or (symbol == symbols_dict[guild_id][ENCODE_DISCORD]["/"]): result_string += " "
            continue
        
        if symbol == "": continue

        if symbol not in used_from_dict:
            return f"Can't decode message because it contains un-assigned symbol: {symbol}"
        current_letter_morse += used_from_dict[symbol]
    
    if (current_letter_morse != ""): result_string += decode_dict[current_letter_morse]

    return result_string

def update_raycode(morse: str, new_raycode: str, twitch: bool, guild_id: int) -> int:
    if new_raycode == "": return -1
    if " " in new_raycode: return -2
    if new_raycode in symbols_dict[guild_id][DECODE] and symbols_dict[guild_id][DECODE][new_raycode] != morse: return -3

    if twitch:
        used_to_dict = symbols_dict[guild_id][ENCODE_TWITCH]        
        savefile_path = SYMBOLS_PATH + str(guild_id) + "/twitch.txt"

    else:
        used_to_dict = symbols_dict[guild_id][ENCODE_DISCORD]
        savefile_path = SYMBOLS_PATH + str(guild_id) + "/discord.txt"

    used_from_dict = symbols_dict[guild_id][DECODE]

    del used_from_dict[used_to_dict[morse]]

    used_to_dict[morse] = new_raycode
    used_from_dict[new_raycode] = morse

    with open(savefile_path, "w") as f:
        f.write(used_to_dict["."] + "\n")
        f.write(used_to_dict["-"] + "\n")
        f.write(used_to_dict[" "] + "\n")
        f.write(used_to_dict["/"])
    f.close()

    return 0

async def send_error_msg(interaction: discord.Interaction, error_id: int) -> None:
    match(error_id):
        case -1: await interaction.response.send_message(f"RayCode symbol can't be nothing, RayCode wasn't updated", ephemeral=True)
        case -2: await interaction.response.send_message(f"RayCode symbol can't contain spaces, RayCode wasn't updated", ephemeral=True)
        case -3: await interaction.response.send_message(f"Same RayCode symbol can't have different meaning on twitch and discord, RayCode wasn't updated", ephemeral=True)
    
    if(error_id < -2):
        await interaction.response.send_message(f"Unknown error detected, please screenshot the message that caused this and contant the bot creater: Krakenuspa", ephemeral=True)

class Client(commands.Bot):
    async def on_ready(self):
        if DEBUG: print('Bot Initialized (DEBUG)')
        else: print('Bot Initialized (STABLE)')

        try:
            for allowed_id in ALLOWED_SERVER_IDS:
                if(DEBUG): allowed_id = DEBUG_SERVER_ID

                guild = discord.Object(id=allowed_id)
                synced = await self.tree.sync(guild=guild)
                print(f"synced {len(synced)} commands to guild {guild.id}")
                
                if(DEBUG): break

        except Exception as e:
            print(f"Error syncing cmds: {e}")

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix = '!', intents = intents)

for allowed_id in ALLOWED_SERVER_IDS:
    if(DEBUG): allowed_id = DEBUG_SERVER_ID
    guild_id = discord.Object(id=allowed_id)

    server_dir   = SYMBOLS_PATH + str(allowed_id) + "/"
    twitch_file  = server_dir + "twitch.txt"
    discord_file = server_dir + "discord.txt"

    if(not os.path.isdir(server_dir)):
        os.mkdir(server_dir)

    if(not os.path.isfile(twitch_file)):
        with open(twitch_file, "x") as f:
            f.write(DEFAULT_SYMBOLS)
        f.close()

    with open(twitch_file, "r") as f:
        l = [line.rstrip() for line in f]
    f.close()

    encode_dict_twitch = {
    "." : l[0],
    "-" : l[1],
    " " : l[2],
    "/" : l[3]
    }

    decode_dict_twitch = {
        l[0] : ".",
        l[1] : "-",
        l[2] : " ",
        l[3] : "/"
    }

    if(not os.path.isfile(discord_file)):
        with open(discord_file, "x") as f:
            f.write(DEFAULT_SYMBOLS)
        f.close()

    with open(discord_file, "r") as f:
        l = [line.rstrip() for line in f]
    f.close()

    encode_dict_discord = {
    "." : l[0],
    "-" : l[1],
    " " : l[2],
    "/" : l[3]
    }

    decode_dict_discord = {
        l[0] : ".",
        l[1] : "-",
        l[2] : " ",
        l[3] : "/"
    }

    server_symbol_dict = {
        ENCODE_TWITCH  : encode_dict_twitch,
        ENCODE_DISCORD : encode_dict_discord,
        DECODE : decode_dict_discord | decode_dict_twitch,
    }

    symbols_dict[allowed_id] = server_symbol_dict

    ### COMMANDS ↓ ###

    @client.tree.command(name="encode", description=f"Encodes text into RayCode", guild=guild_id)
    async def encode(interaction: discord.Interaction, message: str, twitch: bool = False):
        encoded_msg = encode_msg(message, twitch, interaction.guild_id)

        if len(encoded_msg) > CHARACTER_LIMIT:
            await interaction.response.send_message("Encoded message is longer than allowed length of discord msg (2K characters)", ephemeral=True)
        else:
            await interaction.response.send_message(encoded_msg, ephemeral=True)

    @client.tree.command(name="decode", description="Decodes RayCode into text", guild=guild_id)
    async def decode(interaction: discord.Interaction, message: str):
        decoded_msg = decode_msg(message, interaction.guild_id)
        await interaction.response.send_message(decoded_msg, ephemeral=True)

    @client.tree.command(name="change_dot_text", description="Update text for dot in RayCode", guild=guild_id)
    async def change_dot_text(interaction: discord.Interaction, new_text: str, twitch: bool = False):
        error = update_raycode(".", new_text, twitch, interaction.guild_id)
        if twitch: platform = "Twitch"
        else: platform = "Discord"

        if error == 0:
            await interaction.response.send_message(f"Dot in RayCode {platform}, from now on, will be: {new_text}", ephemeral=True)
        else:
            await send_error_msg(interaction, error)

    @client.tree.command(name="change_dash_text", description="Update text for dash in RayCode", guild=guild_id)
    async def change_dash_text(interaction: discord.Interaction, new_text: str, twitch: bool = False):
        error = update_raycode("-", new_text, twitch, interaction.guild_id)
        if twitch: platform = "Twitch"
        else: platform = "Discord"

        if error == 0:
            await interaction.response.send_message(f"Dash in RayCode {platform}, from now on, will be: {new_text}", ephemeral=True)
        else:
            await send_error_msg(interaction, error)

    @client.tree.command(name="change_letter_separator", description="Update text for letter seperator in RayCode", guild=guild_id)
    async def change_letter_seperator(interaction: discord.Interaction, new_text: str, twitch: bool = False):
        error = update_raycode(" ", new_text, twitch, interaction.guild_id)
        if twitch: platform = "Twitch"
        else: platform = "Discord"

        if error == 0:
            await interaction.response.send_message(f"Letter separator in RayCode {platform}, from now on, will be: {new_text}", ephemeral=True)
        else:
            await send_error_msg(interaction, error)

    @client.tree.command(name="change_word_separator", description="Update text for word seperator in RayCode", guild=guild_id)
    async def change_word_seperator(interaction: discord.Interaction, new_text: str, twitch: bool = False):
        error = update_raycode("/", new_text, twitch, interaction.guild_id)
        if twitch: platform = "Twitch"
        else: platform = "Discord"

        if error == 0:
            await interaction.response.send_message(f"Word separator in RayCode {platform}, from now on, will be: {new_text}", ephemeral=True)
        else:
            await send_error_msg(interaction, error)

    if(DEBUG): break

if DEBUG: client.run(TOKEN_DEBUG)
else: client.run(TOKEN_STABLE)