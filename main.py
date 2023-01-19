##
##
## READ THE README.MD FILE!
##
##

import discord,os,random,urllib.request,aiohttp,json,datetime,time,pickle,asyncio,textwrap,contextlib,io,datetime,uuid
from discord_components import *
from discord.ext import commands
from server import KeepOnline
from traceback import format_exception
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select
from PIL import Image, ImageDraw, ImageFilter, ImageFont
# from discord_slash import SlashCommand,SlashContext

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = '-',case_insensitive=True,intents=intents)

my_secret = os.environ['TOKEN']
eclr = 0xDC0034
bot.remove_command("help")
owners = [ #ids of owners ]
ticket_black_list = [ #blacklist from using tickets ]
suggestion_black_list = [ #blacklist fron suggesting more  ]

@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx):
    ch = ctx.message.channel
    ch2 = await ch.clone()
    c = discord.utils.get(ctx.guild.categories,id=1027816401660026901)
    await ch.edit(category=c)
    await ch.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.reply('**Regular users can no longer see this channel!**')


@bot.command()
@commands.has_permissions(manage_messages=True)
async def move(ctx,vc2:int,vc1=None):
  try:
    try:
      vc2 = bot.get_channel(int(vc2))
      if vc1 == None:
        vc1 = ctx.author.voice.channel
      else:
        vc1 = bot.get_channel(int(vc1))
      for i in vc1.voice_states.keys():
        mem = discord.utils.get(bot.get_all_members(), id=int(i)) 
        await mem.move_to(vc2)
    finally:
      await ctx.reply(f'**Moved everyone from {vc1.mention} to {vc2.mention}!**')
  except Exception as e:
    await ctx.send(f'```py\n{e}\n```')

@bot.command()
@commands.has_permissions(ban_members=True)
async def forceban(ctx, user: discord.User):
  if ctx.author.id in owners:
    await ctx.guild.ban(user)
    embed = discord.Embed(title=' ', description=f"Successfully banned **{user.name}**", colour=eclr)
    await ctx.reply(embed=embed, mention_author=False)

@bot.command(name='s')
async def s_(ctx,*,message='a'):
  channel = bot.get_channel(1048648074194604142)
  if len(message) >= 12:
    await channel.send(embed=discord.Embed(description=f'<:pivot:1038379059467538462> **SUGGESTION BY {ctx.author.name}**\n>>> {message}',color=eclr))
    await ctx.reply('<:pivot_g:1038385754180685914> **Successfully submitted**')
  else:
    await ctx.reply('<:pivot:1038379059467538462> **Message cannot be shorter than 12 letters**')

@bot.command()
async def announce(ctx,title,text,embed=False):
  try:
    if ctx.author.id in owners:
      if embed is True:
        embed = discord.Embed(title=title,description=text,color=eclr)
        embed.set_author(name=ctx.author.name+' | Announcement',icon_url=ctx.author.avatar_url)
        await bot.get_channel(990185817123213342).send('||<@&925717318615584815>||',embed=embed)
      else:
        await bot.get_channel(990185817123213342).send(f'{title}\n'+text+'\n||<@&925717318615584815>||')
  except Exception as e:
    await ctx.send(e)

@bot.command()
@commands.cooldown(1,60,commands.BucketType.user)
async def background(ctx,reset='bozo'):
  try:
    boosters = discord.utils.get(ctx.guild.roles,id=1008718416057737287).members
    staff = discord.utils.get(ctx.guild.roles,id=1008745408756977684).members
    if ctx.author in boosters or ctx.author in staff:
      with open('special_bg','r') as sb:
        s = sb.read()
      if reset == 'reset':
        if str(ctx.author.id) in s: 
          os.remove(f'image_bases/Base{ctx.author.id}.png')
          with open('special_bg','w') as sb:
            sb.write(s.replace(str(ctx.author.id),''))
          await ctx.reply('**Background reset to default!**',mention_author=False)
        else:
          await ctx.reply('**Background already set to default!**',mention_author=False)
      else:
        if len(ctx.message.attachments) == 0:
          await ctx.reply('**You must attach an image!**',mention_author=False)
          return
        a = await ctx.reply('**<a:pxd:1033779019423948910> Processing...**',mention_author=False)
        with open('special_bg','a') as sb:
          if str(ctx.author.id) not in s:
            sb.write(f'\n{ctx.author.id}')
          else:
            pass
        image = ctx.message.attachments[0]
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', 'pxd')
        filename, headers = opener.retrieve(image, f'image_bases/Base{ctx.author.id}.png')
        await a.delete()
        await ctx.reply('**Background successfully updated!**',mention_author=False)
    else:
      await ctx.reply('**You must be a booster or staff to use this command.**',mention_author=False)
  except Exception as e:
    await ctx.send(e)

def fileSearch(file,str):
  ln = 0
  rl = []
  with open(file, 'r') as f:
    for i in f:
      ln += 1
      if str in i:
        rl.append((ln, i.rstrip()))
  return rl

@bot.command()
@commands.cooldown(1,10,commands.BucketType.user)
async def stats(ctx,member:discord.Member=None):
  try:
    if member is None:
      member = ctx.author
    with open('WL.json','r') as f:
      ww = f.read()
      w = json.loads(ww)
    if f'{member.id}' not in ww:
      await ctx.reply('**Player mentioned does not have any recorded stats!**')
      return
    wins = w[f"{member.id}"]["wins"]
    streak = w[f"{member.id}"]["ws"]
    losses = w[f"{member.id}"]["losses"]
    L = losses
    if int(losses) == 0:
      L = 1
    with open('leaderboard_telstars','w') as f:
        f.write('')
    with open('Telstra.json','r') as f:
      data = json.load(f)
    top = {k: i for k, i in sorted(data.items(), key=lambda item: item[1], reverse=True)}
    for postion, player in enumerate(top):
      with open('leaderboard_telstars','a') as f:
        f.write(player+'\n')
    li = fileSearch('leaderboard_telstars', f'{member.id}')
    for i in li:
      LBpos = i[0] 
    fetching_message = await ctx.reply('**<a:pxd:1033779019423948910> Processing...**',mention_author=False)
    with open('Telstra.json','r') as f:
      d = json.load(f)
      elo = d[f"{member.id}"]
    with open('special_bg','r') as sb:
      special = sb.read()
    if str(member.id) in special:
      try:
        base = Image.open(f'image_bases/Base{member.id}.png')
      except:
        base = Image.open('Base.png')
    else:
      base = Image.open('Base.png')
    base = base.resize((1366,768))
    base = base.filter(ImageFilter.GaussianBlur(7))
    overlay = Image.open(f"overlay.png")
    base.paste(overlay, (0,0), overlay)
    base = base.convert("RGB")
    draw = ImageDraw.Draw(base)

    eloc = (156,156,156)
    pres = 'stone'
    divX = 5
    #pX = 342
    url = r'1025105293530648657/st.png'
    if int(elo) >= 100 < 200:
      url = r'1025105295581646910/ir.png'
      #pX = 355
      pres = 'iron'
      divX = 4
      eloc = (106,106,106)
    if int(elo) >= 200 < 300:
      url = r'1025105295153832057/go.png'
      pres = 'gold'
      eloc = (241,196,14)
      divX = 4
    if int(elo) >= 300 < 400:
      #pX = 332
      url = r'1025105294327566396/dia.png'
      pres = 'diamond'
      eloc = (17,219,255)
      divX = 4
    if int(elo) >= 400 < 500:
      url = r'1025105294700843141/em.png'
      #pX = 328
      pres = 'emerald'
      eloc = (6,172,62)
    if int(elo) >= 500 < 600:
      url = r'1025105296059801704/pl.png'
      #pX = 322
      pres = 'platinum'
      eloc = (142,197,217)
    if int(elo) >= 600 < 700:
      pres = 'ruby'
      url = r'1025105296462446642/ru.png'
      eloc = (176,0,0)
    if int(elo) >= 700 < 900:
      #pX = 322
      pres = 'sapphire'
      url = r'1025105296835743774/sa.png'
      eloc = (58,94,230)
    if int(elo) >= 1000:
      #pX = 330
      pres = 'crystal'
      url = r'1025105293891350639/cry.png'
      eloc = (140,32,190)
                         
    if len(str(elo)) == 1:
      posX = 960
    if len(str(elo)) == 2:
      posX = 950
    if len(str(elo)) == 3:
      posX = 920
    if len(str(elo)) >= 4:
      posX = 905

    if len(member.name) > 20:
      name = member.name[:20]+'...'
    else:
      name = member.name
    
    draw.text((312,100), name, (255,255,255), font=ImageFont.truetype('font.ttf', 58))
    draw.text((312,163), '#'+member.discriminator, (118,118,118), font=ImageFont.truetype('font.ttf', 42))
    draw.text((312,228), f'{pres}', eloc, font=ImageFont.truetype('font.ttf', 28),align='left')
    
    draw.text((47,415), 'WINS  : '+str(wins)+f'  (WS: {streak})', (255,255,255), font=ImageFont.truetype('font.ttf', 58))
    draw.text((47,515), 'LOSS : '+str(losses), (255,255,255), font=ImageFont.truetype('font.ttf', 58))
    draw.text((47,615), 'W/LR : '+str(round(int(wins)/int(L),2)) +' ('+str(round(((int(wins)/(int(wins)+int(losses)))*100),1))+'%)', (255,255,255), font=ImageFont.truetype('font.ttf', 58))
    #draw.rounded_rectangle((314, 246, 464, 286), fill=None, outline=eloc,width=4, radius=7)
    draw.text((posX,520), f'[{elo}]', eloc, font=ImageFont.truetype('font.ttf', 56))
    draw.text((830,490), f'#{LBpos}', (200,200,200), font=ImageFont.truetype('font.ttf', 32))
    
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'pxd')
    filename, headers = opener.retrieve(member.avatar_url, f'pfp{member.id}.png')
    filename, headers = opener.retrieve(r'https://cdn.discordapp.com/attachments/938363928164073503/'+url, f'pres{member.id}.png')
    
    pfp = Image.open(f"pfp{member.id}.png")
    pres = Image.open(f"pres{member.id}.png")
    width, height = pres.size
    pfp = pfp.resize((232,232))
    pres = pres.resize((width//divX,height//divX))
    base.paste(pfp, (65,57))
    os.remove(f"pfp{member.id}.png")
    base.paste(pres, (1249,46), pres)
    os.remove(f"pres{member.id}.png")
    
    base.save(f"stats{member.id}.png")
    with open(f"stats{member.id}.png",'rb') as f:
      p = discord.File(f, filename=f'{member.id}stats.png')
    embed = discord.Embed(color=eclr)
    embed.set_author(name='Telstra | Player Stats',icon_url=ctx.guild.me.avatar_url)
    embed.set_image(url=f'attachment://{member.id}stats.png')
    await ctx.reply(file=p,embed=embed,mention_author=False)
    await fetching_message.delete()
    os.remove(f"stats{member.id}.png")
  except Exception as e:
    await ctx.send(e)

@bot.command()
@commands.cooldown(1,10,commands.BucketType.user)
async def leaderboard(ctx,t='t'):
  try:
    fetch = await ctx.reply('<a:pxd:1033779019423948910> **Processing...**',mention_author=False)
    tType = ['t','telstars','Telstars','telstar','Telstar','T']
    wType = ['wins','w','W','Wins']
    lType = ['loss','losses','Loss','Losses','l','L']
    wlrType = ['wlr','w/lr','W/lr','Wlr','WLR','W/LR']
    wsType = ['ws','WS', 'WinStreak','winstreak','Winstreak','streak','Streak','Ws']
    if t in tType:
      a = 'Telstar'
      with open('Telstra.json','r') as f:
        data = json.load(f)
      top = {k: i for k, i in sorted(data.items(), key=lambda item: item[1], reverse=True)[:10]}
    if t in wType:
      a = 'Wins'
      with open('WL.json','r') as f:
        data = json.load(f)
      top = {k: i for k, i in sorted(data.items(), key=lambda item: item[1]['wins'], reverse=True)[:10]}
    if t in lType:
      a = 'Losses'
      with open('WL.json','r') as f:
        data = json.load(f)
      top = {k: i for k, i in sorted(data.items(), key=lambda item: item[1]['losses'], reverse=True)[:10]}
    if t in wsType:
      a = 'WinStreak'
      with open('WL.json','r') as f:
        data = json.load(f)
      top = {k: i for k, i in sorted(data.items(), key=lambda item: item[1]['ws'], reverse=True)[:10]}
    if t in wlrType:
      a = 'W/LR'
      with open('WL.json','r') as f:
        data = json.load(f)
      top = {k: i for k, i in sorted(data.items(), key=lambda item: item[1]['wlr'], reverse=True)[:10]}
    base = Image.open('base_leaderboard.png')
    draw = ImageDraw.Draw(base)
    lb = ''
    for postion, player in enumerate(top):
      amt = 0
      if t in tType:
        amt = data[player]
      if t in wType:
        amt = data[player]['wins']
      if t in lType:
        amt = data[player]['losses']
      if t in wsType:
        amt = data[player]['ws']
      if t in wlrType:
        amt = round(data[player]['wlr'],2)
      try:
        player = bot.get_user(int(player))
        lb += f'| {postion+1} |  {player.name}  -  [ {amt} ]\n\n'
      except:
        player = str(player)
        lb += f'| {postion+1} |  {player}  -  [ {amt} ]\n\n'
    draw.text((60,45),lb,(255,255,255),font=ImageFont.truetype('font.ttf', 28))
    base.resize((1080,1080))
    base.save(f"leaderboard.png")
    with open(f"leaderboard.png",'rb') as f:
      p = discord.File(f, filename=f'leaderboard.png')
    embed = discord.Embed(color=eclr)
    embed.set_author(name=f'Telstra | {a} Leaderboard',icon_url=ctx.guild.me.avatar_url)
    embed.set_image(url=f'attachment://leaderboard.png')
    await fetch.delete()
    await ctx.reply(file=p,embed=embed,mention_author=False)
  except Exception as e:
    await ctx.send(e)

@bot.command()
async def submit(ctx,id=None,W=None):
  try:
    if W is None:
      await ctx.reply('**Please mention which team won!**\n> `-submit [gameID] [Winning Team]`')
      return
    else:
      W = W.replace('team ','').replace('Team ','').replace('team','').replace('Team','')
    a = ctx.message.attachments
    if len(a) > 1:
      await ctx.reply('**You attached more than 1 image. Only the first image will be sent in!**')
    if id is None:
      await ctx.reply('**Provide a valid game id!**')
      return
    with open('Games.json','r') as f:
      f = f.read()
    if id not in f:
      await ctx.reply('**Provide a valid game id!**')
      return
    if a == []:
      await ctx.reply('**Please attach an image for proof!**')
    else:
      await ctx.reply('**Successfully submitted screenshot. The game will be reviewed as soon as possible!**')
      embed = discord.Embed(title=f'GAME {id}',color=eclr)
      embed.set_author(name='Telstra | Game Submission',icon_url=ctx.guild.me.avatar_url)
      embed.set_image(url=a[0].url)
      embed.add_field(name='Winner:',value=f'Team {W}\n\n***(refer to {bot.get_channel(1008780010187935804).mention} for teams)***')
      embed.set_footer(text=f'Submitted by {ctx.author} | {ctx.author.id}')
      ch = bot.get_channel(1022201295299411988)
      staff = discord.utils.get(ctx.guild.roles, id=1008745408756977684)
      await ch.send(staff.mention,embed=embed)
  except Exception as e:
    await ctx.send(e)
      
def eloADD(x):
  if x < 100:
      return x+45
  if x in [i for i in range(100,200)]:
      return x+35
  if x in [i for i in range(200,300)]:
      return x+25
  if x in [i for i in range(300,400)]:
      return x+15
  if x in [i for i in range(400,500)]:
      return x+12
  if x in [i for i in range(500,600)]:
      return x+10
  if x in [i for i in range(600,800)]:
      return x+8
  if x in [i for i in range(800,1000)]:
      return x+6
  if x > 1000:
      return x+4

def eloLESS(x):
  if x == 0:
      return x
  if 1 <= x < 90:
      return x-1
  if x in [i for i in range(90,200)]:
      return x-8
  if x in [i for i in range(200,300)]:
      return x-12
  if x in [i for i in range(300,400)]:
      return x-16
  if x in [i for i in range(400,500)]:
      return x-21
  if x in [i for i in range(500,600)]:
      return x-23
  if x in [i for i in range(600,800)]:
      return x-25
  if x in [i for i in range(800,1000)]:
      return x-30
  if x > 1000:
      return x-36

@bot.command()
async def yeah(ctx):
  if ctx.author.id in owners:
    await ctx.guild.me.edit(nick=None)

@bot.command()
@commands.cooldown(1,15,commands.BucketType.user)
async def add(ctx,game,*,team):
  try:

      if game[0] == '#':
        game = game.replace('#','')
        
      with open('Games.json','r') as g:
        games = json.load(g)
      
      t1 = games[f'#{game} \u2193']['Team 1']
      t2 = games[f'#{game} \u2193']['Team 2']
        
      if team in ['team 1','Team 1','1']:
        tn = 'Team 1'
        tt = t1
        ft = t2
      if team in ['team 2', 'Team 2', '2']:
        tn = 'Team 2'
        tt = t2
        ft = t1
      with open('Telstra.json','r') as f:
        ee = f.read()
        e = json.loads(ee)
      with open('WL.json','r') as f:
        ww = f.read()
        w = json.loads(ww)
      with open('Games.json','r') as f:
        f = f.read()
        amt = json.loads(f)
      amt = len(amt[f"#{game} \u2193"]["Team 1"])

      for i in tt:
        m = discord.utils.get(bot.get_all_members(), id=int(i)) 
        ii = str(i)
        if ii in ee:
          x = e[ii]
          if amt >= 3:
            num = eloADD(x)
          else:
            num = x+6
        else:
          if amt >= 3:
            num = eloADD(1)
          else:
            num = 6
          
        if ii in ww:
          with open('WL.json','w') as www:
            w[ii]["wins"] = int(w[ii]["wins"])+1
            lossR = int(w[ii]['losses'])
            if lossR == 0:
              lossR = 1
            w[ii]["wlr"] = (int(w[ii]["wins"]))/lossR
            if w[ii]["recent"] == 'win':
              w[ii]["ws"] = w[ii]["ws"]+1
            else:
              w[ii]["ws"] = 1
            w[ii]["recent"] = 'win'
            json.dump(w,www,indent=4)        
        else:
          with open('WL.json','w') as www:
            w[ii] = {}
            w[ii]["wins"] = 1
            w[ii]["losses"] = 0
            w[ii]["wlr"] = 1
            w[ii]["recent"] = 'win'
            w[ii]["ws"] = 1
            json.dump(w,www,indent=4)
        
        e[ii] = num
        try:
          try:
            await m.edit(nick=f'{num} ✧ {m.nick.split("✧ ",1)[1]}')
          except:
            await m.edit(nick=f'{num} ✧ {m.name}')
        except:
          pass
        if num < 100:
          id = 1026847690375581827
          prev_id = None
        if num >=100 and num <200:
          id = 1023977086819508245
          prev_id = 1026847690375581827
        if num >=200 and num <300:
          id = 1022893255978917960
          prev_id = 1023977086819508245
        if num >=300 and num <400:
          id = 1027103286924410941
          prev_id = 1022893255978917960
        if num >=400 and num <500:
          id = 1027103369548009482
          prev_id = 1027103286924410941
        if num >=500 and num <600:
          id = 1027104681777958972
          prev_id = 1027103369548009482
        if num >=600 and num <800:
          id = 1027104469483257886
          prev_id = 1027104681777958972
        if num >=800 and num <1000:
          id = 1027104570314326038
          prev_id = 1027104469483257886
        if num >= 1000:
          id = 1027104680662282283
          prev_id = 1027104570314326038
        role = discord.utils.get(ctx.guild.roles, id=id)
        try:
          role2 = discord.utils.get(ctx.guild.roles, id=prev_id)
          await m.remove_roles(role2)
        except:
          pass
        await m.add_roles(role)
      for i in ft:
        m = discord.utils.get(bot.get_all_members(), id=int(i)) 
        ii = str(i)
        if ii in ee:
          x = e[ii]
          if amt >= 3:
            num = eloLESS(x)
          else:
            if x >= 6: 
              num = x-6
            else:
              num = 0
          
        if ii in ww:
          with open('WL.json','w') as www:
            w[ii]["losses"] = int(w[ii]["losses"])+1
            lossR = int(w[ii]['losses'])
            if lossR == 0:
              lossR = 1
            w[ii]["wlr"] = int(w[ii]['wins'])/lossR
            w[ii]["ws"] = 0
            w[ii]["recent"] = 'loss'
            json.dump(w,www,indent=4)

        if ii not in ee:
          num = 0
        if ii not in ww:
          with open('WL.json','w') as www:
            w[ii] = {}
            w[ii]["wins"] = 0
            w[ii]["losses"] = 1
            w[ii]["wlr"] = 0
            w[ii]["ws"] = 0
            w[ii]["recent"] = 'loss'
            json.dump(w,www,indent=4)
      
        e[ii] = num
        if num < 100:
          id = 1026847690375581827
          prev_id = 1023977086819508245
        if num >=100 and num <200:
          id = 1023977086819508245
          prev_id = 1022893255978917960
        if num >=200 and num <300:
          id = 1022893255978917960
          prev_id = 1027103286924410941
        if num >=300 and num <400:
          id = 1027103286924410941
          prev_id = 1027103369548009482
        if num >=400 and num <500:
          id = 1027103369548009482
          prev_id = 1027104681777958972
        if num >=500 and num <600:
          id = 1027104681777958972
          prev_id = 1027104469483257886
        if num >=600 and num <800:
          id = 1027104469483257886
          prev_id = 1027104570314326038
        if num >=800 and num <1000:
          id = 1027104570314326038
          prev_id = 1027104680662282283
        if num >= 1000:
          id = 1027104680662282283
          prev_id = None
        role = discord.utils.get(ctx.guild.roles, id=id)
        try:
          role2 = discord.utils.get(ctx.guild.roles, id=prev_id)
          await m.remove_roles(role2)
        except:
          pass
        await m.add_roles(role)
        try:
          try:
            await m.edit(nick=f'{num} ✧ {m.nick.split("✧ ",1)[1]}')
          except:
            await m.edit(nick=f'{num} ✧ {m.name}') 
        except:
          pass

      with open('Telstra.json','w') as ff:
        json.dump(e,ff,indent=4)
      
      embed = discord.Embed(description=f'**Successfuly added Telstars to {tn} (and removed from the other)**',color=eclr)
      embed.set_footer(text=f'in Game #{game}')
      embed.set_author(name='Telstra | Telstars',icon_url=ctx.guild.me.avatar_url)
      
      await ctx.reply(embed=embed,mention_author=False)      

      embed = discord.Embed(description=f'**{ctx.author.mention} added Telstars to {tn} (and removed from the other)**',color=eclr)
      embed.set_footer(text=f'in Game #{game}')
      embed.set_author(name='Telstra | Telstar Log',icon_url=ctx.guild.me.avatar_url)
      await bot.get_channel(1022433167686254622).send(embed=embed)
      
  except Exception as e:
    await print(e)

@bot.command()
async def nick(ctx,*,name=None):
  try:
    boosters = discord.utils.get(ctx.guild.roles,id=1008718416057737287).members
    staff = discord.utils.get(ctx.guild.roles,id=1008745408756977684).members
    if ctx.author in boosters or ctx.author in staff:
      with open('Telstra.json','r') as f:
        d = json.load(f)
      if len(name) > 20:
        await ctx.reply('**Names cannot be longer than 20 letters. `max 20`**',mention_author=False)
      elif name is None:
        await ctx.reply('**Name field cannot be emply.** `-nick [name]`',mention_author=False)
      else:
        try:
          elo = d[str(ctx.author.id)]
          await ctx.author.edit(nick=f'{elo} ✧ {name}')
        except:
          await ctx.author.edit(nick=name)
        await ctx.reply(f'**Nick successfully updated to "{name}".**',mention_author=False)
    else:
      await ctx.reply('**You must be a booster or staff to use this command.**',mention_author=False)
  except Exception as e:
    print(e)
    
#WORK IN PROGRESS
@bot.event
async def on_voice_state_update( member, before: discord.VoiceState, after: discord.VoiceState):
  perms = discord.PermissionOverwrite
  x = member
  ov = {member.guild.default_role: discord.PermissionOverwrite(connect=False,view_channel=True)}
  try: #RTB (1v1)
    ch = bot.get_channel(990194358609408020)
    member_list = ch.members
    if len(ch.members) == 2:
      with open('game','r') as ff:
        fff = int(ff.read())
      g = f'RTB #{fff} ↓'
      with open('game', 'w') as f:
        f.write(str(fff+1))
      
      c = await member.guild.create_category(g)
      vc = await c.create_voice_channel("✧・RTB {1v1}",user_limit=2)
      t = await c.create_text_channel('✦・game-chat',overwrites={member.guild.default_role:perms(view_channel=False)})
      for i in ch.members:
        await t.set_permissions(i,view_channel=True)
        await i.move_to(vc)
        await t.send(i.mention)
        await vc.set_permissions(i,connect=True)
      ########LOG
      members = str([i.mention for i in ch.members]).replace('[','').replace(']','').replace("'","").replace(",","\n")
      embed = discord.Embed(title=g,color=eclr,description=f'***RTB 1v1*** *game at <t:{str(time.time())[:10]}>*')
      embed.add_field(name=f'Members [{len(ch.members)}]', value=members)
      embed.set_author(name='Telstra | Game Log', icon_url=member.guild.me.avatar_url)
      await (bot.get_channel(1008780010187935804)).send(embed=embed)
###########      
      def ChannelEmpty(p,x,d):
        return len(vc.members) == 0
      await bot.wait_for('voice_state_update', check=ChannelEmpty);await vc.delete();
      await c.delete(); await x.delete(); await t.delete()
  except:
    pass
  
  try: 
    queues = [990194874500395038,994816110811697162,990194667100459079,925717319508955161]
    if member.voice.channel.id == 990194874500395038:
      ch = bot.get_channel(990194874500395038)
      type = 'RTB';teamSize = '2v2'
      memA = 4
    if member.voice.channel.id == 994816110811697162:
      ch = bot.get_channel(994816110811697162)
      type = 'RBW';teamSize = '2v2'
      memA = 4
    if member.voice.channel.id == 990194667100459079:
      ch = bot.get_channel(990194667100459079)
      type = 'RBW';teamSize = '3v3'
      memA = 6
    if member.voice.channel.id == 925717319508955161:
      ch = bot.get_channel(925717319508955161)
      type = 'RBW';teamSize = '4v4'
      memA = 8
    if member.voice.channel.id in queues:
      member_list = [discord.utils.get(bot.get_all_members(), id=int(i)) for i in ch.voice_states.keys()]
      if len(ch.members) == memA:
        with open('game','r') as ff:
          fff = int(ff.read())
        g = f'{type} #{fff} ↓'
        with open('game', 'w') as f:
          f.write(str(fff+1))
        x = await member.guild.create_role(name=g)
        for i in queues:
          await bot.get_channel(i).set_permissions(x,connect=False)
        ov = {member.guild.default_role: perms(connect=False,view_channel=True),x: perms(connect=True)}
        c = await member.guild.create_category(g)
        lobby = await c.create_voice_channel("✧・Lobby",overwrites={member.guild.default_role:perms(connect=False)},user_limit=memA)
        team1 = await member.guild.create_voice_channel("✧・Team I {}".format('{'+teamSize+'}'),category=c,overwrites=ov,user_limit=(memA/2))
        team2 = await member.guild.create_voice_channel("✧・Team II {}".format('{'+teamSize+'}'),category=c,overwrites=ov,user_limit=(memA/2))
        
        await asyncio.sleep(2)
        
        for i in member_list:
          await i.move_to(lobby)
          await asyncio.sleep(0.1)

        role = discord.utils.get(member.guild.roles, name=g)
        await lobby.set_permissions(role,connect=True)

        t = await c.create_text_channel('✦・game-chat',overwrites={role:perms(view_channel=True),member.guild.default_role:perms(view_channel=False)})
        
        for i in member_list:
          await i.add_roles(role)

        with open('Telstra.json','r') as lb:
          lb = lb.read()
          get = json.loads(lb)
        ilb = []
        for i in member_list:
          if str(i.id) in get:
            tupl = (str(i.id),int(get[str(i.id)]))
          else:
            tupl = (str(i.id),0)
          ilb.append(tupl)
        ilb.sort(key=lambda x:x[1],reverse=True)
        p = [discord.utils.get(member.guild.members,id=int(x[0])) for x in ilb]
        mList = list()
        cT1 = p[0]
        cT2 = p[1]
        rT1 = str(cT1.id)
        rT2 = str(cT2.id)
        optionL = list()
        for i in p:
          if i.id not in [cT1.id,cT2.id]:
            optionL.append(SelectOption(label=f'{i.name}',value=f'{i.id}'))

        #CAPTAIN 1 PICKING 1
        #await t.send(optionL)
        a = await t.send(f'**{bot.get_user(cT1.id).mention} Pick a player to be in your team.**',components=[Select(placeholder='Pick a player.',options=optionL,custom_id=str(rT1))])
        T1 = 0
        T1P = [cT1.id]
        while T1 == 0:
          interaction = await bot.wait_for("select_option",check=lambda inter: inter.custom_id==str(rT1) and str(inter.user.id) == rT1)
        #  print(interaction)
        #  print(rT1)

          T1P.append(interaction.values[0])
          for i in optionL:
            if i.value == interaction.values[0]:
              optionL.remove(i)

          await a.edit(bot.get_user(int(interaction.values[0])).mention+' is now in **Team 1**',components=[])
          T1 = 1
        #await t.send(optionL)

        #CAPTAIN 2 PICKING 1
        #await t.send(optionL)
        b = await t.send(f'**{bot.get_user(cT2.id).mention} Pick a player to be in your team.**',components=[Select(placeholder='Pick a player.',options=optionL,custom_id=str(rT2))])
        T2 = 0
        T2P = [cT2.id]
        while T2 == 0:
          interaction = await bot.wait_for("select_option",check=lambda inter: inter.custom_id==str(rT2) and str(inter.user.id) == rT2)
        #  print(interaction)
        #  print(rT1)

          T2P.append(interaction.values[0])
          for i in optionL:
            if i.value == interaction.values[0]:
              optionL.remove(i)

          await b.edit(bot.get_user(int(interaction.values[0])).mention+' is now in **Team 2**',components=[])
          T2 = 1
        if teamSize == '2v2':
          for i in T1P:
            try:
              i = discord.utils.get(member.guild.members,id=int(i))
              await i.move_to(team1)
            except:
              pass
          for i in T2P:
            try:
              i = discord.utils.get(member.guild.members,id=int(i))
              await i.move_to(team2)
            except:
              pass
        elif teamSize in ['3v3','4v4']:
          
          #CAPTAIN 1 PICKING 2
          c = await t.send(f'**{bot.get_user(cT1.id).mention} Pick a player to be in your team.**',components=[Select(placeholder='Pick a player.',options=optionL,custom_id=str(rT1)+'b')])
          T1 = 0
          while T1 == 0:
            interaction = await bot.wait_for("select_option",check=lambda inter: inter.custom_id==str(rT1)+'b' and str(inter.user.id) == rT1)

            T1P.append(interaction.values[0])
            for i in optionL:
              if i.value == interaction.values[0]:
                optionL.remove(i)
  
            await c.edit(bot.get_user(int(interaction.values[0])).mention+' is now in **Team 1**',components=[])
            T1 = 1

          #CAPTAIN 2 PICKING 2
          d = await t.send(f'**{bot.get_user(cT2.id).mention} Pick a player to be in your team.**',components=[Select(placeholder='Pick a player.',options=optionL,custom_id=str(rT2)+'b')])
          T2 = 0
          while T2 == 0:
            interaction = await bot.wait_for("select_option",check=lambda inter: inter.custom_id==str(rT2)+'b' and str(inter.user.id) == rT2)
  
            T2P.append(interaction.values[0])
            for i in optionL:
              if i.value == interaction.values[0]:
                optionL.remove(i)
  
            await d.edit(bot.get_user(int(interaction.values[0])).mention+' is now in **Team 2**',components=[])
            T2 = 1

        if teamSize == '3v3':
          for i in T1P:
            try:
              i = discord.utils.get(member.guild.members,id=int(i))
              await i.move_to(team1)
            except:
              pass
          for i in T2P:
            try:
              i = discord.utils.get(member.guild.members,id=int(i))
              await i.move_to(team2)
            except:
              pass
        elif teamSize == '4v4':
          #CAPTAIN 1 PICKING 3
          e = await t.send(f'**{bot.get_user(cT1.id).mention} Pick a player to be in your team.**',components=[Select(placeholder='Pick a player.',options=optionL,custom_id=str(rT1)+'c')])
          T1 = 0
          while T1 == 0:
            interaction = await bot.wait_for("select_option",check=lambda inter: inter.custom_id==str(rT1)+'c' and str(inter.user.id) == rT1)

            T1P.append(interaction.values[0])
            for i in optionL:
              if i.value == interaction.values[0]:
                optionL.remove(i)
  
            await interaction.e(bot.get_user(int(interaction.values[0])).mention+' is now in **Team 1**',components=[])
            T1 = 1

          #CAPTAIN 2 PICKING 3
          f = await t.send(f'**{bot.get_user(cT2.id).mention} Pick a player to be in your team.**',components=[Select(placeholder='Pick a player.',options=optionL,custom_id=str(rT2)+'c')])
          T2 = 0
          while T2 == 0:
            interaction = await bot.wait_for("select_option",check=lambda inter: inter.custom_id==str(rT2)+'c' and str(inter.user.id) == rT2)
  
            T2P.append(interaction.values[0])
            for i in optionL:
              if i.value == interaction.values[0]:
                optionL.remove(i)
  
            await f.edit(bot.get_user(int(interaction.values[0])).mention+' is now in **Team 2**',components=[])
            T2 = 1
          for i in T1P:
            try:
              i = discord.utils.get(member.guild.members,id=int(i))
              await i.move_to(team1)
            except:
              pass
          for i in T2P:
            try:
              i = discord.utils.get(member.guild.members,id=int(i))
              await i.move_to(team2)
            except:
              pass
        ###LOG
        team1players = str([bot.get_user(int(i)).mention for i in T1P]).replace('[','').replace(']','').replace("'","").replace(",","\n")
        team2players = str([bot.get_user(int(i)).mention for i in T2P]).replace('[','').replace(']','').replace("'","").replace(",","\n")
        embed = discord.Embed(title=g,color=eclr,description=f'***{type} {teamSize}*** *game at <t:{str(time.time())[:10]}>*\n\n**Team 1:**\n{team1players}\n\n**Team 2:**\n{team2players}')
        embed.set_author(name='Telstra | Game Log', icon_url=member.guild.me.avatar_url)
        await (bot.get_channel(1008780010187935804)).send(embed=embed)
        with open('Games.json','r') as games:
            games = json.load(games)
        with open('Games.json','w') as file:
          games[g[4:]] = {}
          team1P = [bot.get_user(int(i)).id for i in T1P]
          team2P = [bot.get_user(int(i)).id for i in T2P]
          games[g[4:]]["Team 1"] = team1P 
          games[g[4:]]["Team 2"] = team2P
          json.dump(games,file,indent=4)
        await t.send(f'{role.mention} This game is ranked and **WILL** affect your elo.\n> <#1027839899329642547>\n> <#1027839890366418944>\n**If failed to comply, you will be warned accordingly.**')
        def ChannelEmpty(p,x,d):
          return len(lobby.members)+len(team1.members)+len(team2.members) == 0
        await bot.wait_for('voice_state_update', check=ChannelEmpty)
        try:
          await team1.delete()
          await team2.delete()
        except:
          pass
        await lobby.delete()
        await c.delete()
        await x.delete()
        await t.delete()
  except Exception as e:
    print(e)

@bot.command()
@commands.cooldown(1,30,commands.BucketType.user)
async def quit(ctx):
  if ctx.channel.name=='✦・game-chat':
    uID = uuid.uuid4()
    buttons = [Button(label="Yes", style="3", emoji = "✅", custom_id=f"Yes{uID}"), Button(label=f"No", style="4", emoji = "❎", custom_id=f"No{uID}")]
    embed = discord.Embed(description='**Quit currrent game?**\n Majority must vote **Yes** in order for the game to end.',color=eclr)
    embed.set_author(name='Telstra | Quit',icon_url=ctx.guild.me.avatar_url)
    r = discord.utils.get(ctx.author.guild.roles, name=ctx.channel.category.name)
    og = await ctx.reply(r.mention,embed=embed, components=[buttons], mention_author=False)
    y = []
    n = []
    votes = 0
    for i in ctx.channel.category.voice_channels:
      for m in i.members:
        if m in r.members:
          votes+=1
    while True:
      try:
        print(votes)
        interaction = await bot.wait_for("button_click")
        if interaction.user in r.members:
          if len(y+n) != votes:
            if interaction.custom_id == f'Yes{uID}':
              if interaction.user.id in y+n:
                await interaction.send(content='**Vote already submitted!**')
                pass
              else:
                y.append(interaction.user.id)
                await interaction.send(content='**Your vote (Yes) has been submitted!**',ephemeral=True)
                print(y)
                y = y
            if interaction.custom_id == f'No{uID}':
              if interaction.user.id in y+n:
                await interaction.send(content='**Vote already submitted!**')
                pass
              else:
                n.append(interaction.user.id)
                await interaction.send(content='**Your vote (No) has been submitted!**',ephemeral=True)
                print(y)
                n = n
          else:
            if len(y) >= int(round((votes/2),0)):
              for i in ctx.channel.category.voice_channels:
                await i.delete()
              for i in ctx.channel.category.text_channels:
                await i.delete()
              await r.delete()
              os.remove(f'{ctx.channel.category.name}.pxd')
              await ctx.channel.category.delete()
            else:
              await ctx.message.delete()
              await og.delete()
        else:
          pass
      except Exception as e:
        print(e)

@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name="for -help | Telstra"))
  DiscordComponents(bot)
  print(f"{bot.user} is online!")
  ch = bot.get_channel(991170127804506182)
  embed=discord.Embed(description=f'**Bot Hourly Restart Completed! Bot will restart again in an hour.**',timestamp=datetime.datetime.now(),color=eclr)
  embed.set_author(name='Telstra | Hourly Restart',icon_url=ch.guild.me.avatar_url)
  await bot.get_channel(1028205508651388948).purge(limit=10)
  await bot.get_channel(1028205508651388948).send(embed=embed)
  await ch.purge(limit=10)
  buttons = [
    Button(
      label="Open Ticket",
      style="3",
      emoji= "📨", 
      custom_id="ticket"
    )
  ]
  e = discord.Embed(description=f'*Do not open tickets without any reason.* *If failed to comply you will get warned.*\n*After opening tickets stay patient since staff may take some time to respond.*\n*If a ticket is left inactive for long it will be closed by staff.*\n\n*Some valid reasons to open tickets are: `Reports` `Support` `Appeals`\n\n**click the button below to open a ticket***',color=eclr)
  e.set_author(name='Telstra | Tickets',icon_url=ch.guild.me.avatar_url)
  await ch.send(embed=e, components=[buttons])
  while True:
    try:
      p = await bot.wait_for("button_click")
      if p.custom_id == 'ticket':
        if p.user.id not in ticket_black_list: 
          r = discord.utils.get(ch.guild.roles, name='Staff Team')
          tn = str(p.user.name)[0]+str(random.randint(100,999))
          c = await ch.guild.create_text_channel(f'✦・ticket-{tn}',overwrites={r:discord.PermissionOverwrite(view_channel=True),p.user:discord.PermissionOverwrite(view_channel=True),ch.guild.default_role:discord.PermissionOverwrite(view_channel=False)})
          await p.send(content = f"Ticket Opened! {c.mention}", ephemeral = True)
          em = discord.Embed(title=c.name,description=f'*Ticket opened by {p.user.mention}* at <t:{str(time.time())[:10]}>',color=eclr)
          em.set_author(name='Telstra | Ticket Log',icon_url=ch.guild.me.avatar_url)
          await (bot.get_channel(1011669267831345263)).send(embed=em)
          emb = discord.Embed(description='**Please remain patient, staff will be with you as soon as possible!**',color=eclr)
          emb.set_author(name=f'Telstra | Ticket #{tn}',icon_url=ch.guild.me.avatar_url)
          await c.send(p.user.mention + r.mention, embed=emb)
        else:
          await p.send('**You can no longer open tickets! This maybe due to:\n> Spamming tickets.\n> Opening useless tickets often.\n> Opening false tickets.**')
    except:
      pass
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    if ctx.command.name == 'suggest':
      t = str(f'**{(round(int(error.retry_after)))}** seconds.').replace('.0','')
    elif ctx.command.name == 'quit':
      t = str(f'**{(round(int(error.retry_after)))}** seconds.').replace('.0','')
    elif ctx.command.name == 'background':
      t = str(f'**{(round(int(error.retry_after)))}** seconds.').replace('.0','')
    elif ctx.command.name == 'stats':
      t = str(f'**{(round(int(error.retry_after)))}** seconds.').replace('.0','')
    elif ctx.command.name == 'leaderboard':
      t = str(f'**{(round(int(error.retry_after)))}** seconds.').replace('.0','')
    elif ctx.command.name == 'add':
      t = str(f'**{(round(int(error.retry_after)))}** seconds.').replace('.0','')
    else:
      t = str(f'{(round(int(error.retry_after)/60,0))} minutes.').replace('.0','')
    msg = discord.Embed(description=f"**Command is on cooldown!** you can try again in {t}",color=eclr)
    msg.set_author(name='Telstra | Cooldown',icon_url=ctx.guild.me.avatar_url)
    if ctx.command.name == 'rtb':
      with open('rtb', 'r') as f:
        ff = f.read()
      msg.set_footer(text=f'command last ran by {ff}')
    if ctx.command.name == 'rbw':
      with open('rbw','r') as f:
        ff = f.read()
      msg.set_footer(text=f'command last ran by {ff}')
    await ctx.reply(embed=msg,mention_author=False)

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command(cooldown_after_parsing=True)
@commands.cooldown(1,1200,commands.BucketType.guild)
async def rbw(ctx, *,message=None):
  p = '<:pivot:1038379059467538462>'
  s = '<:stack:1038379067260538961>'
  if ctx.author.voice is None:
    voice = 0
  else:
    voice = ctx.author.voice.channel.id
  if voice not in [990194667100459079,925717319508955161,994816110811697162]:
    a = discord.Embed(description=f'**{p} You need to be in a queue! \n{s} <#994816110811697162>\n{s} <#990194667100459079>\n{s} <#925717319508955161>\n{p} Join one of the channels to use it!**',color=eclr);a.set_author(name='Telstra | RBW Ping',icon_url=ctx.guild.me.avatar_url);await ctx.reply(embed=a,mention_author=False)
    ctx.command.reset_cooldown(ctx)
  else:
    rbw = discord.utils.get(ctx.guild.roles, id=925717318582013981)
    f = open('rbw', 'w')
    f.write(ctx.author.name)
    f.close()
    if message is None:
      message = f"{ctx.author.mention} Wants To Play RBW!"
    embed = discord.Embed(description=f'**{p} {message}**\n**{s} Voice Channel:** {ctx.author.voice.channel.mention}\n**{s} Players in Queue: **{len(ctx.author.voice.channel.members)}', color=eclr) 
    embed.set_footer(icon_url=ctx.author.avatar_url,text=f'{ctx.author.name} | Telstraㅤㅤㅤ')
    embed.set_author(name='Telstra | RBW Ping',icon_url=ctx.guild.me.avatar_url)
    await ctx.channel.purge(limit=1)
    ch = bot.get_channel(1027839723579904051)
    oh = await ch.send(rbw.mention,embed=embed)
    await oh.add_reaction('<:pxd:1023154592927715368>')

@bot.command(cooldown_after_parsing=True)
@commands.cooldown(1,1200,commands.BucketType.guild)
async def rtb(ctx, *,message=None):
  voice = ctx.author.voice
  p = '<:pivot:1038379059467538462>'
  s = '<:stack:1038379067260538961>'
  if voice is None:
    a = discord.Embed(description='**{p} You need to be in <#990194358609408020> or <#990194874500395038> to use this command!**',color=eclr);await ctx.send(embed=a)
    ctx.command.reset_cooldown(ctx)
  else:
    rtb = discord.utils.get(ctx.guild.roles, id=990199064882741338)
    f = open('rtb', 'w')
    f.write(ctx.author.name)
    f.close()
    if message is None:
      message = f"{ctx.author.mention} Wants To Play RTB!"
    embed = discord.Embed(title=f"", description=f'**{p} {message}**\n**{s} Voice Channel: **{ctx.author.voice.channel.mention}\n**{s} Players in Queue: **{len(ctx.author.voice.channel.members)}', color=eclr) 
    embed.set_footer(icon_url=ctx.author.avatar_url,text=f'{ctx.author.name} | Telstraㅤㅤㅤ')
    await ctx.channel.purge(limit=1)
    ch = bot.get_channel(1027839711894568990)
    oh = await ch.send(rtb.mention, embed=embed)
    await oh.add_reaction('<:pxd:1023154592927715368>')

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def suggest(ctx, *, suggestion=None):
  try:
    p = '<:pivot:1038379059467538462>'
    s = '<:stack:1038379067260538961>'
    if ctx.author.id not in suggestion_black_list:
      if suggestion is None:
        await ctx.reply(f'**{p} Please type a suggestion.**')
        pass
      else:
        if len(suggestion) < 10:
          await ctx.reply(f'**{p} Suggestion cannot be shorter than 10 letters!**')
          return
        if ctx.guild.id == 925717318582013972:
          suggestion = suggestion.replace('\n',f'\n{s} ')
          embed = discord.Embed(description=f'**{p} [SUBMITTER](https://a)**\n{s} {ctx.author.mention}\n\n**{p} [SUGGESTION](https://a)**\n{s} {suggestion}', color=eclr)
          embed.set_author(name='Telstra | Suggestion',icon_url=ctx.guild.me.avatar_url)
          embed.set_thumbnail(url=ctx.author.avatar_url)
          embed.set_footer(icon_url=ctx.author.avatar_url,text=f'{ctx.author} | {ctx.author.id} | Telstraㅤㅤㅤ')
          oh = await bot.get_channel(1027840422174797885).send(embed=embed)
          await oh.add_reaction('<:pxd:1023154592927715368>')
          await oh.add_reaction('<:pxd:1023154584945954907>')
          await ctx.message.delete()
          await ctx.send(f'**{ctx.author.mention} Thank you for your suggestion!**')
        else:
          await ctx.send('Sorry you cant use this command in your server')
    else:
      await ctx.reply(f'**{p} You are blacklisted from this command!**\n{s} **You can appeal in <#991170127804506182> if you think it is not justified**',mention_author=False)
  except Exception as e:
    await ctx.send(e)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def ct(ctx):
  if ctx.channel.name[:9] == '✦・ticket-':
    await ctx.channel.delete()
    em = discord.Embed(title=ctx.channel.name,description=f'*Ticket closed by {ctx.author.mention}* at <t:{str(time.time())[:10]}>',color=eclr)
    em.set_author(name='Telstra | Ticket Log',icon_url=ctx.guild.me.avatar_url)
    await (bot.get_channel(1011669267831345263)).send(embed=em)

@bot.command()
async def register(ctx, ign):
  if ctx.author.id in owners:
    try:  
      request = urllib.request.Request(f"https://apiv2.nethergames.org/v1/players/{ign}", headers={'User-Agent': 'Mozilla/91.0'})
      response = urllib.request.urlopen(request)
      get = json.loads(response.read().decode('UTF-8'))
      name = str(get["name"])
      await ctx.author.edit(nick=f'0 ✧ {name}')
      await ctx.reply('Successfully registered as')
    except Exception:
      await ctx.send('**Not a vailid name**\n**usage:** `-register <name>`')

@bot.command()
async def test(ctx,wl,m:discord.Member):
  if ctx.message.author.id in owners:
    try:
      if wl == 'lost':
        won = False
      else:
        won = True
      with open('Telstra.json','r') as f:
        d = json.load(f)
      if str(m.id) in d:
        w = d[str(m.id)]['wins']
        l = d[str(m.id)]['losses']
        if won is True:
          ww = w+1
          ll = l
        else:
          ll = l+1
          ww = w
        d[str(m.id)]['wins']=ww
        d[str(m.id)]['losses']=ll
        with open('Telstra.json','w') as f:
          json.dump(d,f,indent=4)
      else:
        d[str(m.id)] = {}
        if won is True:
          d[str(m.id)]['wins'] = 1
          d[str(m.id)]['losses'] = 0
        else:
          d[str(m.id)]['wins'] = 0
          d[str(m.id)]['losses'] = 1
        with open('Telstra.json','w') as f:
          json.dump(d,f,indent=4)
    except Exception as e:
      result = "".join(format_exception(e, e, e.__traceback__))
      await ctx.send(f"```py\n{result}\n```")

@bot.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, m:discord.Member=None):
  role = discord.utils.get(ctx.guild.roles, id=925717318598819921)
  await m.add_roles(role)
  muted = discord.Embed(description=f'**{m.mention} was muted by {ctx.author.mention}.**',color=eclr)
  muted.set_author(name='Telstra | Muted',icon_url=ctx.guild.me.avatar_url)
  await ctx.reply(embed=muted)
  await bot.get_channel(1019904509423652874).send(embed=muted)

