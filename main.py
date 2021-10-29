# DiscordBot.py
import discord
import os

import random
from server import keep_alive

# アクティビティ取得のおまじない
# bot側にも別途設定する必要あり

intents = discord.Intents().all()
client = discord.Client(intents=intents)

# 起動、再起動時
@client.event
async def on_ready():
    # botがプレイしているゲーム
    act = [
        "MONSTER HUNTER RISE", "FINAL FANTASY VII",
        "Yu-Gi-Oh! Legacy of the Duelist Link Evolution", "Among Us",
        "Devil May Cry 5", "ウマオカン プリティーダービー ～勝ち取りたいものもない～",
        "Hikakin_mania","ゼERO"
    ]
    u = 0
    for e in act:
        u += 1
    gane = random.randint(0, u - 1) #プレイしているゲームをランダムに設定

    if(act[gane]=="Hikakin_mania" or act[gane]=="ゼERO"):
      activity = discord.Activity(type=discord.ActivityType.watching, name=act[gane])
    else:
      #プレイしているゲームをステータスに表示
      activity=discord.Game(name=act[gane])

    await client.change_presence(activity=activity)

    backup_channel = client.get_channel(867666631197982741) 
    # 再起動時にメッセージidが喪失するためバックアップしているチャンネルから再取得
    mst = await backup_channel.fetch_message(backup_channel.last_message_id)
    file = open('test.txt', 'w')
    file.write(str(mst.content))
    file.close()

# ボイスチャンネルのトリガーがひかれた場合
@client.event
async def on_voice_state_update(member, before, after):
    # gane=random.randint(0,u-1)
    # await client.change_presence(activity=discord.Game(name=act[gane]))
    channel = client.get_channel(838937936283828224)    # メッセージを送信するチャンネルid
    backup_channel = client.get_channel(867666631197982741) # 送ったメッセージのidをバックアップするチャンネルのid
    embeduser = '' # 埋め込みテキスト内のユーザー
    isum=0         # サーバー内で通話しているユーザーの合計
    i={"":0}       # ボイスチャンネルごとのユーザーの数(連想配列で宣言)
    for channels in client.get_all_channels():  # サーバー内のチャンネルidをすべて取得
        if(isinstance(channels,discord.channel.VoiceChannel)==True): # ボイスチャンネルのidの場合
          # 連想配列を使用しボイスチャンネルの名前で管理
          embeduser,i[channels.name]=meme(member,embeduser,channels.name,list(channels.voice_states.keys())) # ユーザー名、人数をチャンネルごとに取得
          isum+=i[channels.name]
    
    # 埋め込みテキストの編集
    embed = discord.Embed(title='通話中', description=embeduser)
    if before.self_stream is False and after.self_stream is True:
      embed = discord.Embed(title=f'{member.name}が{after.channel.name}にて配信中！！', description=embeduser)
    # 通話開始時
    if (isum == 1 and before.channel is None):
        # 埋め込みテキスト送信
        message = await channel.send(embed=embed)
        print(message.id)
        # 送信した埋め込みテキストのidを代入
        id = message.id
        # テキストチャンネルにバックアップ
        await backup_channel.send(id)
    if (before.channel is None or (before.channel and after.channel
                                   and before.channel != after.channel)):
        msg = '現在' + str(
            i[after.channel.name]) + f'人 @everyone <@{member.id}>が {after.channel.name} に参加しました。'
        await channel.send(msg)
        # 初回入室時
        if (isum == 1):
            print(message)
            print(id)
            print(type(id))
            # 送信した埋め込みテキストのidを代入
            message2 = id
            # txtファイルにidを書き込み
            file = open('test.txt', 'w')
            file.write(str(message2))
            file.close()
        else:
            file = open('test.txt', 'r')  #送信したメッセージidの読み込み
            message3 = int(file.read())
            # 埋め込みテキストの編集（更新）
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
            message3 = int(file.read())
            mst = await channel.fetch_message(message3)
            print(message3)
            print('a')
            await channel.send("@everyone 通話が終了しました。")
            #global message
            await mst.edit(embed=embed)
        else:
            #global message
            file = open('test.txt', 'r')  #送信したメッセージidの読み込み
            message3 = int(file.read())
            mst = await channel.fetch_message(message3)
            print(message3)
            #global message
            await mst.edit(embed=embed)
    else:
        file = open('test.txt', 'r')
        message3 = int(file.read())
        mst = await channel.fetch_message(message3)
        await mst.edit(embed=embed)
    if before.channel and after.channel:
        # カメラ配信開始時
        if before.self_video is False and after.self_video is True:
            print("video started!")
            await channel.send(
                f"@everyone <@{member.id}> が、{after.channel.name}でカメラ配信を始めました。"
            )
        # カメラ配信終了時
        elif after.self_video is False and before.self_video is True:
            await channel.send(f"<@{member.id}> {member.name}がカメラ配信を終了しました。")
        # 画面共有開始時
        elif before.self_stream is False and after.self_stream is True:
            print("streaming started!")
            # ゲームアクティビティが存在する場合
            try:
                await channel.send(
                    f"@everyone <@{member.id}> が、{after.channel.name}で「{member.activities[0].name}」の配信を始めました。"
                )
                embed = discord.Embed(title='配信タイトル', description=f'{member.activities[0].name}')

                embed.set_author(
                  name=member.name, # ユーザー名
                  icon_url=member.avatar_url # アイコンを設定
                )

                embed.add_field(name="チャンネル",value=after.channel.name)

                try:
                  embed.add_field(name=member.activities[0].details,value=member.activities[0].state)
                  embed.set_image(url=member.activities[0].large_image_url)
                except IndexError:
                  print("IndexError....");
                except AttributeError:
                  try:
                    embed.add_field(name=member.activities[0].details,value=member.activities[0].state)
                  except AttributeError:
                    print("AttributeError.....")
                await channel.send(embed=embed)
                # print(member.activities[0].large_image_url)
            # 存在しない場合
            except IndexError:
                await channel.send(
                    f"@everyone <@{member.id}> が、{after.channel.name}で画面共有を始めました。"
                )
        # 画面共有終了時
        elif after.self_stream is False and before.self_stream is True:
            await channel.send(f"<@{member.id}> が画面共有を終了しました。")


def meme(member, embeduser, chaname, m):
    i = 0   # 人数を数える
    print(member)
    # m,ボイスチャンネルごとのメンバーidがlist型で格納されている。
    for member in m:
        print(member)
        print(m)
        if i == 0:  # 最初の処理時、チャンネルの名前を格納
            embeduser += f'{chaname}' + '\n'
        # メンバーidを代入
        embeduser += f'<@{m[i]}>' + '\n'
        i += 1
    return embeduser, i


keep_alive()
client.run(os.environ['TOKEN'])
