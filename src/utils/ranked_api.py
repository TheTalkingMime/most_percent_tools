import requests
from utils.utils import map_ign_to_name
import os
import json


class BaseMatchData:
    def __init__(self):
        self.data = self._fetch_match_data()
        self.timeline = self._fetch_timeline()
        self.player_names = self._get_player_names()
        self.player_uuids = self._get_player_uuids()

    def _fetch_match_data(self) -> dict:
        pass

    def _fetch_timeline(self) -> list:
        timeline = self.data['data']['timelines']
        timeline.reverse()
        return timeline

    def _get_player_names(self) -> list:
        player_data = self.data['data']['players']
        return [map_ign_to_name(player.get('nickname')) for player in player_data]


    def _get_player_uuids(self) -> list:
        return [player.get('uuid') for player in self.data['data']['players']]

    @property
    def timeline(self) -> list:
        self.data = self._fetch_match_data()
        return self._fetch_timeline()
    
    @timeline.setter
    def timeline(self, value):
        pass

class LiveMatchData(BaseMatchData):
    def __init__(self, uuid: str, private_key: str):
        self.uuid = uuid
        self.private_key = private_key
        super().__init__()

    def _fetch_match_data(self) -> dict:
        headers = {
            'private-key': self.private_key
        }

        response = requests.get(f'https://mcsrranked.com/api/users/{self.uuid}/live', headers=headers).json()

        with open(os.path.join(os.path.dirname(__file__), 'last_live_match.json'), 'w+', encoding='utf-8') as f:
            json.dump(response, f, ensure_ascii=False, indent=2)
        return response


class PostMatchData(BaseMatchData):
    def __init__(self, match_id: int):
        self.match_id = match_id
        super().__init__()

    def _fetch_match_data(self) -> dict:
        return requests.get(f"https://mcsrranked.com/api/matches/{self.match_id}").json()
