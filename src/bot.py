from dotenv import dotenv_values
import discord
from discord import Intents
from utils import magic_assist as assistant
from utils.card_sdk import CardSdk

if __name__ == "__main__":
    config = dotenv_values(".mtgbot.env")
    DISCORD_AUTH_TOKEN = config.get("DISCORD_AUTH_TOKEN")
    CHANNEL_ID = config.get("CHANNEL_ID")
    if not DISCORD_AUTH_TOKEN:
        print("No discord auth token found in environment")
        exit()

    intents = Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_message(message):

        # Don't respond to your own message
        if message.author == client.user:
            return
        
        msg_content = message.content
        matches = assistant.card_match(msg_content)
        for cardname in matches:
            msg = await message.channel.send(f"_Searching for {cardname}..._")
            response = CardSdk.search(cardname)
            if response:
                await msg.edit(content=response)
            else:
                await message.channel.send(content=f"Unable to find \"{cardname}\"")


    # Run the bot
    client.run(DISCORD_AUTH_TOKEN)