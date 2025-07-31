import requests
from utils.constants import CUTOFF_COUNT, CUTOFF_IN_MS, RESET_ADV, ELIMINATE_ADV, PLAYERS, IGN_TO_NAME

class PlayerData:
    def __init__(self, uuid):
        self.scores = [0] + [None for _ in range(CUTOFF_COUNT - 1)]

        response = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
        ign = response.json()['name']
        self.name = IGN_TO_NAME.get(ign, ign)

        self.placement = 1 # Defaults, as first place never gets elimintation adv
        self.advancement_dict = {}
        self.resets = 0
    

    def add_advancement(self, timestamp, adv_type):
        elim_num = PLAYERS - self.placement
        timeslot = self._timestamp_to_timeslot(timestamp)
        
        if adv_type == RESET_ADV:
            self.reset(timeslot)
            return
        if adv_type.startswith("projectelo"):
            return
        if timeslot > elim_num:
            return

        if self.scores[timeslot] == None:
            self.scores[timeslot] = self.scores[timeslot - 1]
        
        self.scores[timeslot] += 1
        self.advancement_dict[adv_type] = timestamp
    

    def reset(self, timestamp):
        timeslot = self._timestamp_to_timeslot(timestamp)
        self.scores[timeslot] = 0
        self.resets += 1
    

    def set_placement(self, placement):
        elimination_num = PLAYERS - placement
        if self.scores[elimination_num] is None:
            self.scores[elimination_num] = self.scores[elimination_num - 1]
        self.placement = placement


    def _timestamp_to_timeslot(self, timestamp: int):
        return min(timestamp//CUTOFF_IN_MS, CUTOFF_COUNT - 1)


def parse_timeline(timeline_data) -> dict[str, PlayerData]:
    group_player_data: dict[str, PlayerData] = {}
    elim_count = 0
    for event in timeline_data:
        uuid = event['uuid']
        adv_type = event['type']
        timestamp = event['time']

        if uuid not in group_player_data:
            group_player_data[uuid] = PlayerData(uuid)
        player = group_player_data[uuid]       

        if adv_type == ELIMINATE_ADV:
            player.set_placement(PLAYERS - elim_count)
            elim_count += 1
            continue

        player.add_advancement(timestamp, adv_type)
    return group_player_data
