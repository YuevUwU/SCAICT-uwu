# Standard imports
import asyncio
import json
import os
# Local imports
from cog.core.sql import link_sql
from cog.core.sql import end

def open_json():
    # open configuration file
    os.chdir("./")
    with open(f"{os.getcwd()}/DataBase/server.config.json", "r", encoding = "utf-8") as file:
        global_settings = json.load(file)
    return global_settings

def get_total_points():
    connection, cursor = link_sql()
    cursor.execute("SELECT SUM(point) FROM `USER`")
    points = cursor.fetchone()[0]
    end(connection, cursor)
    return points

async def update_channel(bot):
    channel = open_json()["SCAICT-alpha"]["channel"]
    await bot.wait_until_ready()
    guild = bot.get_guild(channel["serverID"]) # YOUR_GUILD_ID

    if guild is None:
        print("找不到指定的伺服器")
        return

    member_channel = guild.get_channel(channel["memberCount"]) # YOUR_CHANNEL_ID
    point_channel = guild.get_channel(channel["pointCount"])
    if channel is None:
        print("找不到指定的頻道")
        return

    while not bot.is_closed():
        points = get_total_points()
        total_members = guild.member_count
        await member_channel.edit(name = f"👥電池數：{total_members}")
        await point_channel.edit(name = f"🔋總電量：{points}")
        await asyncio.sleep(600)
