import discord
from discord.ext import commands
from secrets import TOKEN
import os
import time
import asyncio
import math
import asyncio
from discord import Color
import json
import  _datetime

# bot config
intents = discord.Intents.all()
upTime = time.time()
client =  commands.Bot(command_prefix='.', intents=intents)
client.remove_command('help')

#global vars
server_name = "Support Bot server"
devMode = False               
helpContinue = "☑️"
helpStop = "❎"
supportCreate = "✋"
supportCategory = "TICKETS"
serverId = 816329111852810302
numOfTickets = 0


missing_req_arg = "You are missing a required arugment, look at the usage above and try again"

# events
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("hi! im a bot"))
    print("Bot is online.")
    if devMode == False:
        return
    elif devMode == True:
        return
    


@client.event
async def on_raw_reaction_add(payload):
    bot = 807251404137431121
    emoji = payload.emoji
    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    if payload.user_id == bot:
        return
    
    if emoji.name == supportCreate and payload.message_id == 816330962337267736:
       global numOfTickets
       guildid = client.get_guild(serverId)
       category = discord.utils.get(guildid.categories, name=supportCategory)
       numOfTickets += 1
       print(numOfTickets)
       await reaction.remove(payload.member)
       channel = await guildid.create_text_channel(f'ticket-{numOfTickets}', overwrites=None, category=category, reason=None)
       embed = discord.Embed(title="New ticket!", color=Color.green())
       embed.add_field(name="Ticket author: ", value=f"{payload.member.mention}",inline=False)
       embed.add_field(name=f"Created at: ",value=f"This ticket was created on {_datetime.date.today()}",inline=False)
    #    embed.add_field(name="Instructions: ",value="Please provide a brief explanation on why you have created this ticket." inline=False)
       await channel.send(embed=embed)
       tempmsg = await channel.send(f'{payload.member.mention}')
       await tempmsg.delete()
           
    
    
    if emoji.name == helpContinue:
        print("Continued Help")

    


#commands
@client.command()
@commands.has_permissions(administrator=True)
async def test(ctx):
    await ctx.send(f'{ctx.author} has issued the test command, checking if elgible for bot status....')
    user = ctx.author
    allowed_user = client.get_user(463016897110343690)
    if user == allowed_user:
        message = await ctx.send(f'{user} has ran the test command with the corect permissions. Direct messaging them bot information...')
        await user.send(f'Bot information: \n**Server name:** {server_name}\n**Bot uptime:** {round(time.time() - upTime)} seconds\n**Dev Mode:** {devMode}')
        await message.add_reaction('☑️')
    else:
        message2 = await ctx.send(f'{user}, you do not have permission to run the test command. If you think this is a mistake, please contact {allowed_user}')
        await message2.add_reaction('❎')


@client.command()
async def setup_support(ctx):
    msg = await ctx.send("Hello, this is the ticket category! If you have any questions or concerns, please reach out to us! React with the reaction below to create a ticket")
    await msg.add_reaction(supportCreate)




    
@client.command(aliases=['ticket-close', 't-close'])
async def ticketclose(ctx: commands.Context):
    if ctx.channel.category and ctx.channel.category.name == "TICKETS":
        embed = discord.Embed(title="Scheduled closure:", color=0xf40000)
        embed.add_field(name="Scheduled closer:", value=f'{ctx.author} has scheduled to close this ticket!', inline=False)
        embed.add_field(name="Time remaining:", value="This ticket will close in 60 seconds.", inline=False)
        await ctx.send(embed=embed)
        await asyncio.sleep(60)
        await ctx.channel.delete()

    

@client.command(aliases=['ticket-rename', 't-rename'])
async def ticketrename(ctx: commands.Context, name_input): 
    if ctx.channel.category and ctx.channel.category.name == "TICKETS":
        name = f"{name_input}-{numOfTickets}"
        await ctx.channel.edit(name=name )
        await ctx.send(f'Ticket name changed to **{name_input}**!')


@client.command(aliases=['ticket-claim', 't-claim'])
async def ticketclaim(ctx):
    if ctx.channel.category and ctx.channel.category.name == "TICKETS":
        embed = discord.Embed(title="Ticket Claimed:", color=Color.green())
        embed.add_field(name="Claimed by:", value=f"{ctx.author}",inline=False)
        embed.add_field(name="PTS Enabled:", value="Support team, remember you must use PTS in order to speak in a claimed ticket, unless you are a senior moderator+.", inline=False)
    
        claimed_message = await ctx.send(embed=embed)
        
   





# ----------------------- DO NOT EDIT THIS BOTTOM PART, NEEDS CORRECT DIR FOR PI ----------------- #


#for filename in os.listdir('/home/pi/Desktop/diamondsbot/cogs'):
#    if filename.endswith('.py'):
#        client.load_extension(f'cogs.{filename[:-3]}')
client.run(TOKEN)
