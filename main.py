import discord
import os
import tft_graphs
from api_tft_data_downloader import ApiTFTDataDownloader

from config import API_KEY, NICKNAMES, DISCORD_KEY


class Discord(discord.Client):

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    # async def on_message(self, message):
    #     # we do not want the bot to reply to itself
    #     if message.author.id == self.user.id:
    #         return
    #
    #     if message.content.startswith('!check'):
    #         message_discord = ''
    #         for nickname in NICKNAMES:
    #             info = ApiTFTDataDownloader(nickname)
    #             info_for_discord = info.info_execute_functions()
    #             message_discord += info_for_discord
    #             # graph
    #             tft_graphs.portable_execute_func()
    #             with open("..\\tft\\graphs\\" + nickname + '.png', 'rb') as file:
    #                 picture = discord.File(file)
    #                 await message.channel.send(file=picture)
    #         await message.channel.send(message_discord)
    #         self.remove_files()

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        nickname = message.content
        message_discord = ''

        print(nickname)
        if message.author.id == self.user.id:
            return
        if nickname not in NICKNAMES:
            return
        if message.content.startswith(nickname):
            info = ApiTFTDataDownloader(nickname)
            info_for_discord = info.info_execute_functions()
            message_discord += info_for_discord
            # graph
            tft_graphs.portable_execute_func()
            filename = os.path.join("graphs", f"{nickname}.png" )
            with open(filename, 'rb') as file:
                picture = discord.File(file)
                await message.channel.send(file=picture)
            await message.channel.send(message_discord)
            self.remove_files()

    @staticmethod
    def remove_files():
        for nickname in NICKNAMES:
            filename = os.path.join("graphs", f"{nickname}.png" )
            os.remove(filename)


def main():
    client = Discord()
    client.run(DISCORD_KEY)
    # for nickname in NICKNAMES:
    #     info = ApiTFTDataDownloader(nickname)
    #     info.info_execute_functions()


if __name__ == '__main__':
    main()