@bot.command()
@commands.has_permissions(kick_members=True)
async def suspend(ctx, m:discord.Member=None):
  role = discord.utils.get(ctx.guild.roles, id=1018561617232928788)
  await m.add_roles(role)
  suspended = discord.Embed(description=f'**{m.mention} was suspended by {ctx.author.mention}.**',color=eclr)
  suspended.set_author(name='Telstra | Supension',icon_url=ctx.guild.me.avatar_url)
  await ctx.reply(embed=suspended)
  await bot.get_channel(1019904509423652874).send(embed=suspended)

@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx,m:discord.Member,t='discord',*,r='No reason.'):
  if t in ['discord','d','game','g']:
    try:
      logs = bot.get_channel(1019904509423652874)
      if t in ['discord','d']:
        with open('Warns.json','r') as f:
          d = json.load(f)
        if str(m.id) in d:
          discordWarns = d[str(m.id)]['discord']
          totalWarns = d[str(m.id)]['total']
          LifeTime = d[str(m.id)]['lifetime']
          d[str(m.id)]['discord']=discordWarns+1
          d[str(m.id)]['total']=totalWarns+1
          d[str(m.id)]['lifetime']=LifeTime+1
          d[str(m.id)]['warnings'][f'warn{LifeTime+1}']={}
          d[str(m.id)]['warnings'][f'warn{LifeTime+1}']['type'] = 'discord'
          d[str(m.id)]['warnings'][f'warn{LifeTime+1}']['reason'] = r  
        else:
          d[str(m.id)] = {}
          d[str(m.id)]['discord']=1
          d[str(m.id)]['game']=0
          d[str(m.id)]['total'] = 1
          d[str(m.id)]['lifetime'] = 1
          LifeTime = d[str(m.id)]['lifetime']
          discordWarns = d[str(m.id)]['discord']
          totalWarns = d[str(m.id)]['total']
          d[str(m.id)]['warnings']={}
          d[str(m.id)]['warnings'][f'warn{totalWarns}']={}
          d[str(m.id)]['warnings'][f'warn{totalWarns}']['type'] = 'discord'
          d[str(m.id)]['warnings'][f'warn{totalWarns}']['reason'] = r
          
        with open('Warns.json','w') as f:
          json.dump(d,f,indent=4)
          a = discord.Embed(description=f'**{ctx.author.mention} warned (discord) {m.mention} for "{r}"**',color=eclr)
          a.set_author(name='Telstra | Warning Log',icon_url=ctx.guild.me.avatar_url)
          await logs.send(embed=a)
          b=discord.Embed(description=f'**{m.mention} was warned for "{r}".**',color=eclr)
          b.set_author(name='Telstra | Warning',icon_url=ctx.guild.me.avatar_url)
          await ctx.reply(embed=b)
          if discordWarns+1 in [i*3 for i in range(1,100)]:
            role = discord.utils.get(ctx.guild.roles, id=925717318598819921)
            await m.add_roles(role)
            muted = discord.Embed(description=f'**{m.mention} has been muted.**',color=eclr)
            muted.set_author(name='Telstra | Muted',icon_url=ctx.guild.me.avatar_url)
            await ctx.reply(embed=muted)
      else:
        with open('Warns.json','r') as f:
          d = json.load(f)
        if str(m.id) in d:
          gameWarns = d[str(m.id)]['game']
          totalWarns = d[str(m.id)]['total']
          LifeTime = d[str(m.id)]['lifetime']
          d[str(m.id)]['game']=gameWarns+1
          d[str(m.id)]['total']=totalWarns+1
          d[str(m.id)]['lifetime']=LifeTime+1
          d[str(m.id)]['warnings'][f'warn{LifeTime+1}']={}
          d[str(m.id)]['warnings'][f'warn{LifeTime+1}']['type'] = 'game'
          d[str(m.id)]['warnings'][f'warn{LifeTime+1}']['reason'] = r
        else:
          d[str(m.id)] = {}
          d[str(m.id)]['discord']=0
          d[str(m.id)]['game']=1
          d[str(m.id)]['total'] = 1
          d[str(m.id)]['lifetime']=1
          gameWarns = d[str(m.id)]['game']
          totalWarns = d[str(m.id)]['total']
          LifeTime = d[str(m.id)]['lifetime']
          d[str(m.id)]['warnings']={}
          d[str(m.id)]['warnings'][f'warn{totalWarns}']={}
          d[str(m.id)]['warnings'][f'warn{totalWarns}']['type'] = 'game'
          d[str(m.id)]['warnings'][f'warn{totalWarns}']['reason'] = r
          
        with open('Warns.json','w') as f:
          json.dump(d,f,indent=4)
          a = discord.Embed(description=f'**{ctx.author.mention} warned (game) {m.mention} for "{r}"**',color=eclr)
          a.set_author(name='Telstra | Warning Log',icon_url=ctx.guild.me.avatar_url)
          await logs.send(embed=a)
          b=discord.Embed(description=f'**{m.mention} was warned for "{r}".**',color=eclr)
          b.set_author(name='Telstra | Warning',icon_url=ctx.guild.me.avatar_url)
          await ctx.reply(embed=b)
          if gameWarns+1 in [i*3 for i in range(1,100)]:
            role = discord.utils.get(ctx.guild.roles, id=1018561617232928788)
            await m.add_roles(role)
            sus = discord.Embed(description=f'**{m.mention} has been suspended.**',color=eclr)
            sus.set_author(name='Telstra | Suspension',icon_url=ctx.guild.me.avatar_url)
            await ctx.reply(embed=sus)
    except Exception as e:
      result = "".join(format_exception(e, e, e.__traceback__))
      await ctx.send(f"```py\n{result}\n```")

