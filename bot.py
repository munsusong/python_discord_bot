import os
import random
import discord
import json
import requests
import os.path

from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup
from discord.ext import commands
# from dotenv import load_dotenv

# load_dotenv()
# DTOKEN = os.getenv('DISCORD_TOKEN')
# WTOKEN = os.getenv('WEATHER_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name='test', help='어쩌구 저쩌구')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        '안녕',
        '와우!',
        (
            '난 아니지만 '
            '성현우는 확실하다.'
        ),
    ]
    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='채팅채널생성', help='채팅채널을 생성합니다. (ex:!채팅채널생성 채팅채널)')
@commands.has_role('admin')
async def create_textchannel(ctx, channel_name: str):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        await guild.create_text_channel(channel_name)
        await ctx.send(f'\'{channel_name}\' 채널을 만들었어요.')
    else:
        await ctx.send('이미 동일한 이름의 서버가 있어요.')


@bot.command(name='음성채널생성', help='음성채널을 생성합니다. (ex:!음성채널생성 음성채널)')
@commands.has_role('admin')
async def create_voice_channel(ctx, channel_name: str):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        await guild.create_voice_channel(channel_name)
        await ctx.send(f'\'{channel_name}\' 채널을 만들었어요.')
    else:
        await ctx.send('이미 동일한 이름의 서버가 있어요.')


@bot.command(name='추방', help='지정한 멤버를 추방합니다. (ex:!추방 추방할대상 추방사유)')
@commands.has_role('admin')
async def kick(ctx, member: str, reason: str):
    guild = ctx.guild
    temp = discord.utils.get(guild.members, name=member)
    if temp:
        await guild.kick(temp)
        await ctx.send(f'\'{member}\' 멤버를 추방했어요.\n 사유: {reason}')
    else:
        await ctx.send('해당 멤버는 존재하지 않아요.')


@bot.command(name='밴', help='지정한 멤버를 밴합니다. (ex:!밴 밴할대상 밴사유)')
@commands.has_role('admin')
async def ban(ctx, member: str, reason: str):
    guild = ctx.guild
    temp = discord.utils.get(guild.members, name=member)
    if temp:
        await guild.ban(temp)
        await ctx.send(f'\'{member}\' 멤버를 밴했어요.\n 사유: {reason}')
    else:
        await ctx.send('해당 멤버는 존재하지 않아요.')


@bot.command(name='밴목록', help='현재까지 밴 목록을 출력합니다. (ex:!밴목록)')
@commands.has_role('admin')
async def banlist(ctx):
    guild = ctx.guild
    bans = await guild.bans()
    if bans:
        blist = [
            f'{User.user}' for User in bans]
        await ctx.send('🤣밴 목록🤔 ')
        await ctx.send('\n'.join(blist))
    else:
        await ctx.send('밴한 멤버가 없어요.')


@bot.command(name='언밴', help='지정한 멤버의 밴을 해제합니다. (ex:!언밴 언밴할대상 언밴사유)')
@commands.has_role('admin')
async def unban(ctx, member: str, reason: str):
    guild = ctx.guild
    bans = await guild.bans()
    if bans:
        blist = []
        for User in bans:
            blist.append(User.user)

    for search in blist:
        if member == search.name:
            await guild.unban(search)
            await ctx.send(f'\'{search}\' 멤버를 언밴했어요.\n 사유: {reason}')
        else:
            await ctx.send('해당 멤버는 밴되지 않았어요.')


@bot.command(name='초대', help='현재 채팅방의 초대 링크를 생성합니다. (ex:!초대)')
@commands.has_role('admin')
async def invite(ctx):
    text = await ctx.channel.create_invite()
    await ctx.send(text)


