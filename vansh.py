from typing import Any
import discord
from discord import embeds
from discord import client
from discord import message 
from discord.ext import commands
from discord.ext.commands.core import command 
from discord.ext.commands.errors import BotMissingPermissions, CheckFailure, MissingRequiredArgument
from discord.errors import ClientException, DiscordException
import random 
from random import randint
import asyncio

intents=discord.Intents.default()
intents.members=True
client=discord.Client(intents=intents)
SeriousX = commands.Bot(command_prefix=".",case_insensitive=True, intents=intents)

@SeriousX.event
async def on_ready():
  await SeriousX.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=f'.help'))
  print("Bot is ready")

@SeriousX.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send("Invalid command used ! (Check .help for more)")

SeriousX.remove_command("help")

@SeriousX.command(aliases=["info bot"])
async def info(ctx):
 e=discord.Embed(title=":arrow_right: Info", description=f'I am a bot created in python(discord.py). I am a spy bot help you in admin, and entertains ')
 e.add_field(name="**Bot prefix:**", value=".", inline=True)
 e.add_field(name="**Server count:**", value=len(SeriousX.guilds), inline=True)
 await ctx.send(embed=e)

@SeriousX.command()
@commands.has_permissions(manage_guild=True, administrator=True)
async def server(ctx):
   emb=discord.Embed(title="Server stats", color=discord.Color.purple() , description=f'**Server name:** {ctx.guild.name} \n **Server region:** {ctx.guild.region}\n **Server owner:**  {ctx.guild.owner}\n **Server created at:** {ctx.guild.created_at.strftime("%d.%m.%Y")}\n **Server Owner ** {ctx.guild.owner}\n **Server roles:** {len(ctx.guild.roles)}')
   emb.set_thumbnail(url=f'{ctx.guild.icon_url}')
   await ctx.send(embed=emb)

@server.error
async def lol(ctx,error):
  if isinstance(error,commands.MissingPermissions):
    embed=discord.Embed(title="You dont have permissions to use this command", color=discord.Color.red())
    await ctx.send(embed=embed)

@SeriousX.command(aliases=["8ball"])
async def _8ball(ctx, message:str):
  responses=["It is not certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."]
  await ctx.send(f':8ball:{random.choice(responses)}')

@_8ball.error
async def _8ball_error(message, error):
    if isinstance(error, commands.MissingRequiredArgument):
      em=discord.Embed(title=f' Missing question! :point_right: Correct command: .8ball(question) ', color=discord.Color.red())
      await message.send(embed=em)

@SeriousX.command()
@commands.has_permissions(manage_guild=True, administrator=True)
async def send(ctx, member:discord.Member, message ):
  e=discord.Embed(title=f'Message by {ctx.author}', description=f'{member.mention} Here is a message from {ctx.author}({ctx.guild.name})\n\n\n Message: {message}')
  await member.send(embed=e)
  await ctx.send(f'Dm sent')

@send.error
async def send_error(ctx, error):
  emoji=SeriousX.get_emoji(803969799277248542)
  if isinstance(error, commands.MissingPermissions):
    e=discord.Embed(title=f'<a:yes:803969799277248542> You dont have permission to use this')
  await ctx.send(embed=e)

@SeriousX.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount:int):

  if amount>100:
      await ctx.send('You can delete messages more than 100')
  elif amount==0:
     await ctx.send('Lol there is nothing to delete')
  else:
     embe=discord.Embed(title=f'{amount} messages have been deleted')
     await ctx.send(embed=embe)

@clear.error
async def clear_error(ctx,error):
  if isinstance(error,commands.MissingRequiredArgument):
    await ctx.send(f'Please specify the number of messages you want to delete')

@SeriousX.command(name='warn')
@commands.has_permissions(kick_members=True, ban_members=True, manage_guild=True, administrator=True)
@commands.bot_has_permissions(kick_members=True, ban_members=True)
async def warn(ctx, member : discord.Member,* ,reason=None):
 embed=discord.Embed(title=f'Warned member: {member.mention} \n Warned reason: {reason}\n Warned by: {ctx.author}')
 await ctx.send(embed=embed)
 await member.send(f'You have been warned in : {ctx.guild.name} by {ctx.author}')

@warn.error
async def warn_error(ctx,error):
  if isinstance (error, commands.MissingPermissions):
    e=discord.Embed(title=f'You dont have permission to use this command')
    await ctx.send(embed=e)