@bot.command(aliases=['clearwarn'])
@commands.has_permissions(kick_members=True)
async def removewarn(ctx,m:discord.Member,warn):
  with open('Warns.json','r') as f:
    d = json.load(f)
    if str(m.id) in d:
      if d[str(m.id)]["warnings"][f"warn{warn}"]["type"] == 'discord':
        discordWarns = d[str(m.id)]['discord']
        d[str(m.id)]['discord'] = discordWarns-1
      else:
        gameWarns = d[str(m.id)]['game']
        d[str(m.id)]['game'] = gameWarns-1
        
      totalWarns = d[str(m.id)]['total']
      d[str(m.id)]['total']=totalWarns-1
      warns = d[str(m.id)]["warnings"]
      warns.pop(f'warn{warn}',None)
      with open('Warns.json','w') as f:
        json.dump(d,f,indent=4)
      embed = discord.Embed(description=f'**Removed warning #{warn} from {m.mention}!**',color=eclr)
      embed.set_author(name='Telstra | Warning Removal',icon_url=ctx.guild.me.avatar_url)
      await ctx.reply(embed=embed)
      a = discord.Embed(description=f'**{ctx.author.mention} removed Warn #{warn} from {m.mention}**',color=eclr)
      a.set_author(name='Telstra | Warning Log',icon_url=ctx.guild.me.avatar_url)
      await bot.get_channel(1019904509423652874).send(embed=a)
    else:
      await ctx.reply('**Member does not have any warns!**')

