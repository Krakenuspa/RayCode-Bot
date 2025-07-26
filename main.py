from discord.ext import commands
from dotenv import load_dotenv
from raycode import raycode
from os import getenv
import discord

DEBUG: bool = False

ENV_FILE_SECRET: str = "./data.env.secret"
ENV_FILE_SHARED: str = "./data.env.shared"
load_dotenv(ENV_FILE_SECRET)
load_dotenv(ENV_FILE_SHARED)

TOKEN_STABLE:      str | None = getenv('TOKEN_STABLE')
TOKEN_DEBUG:       str | None = getenv('TOKEN_DEBUG')

temp_id: str | None = getenv('ALLOWED_SERVER_ID')
ALLOWED_SERVER_ID: int | None = int(temp_id) if temp_id != None else None

temp_id: str | None = getenv('DEBUG_SERVER_ID')
DEBUG_SERVER_ID:   int | None = int(temp_id) if temp_id != None else None

USED_TOKEN: str | None = TOKEN_DEBUG if DEBUG else TOKEN_STABLE
GUILD_ID: int | None = DEBUG_SERVER_ID if DEBUG else ALLOWED_SERVER_ID

if GUILD_ID == None: raise Exception("Env variable not provided: DEBUG_SERVER_ID or ALLOWED_SERVER_ID")
if USED_TOKEN == None: raise Exception("Env variable not provided: TOKEN_DEBUG or TOKEN_STABLE")

DISCORD_CHARACTER_LIMIT: int = int(getenv('DISCORD_CHARACTER_LIMIT', 2000))
TWITCH_CHARACTER_LIMIT: int = int(getenv('TWITCH_CHARACTER_LIMIT', 500))

async def send_error_msg(interaction: discord.Interaction, error_id: int) -> None:
    match(error_id):
        case -1: await interaction.response.send_message(f"RayCode symbol can't be nothing, RayCode wasn't updated", ephemeral=True)
        case -2: await interaction.response.send_message(f"RayCode symbol can't contain spaces, RayCode wasn't updated", ephemeral=True)
        case -3: await interaction.response.send_message(f"Same RayCode symbol can't have different meaning on twitch and discord, RayCode wasn't updated", ephemeral=True)

        case _: await interaction.response.send_message(f"Unknown error detected, please screenshot the message that caused this and contant the bot creater: Krakenuspa", ephemeral=True) 

class Client(commands.Bot):
    async def on_ready(self):
        if DEBUG: print('Bot Initialized (DEBUG)')
        else: print('Bot Initialized (STABLE)')

        try:
            if GUILD_ID == None: raise Exception("Env variable not provided: DEBUG_SERVER_ID or ALLOWED_SERVER_ID")
            guild = discord.Object(id=GUILD_ID)
            synced = await self.tree.sync(guild=guild)
            print(f"synced {len(synced)} commands to guild {guild.id}")

        except Exception as e:
            print(f"Error syncing cmds: {e}")

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix = '!', intents = intents)
active_raycode = raycode(GUILD_ID)

### COMMANDS ↓ ###

@client.tree.command(name="encode_discord", description=f"Encodes text into RayCode", guild=discord.Object(GUILD_ID))
async def encode_discord(interaction: discord.Interaction, message: str):
    encoded_msg = active_raycode.encode_discord(message)
    
    if len(encoded_msg) > DISCORD_CHARACTER_LIMIT:
        await interaction.response.send_message("Encoded message is longer than allowed length of discord msg (2K characters)", ephemeral=True)
    else:
        await interaction.response.send_message(encoded_msg, ephemeral=True)

@client.tree.command(name="encode_twitch", description=f"Encodes text into RayCode", guild=discord.Object(GUILD_ID))
async def encode_twitch(interaction: discord.Interaction, message: str):
    encoded_msg = active_raycode.encode_twitch(message)

    if len(encoded_msg) > TWITCH_CHARACTER_LIMIT:
        await interaction.response.send_message("Encoded message is longer than allowed length of twitch msg (500 characters)", ephemeral=True)
    else:
        await interaction.response.send_message(encoded_msg, ephemeral=True)

@client.tree.command(name="decode", description="Decodes RayCode into text", guild=discord.Object(GUILD_ID))
async def decode(interaction: discord.Interaction, message: str):
    decoded_msg = active_raycode.decode(message)

    if len(decoded_msg) > DISCORD_CHARACTER_LIMIT:
        await interaction.response.send_message("Decoded message is longer than allowed length of discord msg (2K characters)", ephemeral=True)
    else:
        await interaction.response.send_message(decoded_msg, ephemeral=True)

@client.tree.command(name="change_dot_text", description="Update text for dot in RayCode", guild=discord.Object(GUILD_ID))
async def change_dot_text(interaction: discord.Interaction, new_text: str, discord: bool = False, twitch: bool = False):
    if not discord and not twitch:
        await interaction.response.send_message(f"Please select at least one platform as True", ephemeral=True)
        return
    error = active_raycode.update_symbol(".", new_text, twitch = twitch, discord = discord)
    
    if error == 0:
        await interaction.response.send_message(f"Dot in RayCode, from now on, will be: {new_text}", ephemeral=True)
    else:
        await send_error_msg(interaction, error)

@client.tree.command(name="change_dash_text", description="Update text for dash in RayCode", guild=discord.Object(GUILD_ID))
async def change_dash_text(interaction: discord.Interaction, new_text: str, discord: bool = False, twitch: bool = False):
    if not discord and not twitch:
        await interaction.response.send_message(f"Please select at least one platform as True", ephemeral=True)
        return
    error = active_raycode.update_symbol("-", new_text, twitch = twitch, discord = discord)
    
    if error == 0:
        await interaction.response.send_message(f"Dash in RayCode, from now on, will be: {new_text}", ephemeral=True)
    else:
        await send_error_msg(interaction, error)

@client.tree.command(name="change_letter_separator", description="Update text for letter seperator in RayCode", guild=discord.Object(GUILD_ID))
async def change_letter_seperator(interaction: discord.Interaction, new_text: str, discord: bool = False, twitch: bool = False):
    if not discord and not twitch:
        await interaction.response.send_message(f"Please select at least one platform as True", ephemeral=True)
        return
    error = active_raycode.update_symbol(" ", new_text, twitch = twitch, discord = discord)
    
    if error == 0:
        await interaction.response.send_message(f"Letter separator in RayCode, from now on, will be: {new_text}", ephemeral=True)
    else:
        await send_error_msg(interaction, error)

@client.tree.command(name="change_word_separator", description="Update text for word seperator in RayCode", guild=discord.Object(GUILD_ID))
async def change_word_seperator(interaction: discord.Interaction, new_text: str, discord: bool = False, twitch: bool = False):
    if not discord and not twitch:
        await interaction.response.send_message(f"Please select at least one platform as True", ephemeral=True)
        return
    error = active_raycode.update_symbol("/", new_text, twitch = twitch, discord = discord)
    
    if error == 0:
        await interaction.response.send_message(f"Word separator in RayCode, from now on, will be: {new_text}", ephemeral=True)
    else:
        await send_error_msg(interaction, error)

### Error Handling ↓ ###
@client.event
async def on_command_error(_, error: commands.CommandError):
    if isinstance(error, commands.errors.CommandNotFound): # Avoids throwing an error into output when someone posts "!" at the beginning of their message
        return
    raise error

if __name__ == "__main__":
    client.run(USED_TOKEN)