
import requests
import json
from datetime import datetime
from config import API_KEY


class ApiTFTDataDownloader:

    def __init__(self, name):
        self.summoner_name = name

    def pretty_print(self, matches, wins, rank, places_and_dates):
        print(
            f"Nickname: {self.summoner_name} | Rank: {rank} | Matches: {matches} | Wins: {wins}")
        for place, date in places_and_dates:
            print(str(date) + ' Na miejscu: ' + str(place))
        print('=====================================')

    def get_info_for_discord(self, matches, wins, rank, places_and_dates):
        player_info = f"Nickname: {self.summoner_name} | Rank: {rank} | Matches: {matches} | Wins: {wins} \n"
        for place, date in places_and_dates:
            player_info += (str(date) + ' Na miejscu: ' + str(place) + '\n')
        player_info += '=' * 20
        player_info += '\n'
        return player_info

    @staticmethod
    def find_data(summoner_name):
        url = f"https://eun1.api.riotgames.com/tft/summoner/v1/summoners/by-name/{summoner_name}?api_key={API_KEY}"
        response = requests.get(url)
        response_py = json.loads(response.text)
        puuid = response_py['puuid']
        summoner_id = response_py['id']
        return puuid, summoner_id

    @staticmethod
    def get_rank(summoner_id):
        url = f"https://eun1.api.riotgames.com/tft/league/v1/entries/by-summoner/{summoner_id}?api_key={API_KEY}"
        response = requests.get(url)
        response_py = json.loads(response.text)
        matches = response_py[0]['wins'] + response_py[0]['losses']
        wins = response_py[0]['wins']
        rank = response_py[0]['tier'] + ' ' + response_py[0]['rank']
        return matches, wins, rank

    def get_matches_timestamp(self, puuid):
        url = f"https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count=20&api_key={API_KEY}"
        response = requests.get(url)
        response_py_matches = json.loads(response.text)
        places_and_dates = []
        for match_id in response_py_matches[:10]:
            url_timestamp = f"https://europe.api.riotgames.com/tft/match/v1/matches/{match_id}?api_key={API_KEY}"
            response_timestamp = requests.get(url_timestamp)
            response_py_timestamp = json.loads(response_timestamp.text)
            date = (
                datetime.fromtimestamp(response_py_timestamp['info']['game_datetime'] / 1000).replace(
                    microsecond=0))
            place = self.get_place(response_py_timestamp, puuid)
            places_and_dates.append((place, date))
        return places_and_dates

    @staticmethod
    def get_place(json_info, puuid):
        info_list = (json_info['info']['participants'])
        participants_list = (json_info['metadata']['participants'])
        player_index = participants_list.index(puuid)
        place = info_list[player_index]['placement']
        return place

    def info_execute_functions(self):
        puuid, summoner_id = self.find_data(self.summoner_name)
        matches, wins, rank = self.get_rank(summoner_id)
        places_and_dates = self.get_matches_timestamp(puuid)
        # self.pretty_print(matches, wins, rank, places_and_dates)
        info_for_discord = self.get_info_for_discord(matches, wins, rank, places_and_dates)
        return info_for_discord


def main():
    tft_data_downloader = ApiTFTDataDownloader


if __name__ == '__main__':
    main()