@bot.command(aliases=['warns'])
@commands.has_permissions(kick_members=True)
async def warnings(ctx,m:discord.Member=None):
  if m is None:
    m = ctx.author
  with open('Warns.json','r') as f:
    d = json.load(f)
  if str(m.id) in d:
    embed = discord.Embed(description=f'**Warnings for {m.mention}**\n**- Total Warns:** {d[f"{m.id}"]["total"]}\n**- Game Warns:** {d[f"{m.id}"]["game"]}\n**- Discord Warns:** {d[f"{m.id}"]["discord"]}',color=eclr)
    embed.set_author(name='Telstra | Warningsㅤㅤㅤㅤㅤㅤㅤㅤ',icon_url=ctx.guild.me.avatar_url)
    try:
      for i in d[f"{m.id}"]["warnings"]:
        embed.add_field(name=str(i).replace('warn','Warn #'),value=f'**- Type:** {d[f"{m.id}"]["warnings"][f"{i}"]["type"]}\n**- Reason:** {d[f"{m.id}"]["warnings"][f"{i}"]["reason"]}',inline=False)
    except Exception as e:
      await ctx.send(e)
      pass
    await ctx.reply(embed=embed)
  else:
    await ctx.reply('**Member does not have any warnings yet!**')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def vc(ctx,id):
    try:
      ch = bot.get_channel(int(id))
      members = str([i.mention for i in ch.members]).replace('[','').replace(']','').replace("'","").replace(",","\n")
      embed = discord.Embed(color=eclr,description=members)
      await ctx.reply(embed=embed)
    except:
      await ctx.reply('**Bot ran into an error**')

