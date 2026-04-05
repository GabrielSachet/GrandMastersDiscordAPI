import os
import discord
import requests
import time
import asyncio

# Configurações
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
CHANNEL_ID = int(os.environ.get('CHANNEL_ID'))
CLUB_ID = os.environ.get('CLUB_ID')

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} está online!')
    channel = client.get_channel(CHANNEL_ID)
    await channel.send("Bot iniciado! Monitorando mensagens do clube.")

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.id != CHANNEL_ID:
        return
    await message.channel.send(f"Nova mensagem: {message.content}")

async def monitor_brawl_stars():
    while True:
        try:
            API_URL = f"https://api.brawlstars.com/v1/clubs/{CLUB_ID}/members"
            headers = {'Authorization': 'Bearer SEU_API_KEY'}
            response = requests.get(API_URL, headers=headers)
            data = response.json()
            
            for member in data['items']:
                if 'message' in member:
                    channel = client.get_channel(CHANNEL_ID)
                    await channel.send(member['message'])
        except Exception as e:
            print(f"Erro: {e}")
        await asyncio.sleep(60)

if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
