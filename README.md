# RayCode Discord Bot

## What does it do
<p>This bot is a morse code translator but you replace the default symbols like dots and dashes with your own custom text (i.e. discord/twitch emotes).</p>
<p>WARNING: Although the bot can decode regular morse code, since I had to include spaces between custom texts, it can't encode into regular morse cause of the extra spaces.</p>

## How to setup
<p>This git repo doesn't include very important file which is "data.env.secret" which you have to make yourself. this file includes 4 env variables that you will need to make this bot run</p>
<p>NOTE: If you're not interested in having debug test version of the bot. You can make both tokens same and both server ids same and the bot should work fine.</p>
<dl>
  <dt>TOKEN_STABLE</dt><dd>TOKEN_STABLE is token for your discord bot, make sure to never show this to anyone you don't trust since it can be used to make your bot run any code</dd>
  <dt>TOKEN_DEBUG</dt><dd>TOKEN_DEBUG is same as TOKEN_STABLE but this one is used if you enable DEBUG variable inside the main.py file, mostly used to test changes.</dd>
  <dt>ALLOWED_SERVER_ID</dt><dd>ALLOWED_SERVER_ID is discord server id for which your bot will try to run on in NON-DEBUG state</dd>
  <dt>DEBUG_SERVER_ID</dt><dd>DEBUG_SERVER_ID is discord server id for which your bot will try to run on in NON-DEBUG state</dd>
</dl>
<p>In order to get discord app tokens, go to discord developer website. As for discord server ids, enable developer mode in your account settings and then you can copy id of any server you're in.</p>

# How to use
<p>Once you get the code running succesfully, there will be 7 commands at your disposal, , and </p>
<p>WARNING: Make sure to restrict this bot's change cmds otherwise anyone on your server could mess with those.</p>
### 3 User-Level Commands
<dl>
  <dt>/encode_discord</dt><dd>Encodes given message using custom morse alphabet intended for DISCORD</dd>
  <dt>/encode_twitch</dt><dd>Encodes given message using custom morse alphabet intended for TWITCH</dd>
  <dt>/decode</dt><dd>Decodes a message from ALL: discord morse, twitch morse, and regular morse</dd>
</dl>
### 4 Admin-Level Commands
<p>NOTE: The change commmands have two variables except the new symbol, twitch and discord, only those alphabets set to True will be updated</p>
<p>WARNING: The new symbols can't include a space, cause of the space being the separator between the symbols themselves. The bot will stop you from doing so but still, heads up.</p>
<dl>
  <dt>/change_dot_text</dt><dd>Changes text for DOT in selected alphabets</dd>
  <dt>/change_dash_text</dt><dd>Changes text for DASH in selected alphabets</dd>
  <dt>/change_letter_separator</dt><dd>Changes text for LETTER SEPARATOR in selected alphabets</dd>
  <dt>/change_word_separator</dt><dd>Changes text for WORD SEPARATOR in selected alphabets</dd>
</dl>

## Origin
<p>Got a sudden realization that emotes could be used for communication and in excitement wrote this bot. This was a brief passion project was original designed for weathergirlray who you can find at https://www.twitch.tv/weathergirlray</p>