@bot.command()
async def help(ctx,o=None):
  p = '<:pivot:1038379059467538462>'
  s = '<:stack:1038379067260538961>'
  embed = discord.Embed(color=eclr,description=f"\n{p} **[RBW / RTB](https://a/)**\n{s} *pings for Ranked Bedwars/Bridge. (with a message if provided.)*\n{s} *`-rbw [message]` / `-rtb [message]`*\n\n{p} **[SUGGEST](https://a/)**\n{s} *sends your suggestion to the suggestions channel.*\n{s} *`-suggest [suggestion]`*\n\n{p} **[NG](https://portal.nethergames.org/)**\n{s} *fetches a players stats from NetherGames API.*\n{s} *`-ng [player]`*\n\n{p} **[HOST](https://a/)**\n{s} *pings 'HOST' role to ask for private party.*\n{s} *`-host`*\n\n{p} **[SNIPE](https://a)**\n{s} *fetches the most recently deleted message.*\n{s} *`-snipe`*\n\n{p} **[ESNIPE](https://a)**\n{s} *fetches the most recently edited message.*\n{s} *`-esnipe`*\n\n{p} **[STATS](https://a)**\n{s} *fetches the players stats in Telstra.*\n{s} *`-stats [user]`*\n\n{p} **[LEADERBOARD](https://a)**\n{s} *fetches the player leaderboard in Telstra.*\n{s} *`-leaderboard [wins/streak/telstars]`*\n\n**{p} [SPECIAL](https://a)**\n{s} *lists the special commands for booster and staff.*\n{s} *`-help special`*")
  staff_embed = discord.Embed(color=eclr, description="\n**CLOSE**\n> *closes the game mentioned.*\n> *`-close [game]`*\n\n**CLOSE TICKET**\n> *closes the ticket in which the command is ran.*\n> *`-ct`*\n\n**REFRESH**\n> *moves everyone back into queue after moving them out.*\n> *`-refresh [VoiceChannelID]`*\n\n**MOVE**\n> *moves from one channel into another.*\n> *`-move [Move Into] [Move From]`*\n*> (Move from is not needed if you are in the channel)*\n\n**WARN**\n> *warns the member mentioned.*\n> *`-warn [member] [game/discord] [reason]`*\n\n**REMOVEWARN**\n> *removes a warning from the member mentioned.*\n> *`-removewarn [member] [warn number]`*\n\n**WARNINGS**\n> *displays all the warns a member has.*\n> *`-warnings [member]`*")
  special_embed = discord.Embed(color=eclr, description="\n**NICK**\n> *changes your nick name to the one given.*\n> *`-nick [name]`*\n\n**BACKGROUND**\n> *changes the background for you in stats command to the attachment.*\n> *`-background [reset]`*\n(reset field should not be included if you do not want it to be set to default)")
  embed.set_footer(text=f'Telstra | {ctx.author.name}', icon_url=ctx.author.avatar_url)
  embed.set_author(name="Telstra | Helpㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ",icon_url=ctx.guild.me.avatar_url)
  staff_embed.set_footer(text=f'Telstra | {ctx.author.name}', icon_url=ctx.author.avatar_url)
  staff_embed.set_author(name="Telstra | Staff Commandsㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ",icon_url=ctx.guild.me.avatar_url)
  special_embed.set_footer(text=f'Telstra | {ctx.author.name}', icon_url=ctx.author.avatar_url)
  special_embed.set_author(name="Telstra | Special Commandsㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ",icon_url=ctx.guild.me.avatar_url)
  if o == None:
    await ctx.reply(embed=embed,mention_author=False)
  elif o == 'staff':
    await ctx.reply(embed=staff_embed, mention_author= False)
  elif o == 'special':
    await ctx.reply(embed=special_embed, mention_author= False)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def embed(ctx, title, text, header='Telstra | Embed'):
  embed=discord.Embed(title=title,color=eclr,description=text)
  embed.set_author(name=header,icon_url=ctx.guild.me.avatar_url)
  await ctx.send(embed=embed)

