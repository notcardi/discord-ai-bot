# ipmports
from openai import OpenAI
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()
discordtoken = os.getenv("discordtoken")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
Dclient = commands.Bot(command_prefix = "@",intents=discord.Intents.all())
OAclient = OpenAI(
    api_key=OPENAI_API_KEY,
)
messages = [{"role":"system","content": "You are Nyde, a kind and helpful Discord AI chatbot which is a fanmade recreation of ClydeAI, discord's own AI which got shutdown in December 2023."}]

def chat_gpt(prompt):
    response = OAclient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()
# write to file easily, so that i dont have to copy and paste this every time i want to write to a file
def writetofile(file : str,msg : str):
    if os.path.exists(file):
        with open(file,'a') as logfile:
            logfile.write("\n" + msg)
    else:
        with open(file,'w') as logfile:
            logfile.write(file + " Session started.")
            logfile.write("\n" + msg)


# notify in terminal that the bot is ready
@Dclient.event
async def on_ready():
    print("Bot is ready")

# acessing chatgpt and sending it through discord
@Dclient.event
async def on_message(message):
    if message.author.bot:
        return
    if isinstance(message.channel, discord.channel.DMChannel):
            messages.append({"role":"user","content": message.content})
            messageresp = chat_gpt(message.content)
            await message.reply(messageresp,mention_author=False)
            messages.append({"role":"assistant","content": messageresp})
            writetofile("logs/" + message.author.name + ".log", messageresp)
    else:
        if Dclient.user.mentioned_in(message):
            messages.append({"role":"user","content": message.content})
            messageresp = chat_gpt(message.content)
            await message.reply(messageresp, mention_author=False)
            messages.append({"role":"assistant","content": messageresp})
            writetofile("logs/" + message.author.name + ".log", messageresp)
            
Dclient.run(discordtoken)