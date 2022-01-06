import sqlite3
from sqlite3 import Error
from config import NICKNAMES
from api_tft_data_downloader import ApiTFTDataDownloader
from datetime import date


class DatabaseExecutes:

    def __init__(self, database_path):
        self.database_path = database_path

    def create_connection(self):
        connection = None
        try:
            connection = sqlite3.connect(self.database_path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection

    @staticmethod
    def get_api_info(nickname):
        tft_API_downloader = ApiTFTDataDownloader(nickname)
        puuid, summoner_id = tft_API_downloader.find_data(nickname)
        matches, wins, rank = tft_API_downloader.get_rank(summoner_id)
        return rank

    def execute_query(self, query):
        connection = self.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_read_query(self, query):
        connection = self.create_connection()
        connection.row_factory = lambda cursor, row: row[0]
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            #result = [el[0] for el in result]
            # to samo co:
            # new_result = []
            # for el in result:
            #     new_result.append(el)
            # result = new_result

            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def insert_nicknames(self, nickname):
        create_user = f"""INSERT INTO players(nickname) VALUES ('{nickname}');"""
        self.execute_query(create_user)

    def execute_insert_nicknames(self):
        for nickname in NICKNAMES:
            self.insert_nicknames(nickname)

    def select_from_database(self, selected_info, nickname):
        sql_query = f"""SELECT {selected_info} FROM date_rank WHERE nickname = ('{nickname}');"""
        query_info = self.execute_read_query(sql_query)
        # for info in query_info:
        #     print(info)
        return query_info

    def insert_date_rank(self, nickname, rank):
        today = date.today()
        sql_insert = f"""INSERT INTO date_rank(date, rank, nickname) VALUES ('{today}', '{rank}', '{nickname}');"""
        self.execute_query(sql_insert)

    def execute_insert_date_rank(self):
        for nickname in NICKNAMES:
            rank = self.get_api_info(nickname)
            self.insert_date_rank(nickname, rank)


def main():
    database_executor = DatabaseExecutes(".\\tft_database.sqlite")
    #database_executor.execute_insert_date_rank()


if __name__ == '__main__':
    main()