@bot.command(aliases=['end'])
@commands.has_permissions(manage_messages=True)
async def close(ctx,id):
  try:
    c = discord.utils.get(ctx.guild.categories, name=f'RBW #{id} ↓')
    r = discord.utils.get(ctx.author.guild.roles, name=c.name)
    if id in c.name:
      try:
        os.remove(f'RBW #{id} ↓.pxd')
      except Exception:
        pass
      for i in c.voice_channels:
        await i.delete()
      for i in c.text_channels:
        await i.delete()
      await r.delete()
      await c.delete()
  except Exception:
    c = discord.utils.get(ctx.guild.categories, name=f'RTB #{id} ↓')
    r = discord.utils.get(ctx.author.guild.roles, name=c.name)
    if id in c.name:
      try:
        os.remove(f'RTB #{id} ↓.pxd')
      except Exception:
        pass
      for i in c.voice_channels:
        await i.delete()
      for i in c.text_channels:
        await i.delete()
      await r.delete()
      await c.delete()

@bot.command()
async def Telstars(ctx):
  embed = discord.Embed(description='**Telstars is a point system that players can earn by winning games in the server. For games lost points will deducted from the player. You can still choose not to play for the points using the UNRANKED option in the queue voting. \n\nTo register a win you must submit it with an image as proof using: `-submit [gameID] [winning team]`. It is highly recommended to not submit a unfair game. (such as a 4v3 due to a player leaving.)**\n\n**If a player disconnects after bedbreak it will be counted as a death regardless of the fact its not their fault**',color=eclr)
  embed.set_author(name='Telstra | Telstars',icon_url=ctx.guild.me.avatar_url)
  embed.set_image(url='https://cdn.discordapp.com/attachments/925717319022432304/1027871756616216576/unknown.png')
  await ctx.send(embed=embed)

