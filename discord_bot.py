import discord
import os
import subprocess

TOKEN = 'discord_bot_token'
AUTHORIZED_USER_IDS = ['user_id']
TARGET_CHANNEL_ID = 'channel_id'
FILE_PATH = 'white-list.txt'
PIPE_PATH = '/tmp/minecraft_pipe'

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if str(message.author.id) not in AUTHORIZED_USER_IDS:
        return  

    if message.channel.id != int(TARGET_CHANNEL_ID):
        return 

    if message.content.startswith('!add'):
        content = message.content[len('!add '):].strip()
        if content:
            result = append_to_file(content)
            if result:
                await message.channel.send(f'Added player {content} to whitelist')
                send_command_to_pipe("whitelist reload")
            else:
                await message.channel.send(f'Failed to add player {content} to whitelist')
        else:
            await message.channel.send('No nickname provided after !add command.')
    
    if message.content.startswith('!command'):
        if message.author == client.user:
            return

        if str(message.author.id) not in AUTHORIZED_USER_IDS:
            return  

        if message.channel.id != int(TARGET_CHANNEL_ID):
            return 
    
        command = message.content[len('!command '):].strip()
        if command:
            send_command_to_pipe(command)
            await message.channel.send(f'Sent command to server: {command}')
        else:
            await message.channel.send('No command provided after !command command.')

def append_to_file(content):
    try:
        subprocess.run(f'echo "{content}" >> {FILE_PATH}', shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to append to file: {e}")
        return False

def send_command_to_pipe(command):
    try:
        with open(PIPE_PATH, 'w') as pipe:
            pipe.write(command + '\n')
        return True
    except Exception as e:
        print(f"Failed to write to pipe: {e}")
        return False


client.run(TOKEN)

