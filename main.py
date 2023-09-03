import discord 
import certifi
from urllib.request import urlopen
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

current_url = "https://cplusplus.com/reference/"
current_html = ""
html_bytes = ""
current_level = 0
current_code = 0 #0 for home, 1 for cpp

def getMessage(msg):
    start_index, end_index = msg.find(">") + 1, msg[1:].find("<") 
    return msg[start_index: end_index]


async def help(message):
    help = "Hello I am the Language Reference Bot. My goal is to assist you in programming in C++, Java and Python. Currently I can only help you with C++.\nUse any of the following commands to communicate with me!\n"
    help += "\t$cpp - get help with c++ code\n"
    help += "\t$go + title - learn more about that topic\n"
    await message.channel.send(help)
    
  
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
     
@client.event
async def on_message(message):
    global current_level
    global current_url
    
    if message.author == client.user:
        return
    
    if message.content == "$help":
        await help(message)
        return
    
    if message.content == '$home' or message.content == '$Home':
        current_level = 0
        current_url = "https://cplusplus.com/reference/"
    
    page = urlopen(current_url, cafile=certifi.where())
    html_bytes = page.read()
    current_html = html_bytes.decode("utf-8")
    
    if current_level == 0:
        
        output = "Here is a list of topics:\n"
        
        while "dd" in current_html:
            
            if len(output) > 1950:
                await message.channel.send(output)
                output = ""
                
            start_index, end_index = current_html.find("<dd>"), current_html.find("</dd>")
            output += ("\t" + getMessage(current_html[start_index:end_index]) + "\n")
            current_html = current_html[(end_index + 5):]
            
        await message.channel.send(output)
        current_level = 1
        await message.channel.send("Type one of the options to learn more")
        
    elif current_level == 1:
        
        index = current_html.find(message.content)
        if index < 90:
            await message.channel.send("I did not find the option you picked, try again...")
        else:
            finding_url = current_html[index - 90: index]
            starting_index = finding_url.find("href")
            finding_url = "https://cplusplus.com" + finding_url[starting_index + 7:]
            end_index = finding_url.find("\">")
            finding_url = finding_url[:end_index]
            current_url = finding_url
            await message.channel.send(finding_url)
            
            page = urlopen(current_url, cafile=certifi.where())
            html_bytes = page.read()
            current_html = html_bytes.decode("utf-8")
            
            output = "Here is a list of topics:\n"
            
        
            while "dd" in current_html:
            
                if len(output) > 1950:
                    await message.channel.send(output)
                    output = ""
                
                start_index, end_index = current_html.find("<dd>"), current_html.find("</dd>")
                output += ("\t" + getMessage(current_html[start_index:end_index]) + "\n")
                current_html = current_html[(end_index + 5):]
            
            await message.channel.send(output)
            current_level = 1
            await message.channel.send("Type one of the options to learn more")
            
            



client.run(os.getenv('TOKEN'))    