@bot.command()
async def howtoplay(ctx):
  ch = bot.get_channel(1027839908020224020)
  embed = discord.Embed(description=f"If you wish to play Ranked Bedwars please proceed to <#990208446437679134> and type the following command -rbw (message). \n\nEveryone with RBW PING will be pinged and those who wish to play must join the queue channel.\n\nYou finally have a match starting. First read the rules here <#990622462226104360> .\n\n**THINGS YOU MUST KNOW BEFORE PLAYING RBW**\n\nThere are four roles in RBW listed below:\n\n1st Rusher / Bridger\n2nd Rusher / Tank\n3rd Rusher / Bed Breaker\n4th Rusher / Defender\n\n**First Rusher**: (Fastest/Consistent One Stacker) Gets 24-32 (mainly 28) Iron and one stacks up to high limit.\n\n**Second Rusher**: (Best PvPer) Gets 12 gold and 12 iron. Buys iron armor, 32 blocks and 16 ladders, going up the bridge placing ladders on every other block of the one stack.\n\n**Third Rusher**: (Bed Breaker) Gets 28 iron. Buys either shears and 32 blocks, Iron pickaxe and 32 blocks, or Pickaxe and Axe and 32 blocks\n\n**The defender**: (Forth rusher) Fourth rusher is expected to do a fast bed defense and come up fast. The most ideal bed defense for this is butterfly with wool, Which is both safe and fast to make. (Requires: 32 iron, 4 gold)\n\n**GIVE 8 IRON TO 1ST RUSHER, 3 GOLD TO 2ND RUSHER \n**\n\n**Telstars**\nIn order to gain telstar points after winning a game you must submit it with an image as proof. `-submit (gameID) (winning team)`. You cannot submit bridge games or 2v2 games of any kind. The game has to have been played using bot generated teams.\n\n`(Butterfly Bed Defence Tutorial)`", color=discord.Colour.from_rgb(133,0,0))
  embed.set_author(name="Telstra | HOW TO PLAY",icon_url=ctx.guild.me.avatar_url)
  embed.set_image(url="https://cdn.discordapp.com/attachments/930487083640979476/1007699290208075796/BedDefence.pxd.gif")
  oh = await ch.send(embed=embed)
  await oh.add_reaction('<:pxd:1023154592927715368>')

