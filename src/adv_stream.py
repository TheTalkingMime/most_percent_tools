from utils.ranked_api import LiveMatchData
from utils.player_data_parsing import parse_timeline
from utils.sheets import SheetsEditor
from utils.utils import load_yaml
import time

REF_NAME = 'planetvoid' 

refs = load_yaml('credentials/refs.yaml')

uuid = refs[REF_NAME]['uuid']
private_key = refs[REF_NAME]['private_key']

match_data = LiveMatchData(uuid, private_key)
player_names = match_data.player_names
print(player_names)
player_uuids = match_data.player_uuids

sheet_editor = SheetsEditor()

while True:
    timeline_data = match_data.timeline
    if len(timeline_data) == 0:
        print("No timeline data available. Retrying in 10 seconds...")
        time.sleep(10)
        continue
    break
    
sheet_editor.reset_sheet()
sheet_editor.set_player_names(player_names)

while True:
    all_player_completed_advs = []
    
    timeline_data = match_data.timeline
    print(len(timeline_data))
    

    parsed_timeline = parse_timeline(timeline_data)

    for uuid in player_uuids:
        player_data = parsed_timeline.get(uuid)
        completed_advs = list(player_data.advancement_dict.keys())
        all_player_completed_advs.append(list(player_data.advancement_dict.keys()))

    sheet_editor.update_adv_status(all_player_completed_advs)
    time.sleep(10)
    print("Updating sheet..")
    