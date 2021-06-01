users = await reaction.users().flatten()
# users is now a list of User...
winner = random.choice(users)
await channel.send('{} has won the raffle.'.format(winner))
''''errors-;/''''
'''@SeriousX.command()
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)
async def bans(ctx,member : discord.Member ):
  em=discord.Embed(tile=f'Bans {member.mention}' ,description=f'Banned how many time ?: {}')
  await ctx.send(embed=em)

@bans.error
async def bans_error(ctx,error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send(f'You dont have required permision to use this command')
  else:
    raise error''''
''''@SeriousX.group()
async def help(ctx):
   emb=discord.Embed(title="Help...Your detective SeriousX is here to help you...pls use '.' as prefix", 
   await ctx.send(embed=emb)

@SeriousX.command()
async def fun(ctx):
    embed=discord.Embed(title="Fun Help", description="You can find fun command here", color=0xFF5733 )
    await ctx.send(embed=embed)

@SeriousX.command()
async def Admin(ctx):
    embed=discord.Embed(title=" Admin Help", description="Moderation and admin command", color=0xFF5733 )
    await ctx.send(embed=embed)'''
    
'''@bot.command(pass_context=True)
@commands.has_permissions(kick_members = True)
async def mute(ctx, member: discord.Member):
  if mute(ctx.guild.roles, name="MUTED"):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.send(f"{member} has been muted!")
  elif role in member.roles:
    await ctx.send(f"Hey, chill {member} is still muted! Give them a break ...")
  else:
    guild=ctx.guild
    perms = discord.Permissions(send_messages=False, read_messages=True)
    role = await guild.create_role(name="MUTED", permissions=perms)
    role.hoist=True
    await member.add_roles(role)
    await ctx.send(f"{member} has been muted! And created new role ```MUTED```")
'''
'''@SeriousX.event
async def on_member_join( member : discord.Member):
  channel=SeriousX.get_channel(804239129700859904)
  em=discord.Embed( description=f'{member.mention} Welcome to the "{member.guild.name}" and dont forget to react with roles ', color=discord.Color.blurple())
  await channel.send(embed=em)
  await member.send(f'{member.mention}welcome to {member.guild.name}....Dont forget to read the rules and react with roles')'''

''' 