@bot.command(cooldown_after_parsing=True)
@commands.cooldown(1,1200,commands.BucketType.guild)
async def host(ctx):
  host = discord.utils.get(ctx.guild.roles, id=925717318582013976)
  message = f"**{ctx.author.mention} Wants a Private Party!**"
  embed = discord.Embed(title=f"", description=message, color=eclr) 
  embed.set_footer(icon_url=ctx.author.avatar_url,text=f'{ctx.author.name} | Telstraㅤㅤㅤ')
  await ctx.channel.purge(limit=1)
  await ctx.send(host.mention, embed=embed)

bot.deleted = {}
@bot.event
async def on_message_delete(message):
    bot.deleted[message.guild.id] = (message.content, message.author, message.channel.name,message.created_at)

bot.edited = {} 
@bot.event
async def on_message_edit(message_before, message_after):
  bot.edited[message_before.guild.id] = (message_before.content, message_before.author, message_before.channel.name, message_before.created_at)

@bot.command()
async def snipe(ctx):
  try:
    try:
      contents, author, channel_name, ttime = bot.deleted[ctx.guild.id] 
    except:
      await ctx.send("**No deleted messages found!**",mention_author=False)
      return
    ttime = ttime.strftime('at %r')
    embed = discord.Embed(description=f'>>> '+contents, color=eclr)
    embed.set_author(name=f"{author}", icon_url=author.avatar_url)
    embed.set_footer(text=f"in #{channel_name} | ({ttime})")
    await ctx.reply(embed=embed,mention_author=False)
  except Exception as e:
    await ctx.send(e)
  
#esnipe
@bot.command()
async def esnipe(ctx):
  try:
    try:
      contents, author, channel_name, ttime = bot.edited[ctx.guild.id]  
    except:
      await ctx.reply("**No edited messages found!**",mention_author=False)
      return
    ttime = ttime.strftime('at %r')
    embed = discord.Embed(description=f'>>> '+contents, color=eclr)
    embed.set_author(name=f"{author}", icon_url=author.avatar_url)
    embed.set_footer(text=f"in #{channel_name} | ({ttime})")
    await ctx.reply(embed=embed,mention_author=False)
  except Exception as e:
    await ctx.send(e)

@bot.event
async def on_message(message):
  await bot.process_commands(message)
  if bot.user.mention in message.content:
    embed = discord.Embed(title="", description="My Prefix is `-`\nFor more information do `-help`", color=eclr)
    await message.reply(embed=embed)
      
        
#          ****do not write code below this****
KeepOnline()
bot.run(my_secret)
