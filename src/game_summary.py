from utils.ranked_api import PostMatchData
from utils.player_data_parsing import parse_timeline
from utils.constants import PLAYERS 

match_id = 2642228

match_data = PostMatchData(match_id)

parsed_timeline = parse_timeline(match_data.timeline)

output = [None for _ in range(PLAYERS)]
for player in parsed_timeline.values():
    print(player.name)
for player in parsed_timeline.values():
    output_data = [player.name]
    for score in player.scores:
        output_data.append(str(score) if score is not None else "")
    output_data.append(str(player.placement))
    output[player.placement - 1] = ",".join(output_data)

for line in output:
    print(line)