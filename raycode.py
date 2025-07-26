from dotenv import load_dotenv
from os import getenv
from pathlib import Path
import shutil
import json

ENV_FILE_SECRET: str = "./data.env.secret"
ENV_FILE_SHARED: str = "./data.env.shared"
load_dotenv(ENV_FILE_SECRET)
load_dotenv(ENV_FILE_SHARED)

SYMBOLS_PATH:      str | None = getenv('SYMBOLS_PATH', default="./symbols")
DEFAULT_DICT_FILE: str | None = getenv('DEFAULT_FILE', default="./default.json")
TWITCH_FILE_NAME:  str | None = getenv('TWITCH_FILE_NAME', default="twitch.json")
DISCORD_FILE_NAME: str | None = getenv('DISCORD_FILE_NAME', default="discord.json")

BASE_MORSE_ENCODE: dict[str, str] = {
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
BASE_MORSE_DECODE: dict[str, str] = {v: k for k, v in BASE_MORSE_ENCODE.items()}

def __remove_multiple_white_spaces__(txt: str) -> str:
    while "  " in txt: txt = txt.replace("  ", " ")
    return txt

class raycode:
    guild_id: int

    __discord_encode_dict__: dict[str, str]
    __twitch_encode_dict__: dict[str, str]
    __decode_dict__: dict[str, str]

    __server_dir__: Path
    __discord_file__: Path
    __twitch_file__: Path

    def __init__(self, guild_id: int) -> None:
        self.guild_id = guild_id

        self.__server_dir__   = Path(f"./{SYMBOLS_PATH}/{self.guild_id}")
        self.__discord_file__ = Path(f"{self.__server_dir__}/{DISCORD_FILE_NAME}")
        self.__twitch_file__  = Path(f"{self.__server_dir__}/{TWITCH_FILE_NAME}")
        
        self.__load_dicts__()

    ### PUBLIC METHODS ↓ ###

    def encode_discord(self, message: str) -> str:
        """
            Returns encoded version of given message (Uses discord encode dictionary)\n
        """
        return self.__general_encode__(message, self.__discord_encode_dict__)

    def encode_twitch(self, message: str) -> str:
        """
            Returns encoded version of given message (Uses twitch encode dictionary)\n
        """
        return self.__general_encode__(message, self.__twitch_encode_dict__)

    def decode(self, message: str) -> str:
        """
            Returns decoded version of given message from:\n
            Regular Morse Code\n
            Discord Raycode\n
            Twitch Raycode\n
        """
        message = __remove_multiple_white_spaces__(message)
        result_string: str = ""
        current_letter_morse: str = ""
        symbol_list: list[str] = message.split(" ")
        regular_morse = True # Default assumption

        for symbol in symbol_list:
            if regular_morse and (symbol in BASE_MORSE_DECODE):
                result_string += BASE_MORSE_DECODE[symbol]
                continue
            else:
                regular_morse = False

            if symbol == "": continue   

            if (symbol == self.__twitch_encode_dict__[" "]) or (symbol == self.__twitch_encode_dict__["/"]) or (symbol == self.__discord_encode_dict__[" "]) or (symbol == self.__discord_encode_dict__["/"]):
                result_string += BASE_MORSE_DECODE[current_letter_morse]
                current_letter_morse = ""

                if (symbol == self.__twitch_encode_dict__["/"]) or (symbol == self.__discord_encode_dict__["/"]):
                    result_string += " "
                continue
            
            if symbol not in self.__decode_dict__:
                return f"Can't decode message because it contains un-assigned symbol: {symbol}"

            current_letter_morse += self.__decode_dict__[symbol]

        if (current_letter_morse != ""): result_string += BASE_MORSE_DECODE[current_letter_morse]

        return result_string

    def update_symbol(self, morse_symbol: str, new_symbol: str, discord: bool = False, twitch: bool = False) -> int:
        """
            Updates a symbol for provided guild id of the instance of raycode:\n
            Set ``discord`` and/or ``twitch`` to True if you wish to overwrite that specific dictionary\n

            Returns error_code as integer
        """

        if new_symbol == "": return -1
        if " " in new_symbol: return -2
        if new_symbol in self.__decode_dict__ and self.__decode_dict__[new_symbol] != morse_symbol: return -3
        
        if discord:
            del self.__decode_dict__[self.__discord_encode_dict__[morse_symbol]]
            
            self.__discord_encode_dict__[morse_symbol] = new_symbol
            self.__decode_dict__[new_symbol] = morse_symbol

            with open(self.__discord_file__, "w") as f:
                f.write(json.dumps(self.__discord_encode_dict__, indent=4))
            f.close()
            
        
        if twitch:
            del self.__decode_dict__[self.__twitch_encode_dict__[morse_symbol]]
            
            self.__twitch_encode_dict__[morse_symbol] = new_symbol 
            self.__decode_dict__[new_symbol] = morse_symbol

            with open(self.__discord_file__, "w") as f:
                f.write(json.dumps(self.__twitch_encode_dict__, indent=4))
            f.close()

        return 0
     
    ### PRIVATE METHODS ↓ ###

    def __load_dicts__(self) -> None:
        self.__server_dir__.mkdir(exist_ok=True)

        self.__set_default_symbol__(discord = not self.__discord_file__.exists(), twitch = not self.__twitch_file__.exists())

        with open(self.__twitch_file__, "r") as f:
            self.__twitch_encode_dict__ = json.load(f)
        f.close()

        with open(self.__discord_file__, "r") as f:
            self.__discord_encode_dict__ = json.load(f)
        f.close()

        self.__decode_dict__ = {v: k for k, v in self.__discord_encode_dict__.items()} | {v: k for k, v in self.__twitch_encode_dict__.items()}

    def __set_default_symbol__(self, discord: bool = False, twitch: bool = False) -> None:
        if DEFAULT_DICT_FILE == None: raise Exception("Default file is undefined in data.env.shared")

        if discord: shutil.copy(DEFAULT_DICT_FILE, self.__discord_file__)
        if twitch : shutil.copy(DEFAULT_DICT_FILE, self.__twitch_file__)

    def __general_encode__(self, message: str, used_dict: dict[str,str]) -> str:
        message = __remove_multiple_white_spaces__(message).lower()
        result_string: str = ""
        i: int = 0
    
        while i < len(message):
            if message[i] not in BASE_MORSE_ENCODE: return f"Can't encode message because it contains un-assigned character: {message[i]}"
            
            for regular_morse in BASE_MORSE_ENCODE[message[i]]:
                result_string += " " + used_dict[regular_morse]

            if (message[i] != " ") and ((i+1) != len(message)) and (message[i+1] != " "): # Avoids duplicate or unwanted letter seperators
                result_string += " " + used_dict[" "]

            i += 1
    
        result_string = result_string.strip()
    
        if result_string[:2] == "- ": result_string = "\\" + result_string #Special condition to avoid bullet-ins on discord
    
        return result_string

if __name__ == "__main__":
    pass