@SeriousX.command(name='kick', pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member=None,* , reason=None):
  if member == None:
    em=discord.Embed(title='Member object is required')
    await ctx.send(embed=em)
  else:
    if member == ctx.author:
      em=discord.Embed(title='You are mad or wht.....you cant kick yourself noob')
      await ctx.send(embed=em)
    elif member.top_role>=ctx.author.top_role:
      await ctx.send("You cant kick a user which is equal to you or higher to your rank")
    else:
          await member.send(f'You have been kicked from ({ctx.guild.name}) for this reason: {reason}')
          await member.kick(reason=reason)
          embed=discord.Embed(title="Kick", description=f'**Offender:** {member.mention}, {member.id}\n **Reason:** {reason}\n **Responsible mod:** {ctx.author}', color=discord.Color.red())
          await ctx.send(embed=embed)
 

@kick.error
async def kick_error(ctx,error):
  if isinstance(error, commands.MissingPermissions):
    em=discord.Embed(title=f'You dont have permission to use this command')
    await ctx.send(embed=em)


@SeriousX.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member=None,* , reason=None):
  if member is None:
    await ctx.send("You need to send a person whom you have to ban")
  elif member is ctx.author:
    await ctx.send('You cant ban yourself')
  else:
     embed=discord.Embed(title="Ban",description=f'**Offender:** {member.mention}, {member.id} \n **Reason:** {reason}\n **Responsible mod:** {ctx.author}\n ' , color=discord.Color.orange())
     await ctx.send(embed=embed)
     await member.send(f'You have been banned from ({ctx.guild.name}) for this reason: {reason}')
     await member.ban(reason=reason)

