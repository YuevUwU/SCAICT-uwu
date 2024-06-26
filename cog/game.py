import discord
from discord.ext import commands
import os
import json
from cog.core.sql import write
from cog.core.sql import read
from cog.core.sql import link_sql
from cog.core.sql import end
import random

def getChannels():#要特殊用途頻道的列表，這裡會用來判斷是否在簽到頻簽到，否則不予授理
    
    with open(f"{os.getcwd()}/DataBase/server.config.json", "r") as file:
        return json.load(file)["SCAICT-alpha"]

stickers = getChannels()["stickers"]['logo']

class game(commands.Cog):
    # User can use this command to play ✊-🤚-✌️ with the bot in the command channel
    @discord.slash_command(name="rock_paper_scissors", description="玩剪刀石頭布")
    # useser can choose ✊, 🤚, or ✌️ in their command
    async def rock_paper_scissors(self, interaction, choice: discord.Option(str, choices=["✊", "🤚", "✌️"])):
        if (interaction.channel.id!=getChannels()["channel"]["commandChannel"]):
            await interaction.response.send_message("這裡不是指令區喔")
            return
        userId = interaction.user.id
        nickName = interaction.user
        CONNECTION,CURSOR=link_sql()#SQL 會話
        
        point = read(userId,'point',CURSOR)
        if point<5:
            await interaction.response.send_message("你的電電點不足以玩這個遊戲")
            end(CONNECTION,CURSOR)
            return
        if choice not in ["✊", "🤚", "✌️"]:
            await interaction.response.send_message("請輸入正確的選擇")
            end(CONNECTION,CURSOR)
            return
        botChoice = random.choice(["✊", "🤚", "✌️"])
        game_outcomes = {
            ("✌️", "✊"): 5,
            ("✌️", "🤚"): -5,
            ("✊", "✌️"): -5,
            ("✊", "🤚"): 5,
            ("🤚", "✌️"): 5,
            ("🤚", "✊"): -5,
        }

        if botChoice == choice:
            await interaction.response.send_message(content=f"我出{botChoice}，平手。你還有{point}{stickers}")
        else:
            point += game_outcomes[(botChoice, choice)]
            result = "你贏了" if game_outcomes[(botChoice, choice)] > 0 else "你輸了"
            await interaction.response.send_message(content=f"我出{botChoice}，{result}，你還有{point}{stickers}")
            print(f"{userId},{nickName} Get {game_outcomes[(botChoice, choice)]} point by playing rock-paper-scissors")
        write(userId, 'point',point ,CURSOR)
        end(CONNECTION,CURSOR)
    @discord.slash_command(name="number_status", description="數數狀態")
    async def numberStatus(self, interaction):
        CONNECTION,CURSOR=link_sql()#SQL 會話
        CURSOR.execute("SELECT seq FROM game")
        nowStatus=CURSOR.fetchone()[0]
        end(CONNECTION,CURSOR)
        embed = discord.Embed(
            title="現在數到",
            description=f"{nowStatus} (dec) 了，接下去吧!",
            color=0xff24cf,
            )
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(game(bot))
