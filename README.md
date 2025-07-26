# RayCode Discord Bot

## What does it do
<p>This bot is a morse code translator but you replace the default symbols like dots and dashes with your own custom text (i.e. discord/twitch emotes).</p>
<p>WARNING: Although the bot can decode regular morse code, since I had to include spaces between custom texts, it can't encode into regular morse cause of the extra spaces.</p>

## How to use
<p>This git repo doesn't include very important file which is "data.env.secret" which you have to make yourself. this file includes 4 env variables that you will need to make this bot run</p>
<p>NOTE: If you're not interested in having debug test version of the bot. You can make both tokens same and both server ids same and the bot should work fine.</p>
<dl>
  <dt>TOKEN_STABLE</dt><dd>TOKEN_STABLE is token for your discord bot, make sure to never show this to anyone you don't trust since it can be used to make your bot run any code</dd>
  <dt>TOKEN_DEBUG</dt><dd>TOKEN_DEBUG is same as TOKEN_STABLE but this one is used if you enable DEBUG variable inside the main.py file, mostly used to test changes.</dd>
  <dt>ALLOWED_SERVER_ID</dt><dd>ALLOWED_SERVER_ID is discord server id for which your bot will try to run on in NON-DEBUG state</dd>
  <dt>DEBUG_SERVER_ID</dt><dd>DEBUG_SERVER_ID is discord server id for which your bot will try to run on in NON-DEBUG state</dd>
</dl>
<p>In order to get discord app tokens, go to discord developer website. As for discord server ids, enable developer mode in your account settings and then you can copy id of any server you're in.</p>

## Origin
<p>Got a sudden realization that emotes could be used for communication and in excitement wrote this bot. This was a brief passion project was original designed for weathergirlray who you can find at https://www.twitch.tv/weathergirlray</p>
