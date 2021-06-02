#Discord Bot
# id - 575109063419887618
# token - NTc1MTA5MDYzNDE5ODg3NjE4.XNDKbA.6fQXVeKHDn_kSATflG3FATLMyyw
# permissions int - 67648
# https://discordapp.com/oauth2/authorize?client_id=575109063419887618&scope=bot&permissions=67648
# server id - 420371828335312896
# brandon - 238807706419331072
#Alex - 249429936098639873

import discord
from discord.ext import commands
import urllib.parse, urllib.request, re
import os
import time
import asyncio
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use("fivethirtyeight")
client = commands.Bot(command_prefix = '.')







def community_report(rguild):
        online = 0
        offline = 0
        idle = 0
        
        
        for x in rguild.members:
            if str(x.status) == "online":
                online += 1;          
            elif str(x.status) == "offline":
                offline += 1
            else:
                idle += 1

        return online, idle, offline


async def user_metrics():
        await client.wait_until_ready()
        global guild
        
        while not client.is_closed():
            try:
                online, idle, offline = community_report(guild)
                with open("usermetrics.csv", "a") as f:
                    f.write(f"{int(time.time())},{online},{idle},{offline}\n")
                    
                    
                    df = pd.read_csv("usermetrics.csv", names = ['time', 'online','idle','offline'])
                    df['date'] = pd.to_datetime(df['time'], unit = 's')
                    df['total'] = df['online'] + df['offline'] + df['idle']
                    df.drop("time", 1, inplace=True)
                    df.set_index("date", inplace = True)
                    
                    print(df.head())
                    plt.clf()
                    df['online'].plot()
                    df['offline'].plot()
                    df['idle'].plot()
                    plt.legend()
                    plt.savefig("online.png")
                    plt.savefig("offline.png")
                    plt.savefig("idle.png")
                    
                await asyncio.sleep(300)
            
            except Exception as e:
                print(str(e))
                await asyncio.sleep(300)
 
        
@client.event  # event decorator/wrapper

async def on_ready():
    global guild
    guild = client.get_guild(420371828335312896)
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game('At Your Service'))
    print(f"we have logged in as {client.user}")
    





    
    
    
@client.event

async def on_message(message):
    global guild
    
    print(f"{message.channel} : {message.author} : {message.author.name} : {message.content} ")
    
    
    
    if "count()" == message.content.lower():
        await message.channel.send(f"There are {guild.member_count} members in this server!!!")
    
    elif "hi there" in message.content.lower():
        await message.channel.send("HI!")

    elif "!echo" in message.content.lower():
        msg = message.content.split()
        output = ''
        for word in msg[1:]:
            output += word
            output += ' '
        await message.channel.send(output)
        
        
        
        
    elif "!report" == message.content.lower():
        online, idle, offline = community_report(guild)
    

        await message.channel.send(f"Online : {online}. Idle/AFK/Do Not Disturb: {idle}. Offline: {offline}")
        filen = discord.File("online.png", filename="online.png")
        await message.channel.send("online.png", file = filen)
    

    await client.process_commands(message)
    




@client.command()
async def clear(ctx, amount = 2):
    if (amount <= 200):
        await ctx.channel.purge(limit = amount)
    


@client.command()
async def kick(ctx, member : discord.Member = None, *, reason = None):
    await member.kick(reason = reason)
    await ctx.send(f'Banned{member.mention}')
                     
                     
@client.command()
async def ban(ctx, member: discord.Member, * , reason = None):
    await member.ban(reason = reason)
    
                    
@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    
    
    for ban_entry in banned_users:
        user = ban_entry.user
        
        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return





        
        
@client.command()
async def youtube(ctx,*, search):
    
    query_string = urllib.parse.urlencode({
            'search_query' : search
            })
    htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
    await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])
    
    

    
        
        
        

    
    
    

        









    

client.loop.create_task(user_metrics())

client.run("NTc1MTA5MDYzNDE5ODg3NjE4.XNDKbA.6fQXVeKHDn_kSATflG3FATLMyyw")