# @bot.command(name="날씨", help='날씨를 검색합니다. (ex:!날씨 지역영어이름)')
# async def weather(ctx, location: str):
#     url = (
#         f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WTOKEN}')
#     r = requests.get(url)
#     if r:
#         data = json.loads(r.text)
#         loc = data['name']
#         wea = data['weather'][0]['description']
#         await ctx.send("말씀하신 날씨 검색 결과에요")
#         await ctx.send("지역은 "+loc)
#         await ctx.send("날씨는 "+wea+" 에요")
#     else:
#         await ctx.send("해당 지역은 존재하지 않아요")

    # 네이버의 robots.txt에 따르면 네이버 메인을 제외한 사이트의 크롤링은 허가되어있지 않습니다.

@bot.command(name="날씨", help='날씨를 검색합니다. (ex:!날씨 지역이름)')
async def weather(ctx, location: str):
    word = ["지금 ", "내일 오전", "내일 오후", "모레 오전", "모레 오후"]
    url = parse.quote(location+"날씨")
    html = urlopen(
        "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query="+url)
    bsObject = BeautifulSoup(html, "html.parser")

    if bsObject.select(".todaytemp"):
        await ctx.send(location+" 날씨를 알려드릴께요")
        await ctx.send("기준 지역은 "+bsObject.select(".btn_select")[0].get_text()+" 이에요")
        for x in range(0, 5):
            await ctx.send(word[x]+": "+bsObject.select(".todaytemp")[x].get_text()+"'C "
                           + bsObject.select(".cast_txt")[x].get_text())
    else:
        await ctx.send("말씀하신 장소는 파악되지 않은 장소에요")


@bot.command(name="todo추가", help="할일을 추가합니다. (ex:!todo추가 todo에 적용할 항목)")
async def Todoadd(ctx, *temp: str):
    string = ""
    for t in temp:
        string += t + " "

    count = 1
    if(os.path.isfile('todo.txt')):
        f = open('todo.txt', 'r')
        lines = f.readlines()
        count = len(lines)+1
        f.close()

    with open('todo.txt', 'a') as f:
        f.write(f'{count}. {string}\n')
        await ctx.send("해당 메시지를 Todo에 추가했어요")


@bot.command(name="todo검색", help="Todo 중 입력한 단어를 검색합니다. (ex:!todo검색 검색할단어)")
async def Todosearch(ctx, *temp: str):
    string = ""
    for t in temp:
        string += t + " "
    await ctx.send(string.strip())
    if(os.path.isfile('todo.txt')):
        f = open('todo.txt', 'r')
        lines = f.readlines()
        await ctx.send(string+" 포함된 문장 목록이에요.")
        for r in lines:
            if string.strip() in r:
                await ctx.send(r)
        await ctx.send("검색된 항목을 보시고 \'!todo완료 번호\' 를 입력하여 완료시켜주세요.")
        f.close()
    else:
        await ctx.send("Todo목록이 확인되지 않아요")


@bot.command(name="todo완료", help="입력한 번호에 있는 todo를 완료합니다. (ex:!todo완료 번호)")
async def Todocomplete(ctx, temp: int):
    count = 1

    if(os.path.isfile('todo.txt')):
        f = open('todo.txt', 'r')
        lines = f.readlines()
        lines.pop(temp-1)
        f.close()
        ff = open('todo.txt', 'w')
        for e in lines:
            ff.write(f'{count}. {e[3:]}')
            count += 1
        ff.close()

        await ctx.send(f"{temp}번 작업이 완료되었어요.")
    else:
        await ctx.send("Todo목록이 확인되지 않아요")


@bot.command(name="todo목록", help="Todo 목록을 전체 출력합니다. (ex:!todo목록)")
async def Todolist(ctx):
    with open('todo.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            await ctx.send(line)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        error = str(error)
        if error.find('admin'):
            await ctx.send('admin 권한이 필요해요')
        else:
            await ctx.send('명령어 오류에요')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game('코딩매니저'))

bot.run(os.environ['token'])

# 노래, 주식
# 비로그인 회원 찾기 방법

# todo 단어 검색 강화(2가지 이상의 단어가 들어간 문장 조회기능)
# todo 단어를 이용한 완료(현재는 번호로 완료)
# todo 완료 여러개 동시에 할 수 있게
# todo
# 디스코드봇 호스팅
