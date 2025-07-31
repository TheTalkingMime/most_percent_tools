import gspread
from utils.utils import load_yaml
from utils.constants import PLAYERS

class SheetsEditor:
    def __init__(self):
        config = load_yaml("data/sheets_info.yaml")

        gc = gspread.service_account(
            filename=config.get("credentials-path")
            )
        self.conn = gc.open_by_url(config.get("spreadsheet-url"))
        self.data_sheet = self.conn.worksheet("Live Game")
        self.sorted_sheet = self.conn.worksheet("Live Game Sorted")

        self.first_player_col = config.get("sheet-info").get("first_player_col")
        self.last_player_col = config.get("sheet-info").get("last_player_col")

        self.adv_to_row = self._get_adv_to_row_mapping()

    def _get_adv_to_row_mapping(self):
        adv_to_row = {}
        for i, adv in enumerate(self.conn.worksheet("Live Game").get_values("A:A")):
            adv_name = adv[0]
            adv_to_row[adv_name] = (i + 1)
        return adv_to_row

    def reset_sheet(self):
        values = [["FALSE"] * PLAYERS for _ in range(self.data_sheet.row_count - 2)]

        print(len(values))

        self.data_sheet.batch_update([{
            "range": f"{self.first_player_col}3:{self.last_player_col}{self.data_sheet.row_count}",
            "values": values
        }], value_input_option='USER_ENTERED')

        self.data_sheet.batch_update([{
            "range": f"{self.first_player_col}1:{self.last_player_col}1",
            "values": [[None] * PLAYERS]
        }])

    def set_player_names(self, player_names:list[str]):
        # assert len(player_names) == PLAYERS, f"There should be exactly {PLAYERS} player names."
        player_names_range = f"{self.first_player_col}1:{self.last_player_col}1"
        self.data_sheet.update(range_name=player_names_range, values=[player_names])
        self.sorted_sheet.update(range_name=player_names_range, values=[player_names])

    
    def update_adv_status(self, completed_advs:list[list[str]]):
        # assert len(completed_advs) == PLAYERS, f"There should be exactly {PLAYERS} lists of advancements."
        batch_updates = []
        for column_idx, player_advs in enumerate(completed_advs):
            player_col = chr(ord(self.first_player_col) + column_idx)
            for adv in player_advs:
                if adv not in self.adv_to_row:
                    raise ValueError(f"Advancement {adv} not found in the sheet.")
                row = self.adv_to_row[adv]
                batch_updates.append({
                    "range": f"{player_col}{row}",
                    "values": [["TRUE"]]
                })
        self.data_sheet.batch_update(batch_updates, value_input_option='USER_ENTERED')
        return
                           
    def full_refresh(self, completed_advs:list[list[str]], player_names:list[str]):
        self.reset_sheet()
        self.set_player_names(player_names)
        self.update_adv_status(completed_advs)
