# Third-party imports
# import mysql.connector
# Local imports
from .sql import link_sql

connection, cursor = link_sql()

cursor.execute("USE DCSQLtest")
cursor.execute(
    "CREATE TABLE `USER` (\
        uid BIGINT NOT NULL,\
        loveuwu TINYINT(1) NOT NULL DEFAULT 0,\
        point INT NOT NULL DEFAULT 0,\
        ticket INT NOT NULL DEFAULT 0,\
        charge_combo INT NOT NULL DEFAULT 0,\
        next_lottery INT NOT NULL DEFAULT 0,\
        last_charge DATETIME NOT NULL DEFAULT '1970-01-01 00:00:00',\
        last_comment DATE NOT NULL DEFAULT '1970-01-01',\
        today_comments INT NOT NULL DEFAULT 0,\
        PRIMARY KEY (`uid`)\
    )"
)
cursor.execute(
    "CREATE TABLE `CommentPoints` (\
        seq INT AUTO_INCREMENT PRIMARY KEY,\
        uid BIGINT NOT NULL,\
        times INT NOT NULL DEFAULT 2,\
        next_reward INT NOT NULL DEFAULT 1,\
        FOREIGN KEY (`uid`) REFERENCES USER(`uid`) ON DELETE CASCADE\
    )"
)
cursor.execute(
    "CREATE TABLE `game` (\
        seq BIGINT NOT NULL DEFAULT 0,\
        lastID BIGINT DEFAULT 0\
    );\
    insert into game (seq) VALUES 0;"
)

# 查看所有databases
# cursor.execute("SHOW DATABASES")
# ret = cursor.fetchall()
# print(ret)

print("done")
cursor.close()
connection.commit()
connection.close()
