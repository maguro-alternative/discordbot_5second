# DiscordBot.py
import discord
import os

import random
from server import keep_alive

intents = discord.Intents().all()
client = discord.Client(intents=intents)

act = [
    "MONSTER HUNTER RISE", "FINAL FANTASY VII",
    "Yu-Gi-Oh! Legacy of the Duelist Link Evolution", "Among Us",
    "Devil May Cry 5", "ウマオカン プリティーダービー ～勝ち取りたいものもない～"
]
u = 0
for e in act:
    u += 1


@client.event
async def on_ready():
    gane = random.randint(0, u - 1)
    await client.change_presence(activity=discord.Game(name=act[gane]))
    backup_channel = client.get_channel(867666631197982741)
    mst = await backup_channel.fetch_message(backup_channel.last_message_id)
    file = open('test.txt', 'w')
    file.write(str(mst.content))
    file.close()


@client.event
async def on_voice_state_update(member, before, after):
    # gane=random.randint(0,u-1)
    # await client.change_presence(activity=discord.Game(name=act[gane]))
    channel = client.get_channel(838937936283828224)    # メッセージを送信するチャンネルid
    backup_channel = client.get_channel(867666631197982741) # 送ったメッセージのidを送信し、記録するチャンネルid
    #members = channel.members
    embeduser = ''
    # for channels in client.get_all_channels():
        # if(isinstance(channels,discord.channel.VoiceChannel)==True): # and channel.topic
          # i={channels.name,isum}
          # print("チャンネルID：" + str(channel.id))
          # print(type(channel))
    isum=0
    i={"":0}
    for channels in client.get_all_channels():  # サーバー内のチャンネルidをすべて取得
        if(isinstance(channels,discord.channel.VoiceChannel)==True): # ボイスチャンネルのidの場合
          i[channels.name]=isum  # 連想配列を使用しボイスチャンネルの名前で管理
          embeduser,i[channels.name]=meme(member,embeduser,channels.name,list(channels.voice_states.keys())) # ユーザー名、人数をチャンネルごとに取得
          isum+=i[channels.name]
    
    embed = discord.Embed(title='通話中', description=embeduser)
    if before.self_stream is False and after.self_stream is True:
      embed = discord.Embed(title=f'{member.name}が{after.channel.name}にて配信中！！', description=embeduser)

    # print(i)
    if (isum == 1 and before.channel is None):
        message = await channel.send(embed=embed)
        print(message.id)
        print('a')
        id = message.id
        await backup_channel.send(id)
    if (before.channel is None or (before.channel and after.channel
                                   and before.channel != after.channel)):
        msg = '現在' + str(
            i[after.channel.name]) + f'人 @everyone <@{member.id}>が {after.channel.name} に参加しました。'
        await channel.send(msg)
        if (isum == 1):
            #message=await channel.send(embed=embed)
            print(message)
            print(id)
            print(type(id))
            message2 = id
            file = open('test.txt', 'w')
            file.write(str(message2))
            file.close()
        else:
            file = open('test.txt', 'r')  #送信したメッセージidの読み込み
            #discord.message.Message(message3)
            message3 = int(file.read())
            #discord.message.Message(message3)
            mst = await channel.fetch_message(message3)
            print(message3)
            print('a')
            #global message
            await mst.edit(embed=embed)
    if (after.channel is None or (before.channel and after.channel
                                  and before.channel != after.channel)):
        out = '現在' + str(
            i[before.channel.name]) + f'人　<@{member.id}> が {before.channel.name} から退出しました。'
        await channel.send(out)
        if isum == 0:
            embed = discord.Embed(title='通話終了', description=None)
            file = open('test.txt', 'r')  #送信したメッセージidの読み込み
            #discord.message.Message(message3)
            message3 = int(file.read())
            #discord.message.Message(message3)
            mst = await channel.fetch_message(message3)
            print(message3)
            print('a')
            await channel.send("@everyone 通話が終了しました。")
            #global message
            await mst.edit(embed=embed)
        else:
            #global message
            file = open('test.txt', 'r')  #送信したメッセージidの読み込み
            #discord.message.Message(message3)
            message3 = int(file.read())
            #discord.message.Message(message3)
            mst = await channel.fetch_message(message3)
            print(message3)
            print('a')
            #global message
            await mst.edit(embed=embed)
    else:
        file = open('test.txt', 'r')
        message3 = int(file.read())
        mst = await channel.fetch_message(message3)
        await mst.edit(embed=embed)
    if before.channel and after.channel:
        channel = client.get_channel(838937936283828224)
        if before.self_video is False and after.self_video is True:
            print("video started!")
            await channel.send(
                f"@everyone <@{member.id}> が、{after.channel.name}でカメラ配信を始めました。"
            )
        elif after.self_video is False and before.self_video is True:
            await channel.send(f"<@{member.id}> {member.name}がカメラ配信を終了しました。")
        elif before.self_stream is False and after.self_stream is True:
            print("streaming started!")
            try:
                await channel.send(
                    f"@everyone <@{member.id}> が、{after.channel.name}で「{member.activities[0].name}」の配信を始めました。"
                )
            except IndexError:
                await channel.send(
                    f"@everyone <@{member.id}> が、{after.channel.name}で画面共有を始めました。"
                )
        elif after.self_stream is False and before.self_stream is True:
            await channel.send(f"<@{member.id}> が画面共有を終了しました。")
    print(before.self_stream)
    print(after.self_stream)
    if member.activities[0].name: print(member.activities[0].name)
    print(type(member.activities))
    print(member)
    print(client.get_channel(838937936283828225).name)


def meme(member, embeduser, chaname, m):
    i = 0
    print(member)
    print("1")
    for member in m:
        print(member)
        print(m)
        #memids.append(m[i])
        if i == 0:
            embeduser += f'{chaname}' + '\n'
        embeduser += f'<@{m[i]}>' + '\n'
        i += 1
    return embeduser, i


keep_alive()
client.run(os.environ['TOKEN'])