@ban.error
async def banerror(ctx,error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send(f'You dont have permission to use this command')
    
@SeriousX.command()
async def beg(ctx):
  beg=['I am not gonna give you anything', 
       'You are awarded 70 x ', 
       'Hey beggar I dont have my cheque book ',
       'You are lucky.You got 120 x',
       'Oh you poor little beggar, take 20 x',
       'Bruh you get nothing except a slap',
       'Oh you need money, take 1 x',
       'Sorry someone stole my purse',
       'Lol..You asked money from a robber',
       'eewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww',
       'Bruh take 56 x ',
       'You got jackpot of 200 x']
  await ctx.send(f'{random.choice(beg)}')

@SeriousX.command()
async def remind(ctx, *, for_wht, time=None): 
  itime=time[:-1]
  stime=time[1:]
  days=int(itime)*86400
  hour=int(itime)*3600
  min=int(itime)*60
  if time is None:
    await ctx.send('Time cant be none')
  elif time is not None:
    if stime=='s':
      el=discord.Embed(title=f'Reminder' , description=f'Reminder set for {ctx.author} about: {for_wht} in {time}')
      await ctx.send(embed=el)
      await asyncio.sleep(itime)
      embe=discord.Embed(title="Reminder", description=f'You are reminded for {for_wht} which you set {time} ago')
      await ctx.author.send(embed=embe)
    elif stime=='h':
        e=discord.Embed(title=f'Reminder' , description=f'Reminder set for {ctx.author} about: {for_wht} in {time}')
        await ctx.send(embed=e)
        await asyncio.sleep(hour)
        embed=discord.Embed(title="Reminder", description=f'You are reminded for {for_wht} which you set {time} ago')
        await ctx.author.send(embed=embed)
    elif stime=='d':
       hello=discord.Embed(title=f'Reminder' , description=f'Reminder set for {ctx.author} about: {for_wht} in {time}')
       await ctx.send(embed=hello)
       await asyncio.sleep(days)
       emba=discord.Embed(title="Reminder", description=f'You are reminded for {for_wht} which you set {time} ago')
       await ctx.author.send(embed=emba)
    else:
      await ctx.send('Syntax error! Correct syntax : .remind(reminder for wht?)(reminder time eg-; 5h, 4d, 6m, 2s)')

@SeriousX.command()
async def slowmode(ctx,time=None, channel:discord.TextChannel=None ):
  itime=time[:-1]
  stime=time[-1]
  print(stime)
  print(itime)
  hour=int(itime)*3600
  min=int(itime)*60
  print(hour)
  print(min)
  
  if time is None:
    await ctx.send("Duration cant be none...Correct syntax= .slowmode (channel name(if required))(duration)")
  
  elif time is not None:
    if channel is None:
       if stime=='h':
           await ctx.channel.edit(slowmode_delay=hour)
           await ctx.send(f'Slowmode has been set for this channel for duration of {time}')
       elif stime=='m':
            await ctx.channel.edit(slowmode_delay=min)
            await ctx.send(f'Slowmode has been set for this channel for duration of {time}')
       elif stime=='s':
           await ctx.channel.edit(slowmode_delay=itime)
           await ctx.send(f'Slowmode has been set for channel {channel} for duration of {time}')
       else:
           embe=discord.Embed(title="Correct syntax is (duration like 5,4,3 ect.)(value like s,m,h)")
           await ctx.send(embed=embe)
    elif channel is not None:
       if stime=='h':
           await channel.edit(slowmode_delay=hour)
           await ctx.send(f'Slowmode has been set for channel {channel} for duration of {time}')
       elif stime=='m':
           await channel.edit(slowmode_delay=min)
           await ctx.send(f'Slowmode has been set for channel {channel} for duration of {time}')
       elif stime=='s':
           await channel.edit(slowmode_delay=itime)
           await ctx.send(f'Slowmode has been set for channel {channel} for duration of {time}')
       else:
           emb=discord.Embed(title="Correct syntax is .slowmode(duration like 5,4,3 ect.)(value like s,m,h)(channel(if required))")
           await ctx.send(embed=emb)
 
 

@SeriousX.command()
async def complain(ctx , complain, member:discord.Member=None):
  if member is ctx.author:
    await ctx.send("Looks like you are in depression....Noob why you are complaing to yourself ")
  if member is None:
    await ctx.send("")
  else:
     embed=discord.Embed(title=f'Complain by {ctx.author}',color=discord.Color.red(), description=f'Complain by: {ctx.author}\n Complain to: {member.mention}\n Complain: {complain}')
  await ctx.message.delete()
  await ctx.send(embed=embed)






@SeriousX.command(aliases=[" oak planks recipe"])
async def oak(ctx):
  em=discord.Embed(Title="Oak planks")
  em.add_field(name="How to make ?", value="Place 1 oak log in crafting menu or crafting table (.recipe crafting table to see about this) that will result in 4 oak planks")
  em.set_image(url="https://www.digminecraft.com/basic_recipes/images/make_oak_wood_plank.png")
  await ctx.send(embed=em)

@SeriousX.command(Nam=["shield_recipe"])
async def recipe(ctx):
  emb=discord.Embed(Title="Shield")
  emb.add_field(name="How to make ?", value="Place 1 iron ignot  ")
  emb.set_image(url="https://www.digminecraft.com/armor_recipes/images/make_shield.png")
  await ctx.send(embed=emb)



SeriousX.run("")
#commands having error
'''@SeriousX.event
async def on_member_join( member : discord.Member):
  channel=SeriousX.get_channel(804239129700859904)
  em=discord.Embed( description=f'{member.mention} Welcome to the "{member.guild.name}" and dont forget to react with roles ', color=discord.Color.blurple())
  await channel.send(embed=em)
  await member.send(f'{member.mention}welcome to {member.guild.name}....Dont forget to read the rules and react with roles')
'''
'''
def check(msg):
        return msg.author == message.author and msg.channel == message.channel and msg.content.lower() in ["odd", "eve"]
@SeriousX.command()
async def single(self,ctx):
  em=discord.Embed(title=f' What do you want to take:', description=f'{ctx.author.mention} Pick from the list below.. \n Type ```odd``` for odd \n Type ```eve``` for even')
  em.set_footer(text="You have only 30 sec to respond ")
  await ctx.send(embed=em)
  msg = await self.client.wait_for("message", timeout = 30 , check=check)
  em=discord.Embed(title="Which numbed you want to take:", description="You can only take number from 1-10 or else get rekt!")
  em.set_footer(text="You have only 30 seconds to respond")
  await ctx.send(embed=em)
  mes = await self.client.wait_for("message", timeout = 30 , check = lambda message: message.author == ctx.author and message.channel == ctx.channel)
  if int(mes.content)<=0:
    await ctx.send(f'Duffer cant you see wht is given above..You can only enter between 1 and 10')
  elif int(mes.content)>10:
    await ctx.send(f'You are having some brain issues...You can only enter number between 1 and 10')
  try:
    msg and mes
    botchoice=random.randint(1,10)
    sum=int(mes)+botchoice
    if msg.content=="odd" and sum%2!=0 or msg.content=="even" and sum%2==0:
       await ctx.send(f'I choosed {botchoice} and sum is {sum}, Congrats! You won')
    elif msg.content=="eve" and sum%2!=0 or msg.content=="odd" and sum%2==0:
        await ctx.send(f'I choosed {botchoice} and sum is {sum}, Better luck next time')
    else:
         await ctx.send("Not a valid option bruh")
  except asyncio.TimeoutError:
     e=discord.Embed(title='Why you even try to start a game if you dont want to play it ? ')
     await ctx.send(embed=e)
  '''
'''@SeriousX.command()
    async def announce(ctx, string: str, colour:str):
    colours= {"green": 0x00ff00, "red": 0xff0000, "blue": 0x0000ff }
    print("string")
    embed=discord.Embed(title="Announcement", description= string, color=colour[colours])
    await ctx.send(embed=embed)'''
