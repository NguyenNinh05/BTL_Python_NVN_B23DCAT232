class Player:
    def __init__(self, name, nation, position, team, age):
        self.name = name
        self.nation = nation
        self.team = team
        self.position = position
        self.age = age
        self.playing_time = {
            "matches_played": "N/a",
            "starts": "N/a",
            "minutes": "N/a"
        }
        self.performance = {
            "goals": "N/a",
            "assists": "N/a",
            "yellow_cards": "N/a",
            "red_cards": "N/a"
        }
        self.expected = {
            "xG": "N/a",
            "xAG": "N/a"
        }
        self.progression = {
            "PrgC": "N/a",
            "PrgP": "N/a",
            "PrgR": "N/a"
        }
        self.per_90 = {
            "Gls": "N/a",
            "Ast": "N/a",
            "xG": "N/a",
            "xAG": "N/a",
        }
        self.goalkeeping = {
            "Performance": {
                "GA90": "N/a",
                "Save%": "N/a",
                "CS%": "N/a"
            },
            "Penalty Kicks": {
                "Save%": "N/a"
            }
        }
        self.shooting = {
            "SoT%": "N/a",
            "SoT/90": "N/a",
            "G/Sh": "N/a",
            "Dist": "N/a",
        }
        self.passing = {
            "Total": {
                "Cmp": "N/a",
                "Cmp%": "N/a",
                "TotDist": "N/a",
            },
            "Short": {
                "Cmp%": "N/a"
            },
            "Medium": {
                "Cmp%": "N/a"
            },
            "Long": {
                "Cmp%": "N/a"
            },
            "Expected": {
                "KP": "N/a",
                "1/3": "N/a",
                "PPA": "N/a",
                "CrsPA": "N/a",
                "PrgP": "N/a"
            }
        }
        self.goal_shot_creation = {
            "SCA": {
                "SCA": "N/a",
                "SCA90": "N/a"
            },
            "GCA": {
                "GCA": "N/a",
                "GCA90": "N/a"
            },
        }
        self.defensive_actions = {
            "Tackles": {
                "Tkl": "N/a",
                "TklW": "N/a",
            },
            "Challenges": {
                "Att": "N/a",
                "Lost": "N/a"
            },
            "Blocks": {
                "Blocks": "N/a",
                "Sh": "N/a",
                "Pass": "N/a",
                "Int": "N/a",
            }
        }
        self.possession = {
            "Touches": {
                "Touches": "N/a",
                "Def Pen": "N/a",
                "Def 3rd": "N/a",
                "Mid 3rd": "N/a",
                "Att 3rd": "N/a",
                "Att Pen": "N/a",
            },
            "Take-Ons": {
                "Att": "N/a",
                "Succ%": "N/a",
                "Tkld%": "N/a"
            },
            "Carries": {
                "Carries": "N/a",
                "ProDist": "N/a",
                "ProgC": "N/a",
                "1/3": "N/a",
                "CPA": "N/a",
                "Mis": "N/a",
                "Dis": "N/a"
            },
            "Receiving": {
                "Rec": "N/a",
                "PrgR": "N/a"
            }
        }
        self.misc_stats = {
            "Performance": {
                "Fls": "N/a",
                "Fld": "N/a",
                "Off": "N/a",
                "Crs": "N/a",
                "OG": "N/a",
                "Recov": "N/a"
            },
            "Aerial Duels": {
                "Won": "N/a",
                "Lost": "N/a",
                "Won%": "N/a"
            }
        }

    def setPlaying_time(self, arr):
        self.playing_time["matches_played"] = arr[0]
        self.playing_time["starts"] = arr[1]
        self.playing_time["minutes"] = arr[2]

    def setPerformance(self, arr):
        self.performance["goals"] = arr[0]
        self.performance["assists"] = arr[2]
        self.performance["yellow_cards"] = arr[3]
        self.performance["red_cards"] = arr[4]

    def setExpected(self, arr):
        self.expected["xG"] = arr[0]
        self.expected["xAG"] = arr[2]

    def setProgression(self, arr):
        self.progression["PrgC"] = arr[0]
        self.progression["PrgP"] = arr[1]
        self.progression["PrgR"] = arr[2]

    def setPer90(self, arr):
        self.per_90["Gls"] = arr[0]
        self.per_90["Ast"] = arr[1]
        self.per_90["xG"] = arr[5]
        self.per_90["xAG"] = arr[6]

    def setGoalkeeping(self, performance_arr, penalty_arr):
        self.goalkeeping["Performance"]["GA90"] = performance_arr[1]
        self.goalkeeping["Performance"]["Save%"] = performance_arr[4]
        self.goalkeeping["Performance"]["CS%"] = performance_arr[9]
        self.goalkeeping["Penalty Kicks"]["Save%"] = penalty_arr[4]

    def setShooting(self, arr):
        self.shooting["SoT%"] = arr[3]
        self.shooting["SoT/90"] = arr[5]
        self.shooting["G/Sh"] = arr[6]
        self.shooting["Dist"] = arr[8]

    def setPassing(self, total_arr, short_arr, medium_arr, long_arr, expected_arr):
        self.passing["Total"]["Cmp"] = total_arr[0]
        self.passing["Total"]["Cmp%"] = total_arr[2]
        self.passing["Total"]["TotDist"] = total_arr[3]
        self.passing["Short"]["Cmp%"] = short_arr[2]
        self.passing["Medium"]["Cmp%"] = medium_arr[2]
        self.passing["Long"]["Cmp%"] = long_arr[2]
        self.passing["Expected"]["KP"] = expected_arr[4]
        self.passing["Expected"]["1/3"] = expected_arr[5]
        self.passing["Expected"]["PPA"] = expected_arr[6]
        self.passing["Expected"]["CrsPA"] = expected_arr[7]
        self.passing["Expected"]["PrgP"] = expected_arr[8]

    def setGoalShotCreation(self, sca_arr, gca_arr):
        self.goal_shot_creation["SCA"]["SCA"] = sca_arr[0]
        self.goal_shot_creation["SCA"]["SCA90"] = sca_arr[1]
        self.goal_shot_creation["GCA"]["GCA"] = gca_arr[0]
        self.goal_shot_creation["GCA"]["GCA90"] = gca_arr[1]

    def setDefensiveActions(self, tackles_arr, challenges_arr, blocks_arr):
        self.defensive_actions["Tackles"]["Tkl"] = tackles_arr[0]
        self.defensive_actions["Tackles"]["TklW"] = tackles_arr[1]
        self.defensive_actions["Challenges"]["Att"] = challenges_arr[1]
        self.defensive_actions["Challenges"]["Lost"] = challenges_arr[3]
        self.defensive_actions["Blocks"]["Blocks"] = blocks_arr[0]
        self.defensive_actions["Blocks"]["Sh"] = blocks_arr[1]
        self.defensive_actions["Blocks"]["Pass"] = blocks_arr[2]
        self.defensive_actions["Blocks"]["Int"] = blocks_arr[3]

    def setPossession(self, touches_arr, take_ons_arr, carries_arr, receiving_arr):
        self.possession["Touches"]["Touches"] = touches_arr[0]
        self.possession["Touches"]["Def Pen"] = touches_arr[1]
        self.possession["Touches"]["Def 3rd"] = touches_arr[2]
        self.possession["Touches"]["Mid 3rd"] = touches_arr[3]
        self.possession["Touches"]["Att 3rd"] = touches_arr[4]
        self.possession["Touches"]["Att Pen"] = touches_arr[5]
        self.possession["Take-Ons"]["Att"] = take_ons_arr[0]
        self.possession["Take-Ons"]["Succ%"] = take_ons_arr[2]
        self.possession["Take-Ons"]["Tkld%"] = take_ons_arr[4]
        self.possession["Carries"]["Carries"] = carries_arr[0]
        self.possession["Carries"]["ProDist"] = carries_arr[2]
        self.possession["Carries"]["ProgC"] = carries_arr[3]
        self.possession["Carries"]["1/3"] = carries_arr[4]
        self.possession["Carries"]["CPA"] = carries_arr[5]
        self.possession["Carries"]["Mis"] = carries_arr[6]
        self.possession["Carries"]["Dis"] = carries_arr[7]
        self.possession["Receiving"]["Rec"] = receiving_arr[0]
        self.possession["Receiving"]["PrgR"] = receiving_arr[1]

    def setMiscStats(self, performance_arr, aerial_duels_arr):
        self.misc_stats["Performance"]["Fls"] = performance_arr[0]
        self.misc_stats["Performance"]["Fld"] = performance_arr[1]
        self.misc_stats["Performance"]["Off"] = performance_arr[2]
        self.misc_stats["Performance"]["Crs"] = performance_arr[3]
        self.misc_stats["Performance"]["OG"] = performance_arr[4]
        self.misc_stats["Performance"]["Recov"] = performance_arr[5]
        self.misc_stats["Aerial Duels"]["Won"] = aerial_duels_arr[0]
        self.misc_stats["Aerial Duels"]["Lost"] = aerial_duels_arr[1]
        self.misc_stats["Aerial Duels"]["Won%"] = aerial_duels_arr[2]

    def __str__(self) -> str:
        return self.name + " " + str(self.age) + " " + self.team + "\n" + str(self.performance) + \
            "\n" + str(self.per_90) + \
            "\n" + str(self.goalkeeping) + \
            "\n" + str(self.shooting)

class Player_Manager:
    def __init__(self) -> None:
        self.list_player = []

    def add(self, player):
        self.list_player.append(player)

    def find(self, name, team):
        for i in self.list_player:
            if i.name == name and i.team == team:
                return i
        return None

    def filtering(self):
        self.list_player = list(filter(lambda p: p.playing_time["minutes"] > 90, self.list_player))

    def show(self):
        for i in self.list_player:
            print(i)

    def sort(self):
        self.list_player = sorted(self.list_player, key=lambda x: (x.name.split()[-1], -x.age))

header_player = [
    "name", "nation", "team", "position", "age",
    "matches_played", "starts", "minutes",
    "goals", "assists", "yellow_cards", "red_cards",
    "xG", "xAG",
    "GA90", "Save%", "CS%", "PK_Save%",
    "PrgC", "PrgP", "PrgR",
    "per90_Gls", "per90_Ast", "per90_xG", "per90_xAG",
    "SoT%", "SoT/90", "G/Sh", "Dist",
    "Pass_Cmp", "Pass_Cmp%", "TotDist",
    "Short_Cmp%", "Medium_Cmp%", "Long_Cmp%", 
    "KP", "1/3", "PPA", "CrsPA", "PrgP",
    "SCA", "SCA90", "GCA", "GCA90",
    "Tkl", "TklW", "Challenges_Att", "Challenges_Lost",
    "Blocks", "Blocks_SH", "Blocks_Pass", "Blocks_Int",
    "Touches", "Def_Pen", "Def_3rd", "Mid_3rd", "Att_3rd", "Att_Pen",
    "Take_Att", "Take_Succ%", "Take_Tkld%",
    "Carries", "Carries_ProDist", "Carries_ProgC", "Carries_1/3", "Carries_CPA", "Carries_Mis", "Carries_Dis",
    "REC", "REC_PrgR",
    "Fls", "Fld", "Off", "Crs", "OG", "Recov", "Aerial_Won", "Aerial_Lost", "Aerial_Won%"
]

def row_player(player):
    return [
        player.name, player.nation, player.team, player.position, player.age,
        player.playing_time["matches_played"], player.playing_time["starts"], player.playing_time["minutes"],
        player.performance["goals"], player.performance["assists"], player.performance["yellow_cards"], player.performance["red_cards"],
        player.expected["xG"], player.expected["xAG"],
        player.goalkeeping["Performance"]["GA90"], 
        player.goalkeeping["Performance"]["Save%"], 
        player.goalkeeping["Performance"]["CS%"],
        player.goalkeeping["Penalty Kicks"]["Save%"],
        player.progression["PrgC"], player.progression["PrgP"], player.progression["PrgR"],
        player.per_90["Gls"], player.per_90["Ast"], player.per_90["xG"], player.per_90["xAG"],
        player.shooting["SoT%"], player.shooting["SoT/90"], player.shooting["G/Sh"], player.shooting["Dist"],
        player.passing["Total"]["Cmp"], player.passing["Total"]["Cmp%"], player.passing["Total"]["TotDist"],
        player.passing["Short"]["Cmp%"], player.passing["Medium"]["Cmp%"], player.passing["Long"]["Cmp%"],
        player.passing["Expected"]["KP"], player.passing["Expected"]["1/3"], player.passing["Expected"]["PPA"], 
        player.passing["Expected"]["CrsPA"], player.passing["Expected"]["PrgP"],
        player.goal_shot_creation["SCA"]["SCA"],  player.goal_shot_creation["SCA"]["SCA90"],  player.goal_shot_creation["GCA"]["GCA"],  player.goal_shot_creation["GCA"]["GCA90"], 
        player.defensive_actions["Tackles"]["Tkl"], player.defensive_actions["Tackles"]["TklW"], 
        player.defensive_actions["Challenges"]["Att"], player.defensive_actions["Challenges"]["Lost"],
        player.defensive_actions["Blocks"]["Blocks"], player.defensive_actions["Blocks"]["Sh"], 
        player.defensive_actions["Blocks"]["Pass"], player.defensive_actions["Blocks"]["Int"],
        player.possession["Touches"]["Touches"], player.possession["Touches"]["Def Pen"], 
        player.possession["Touches"]["Def 3rd"], player.possession["Touches"]["Mid 3rd"], 
        player.possession["Touches"]["Att 3rd"], player.possession["Touches"]["Att Pen"],
        player.possession["Take-Ons"]["Att"], player.possession["Take-Ons"]["Succ%"], 
        player.possession["Take-Ons"]["Tkld%"],
        player.possession["Carries"]["Carries"], player.possession["Carries"]["ProDist"], 
        player.possession["Carries"]["ProgC"], player.possession["Carries"]["1/3"], 
        player.possession["Carries"]["CPA"], player.possession["Carries"]["Mis"], 
        player.possession["Carries"]["Dis"],
        player.possession["Receiving"]["Rec"], player.possession["Receiving"]["PrgR"],
        player.misc_stats["Performance"]["Fls"], player.misc_stats["Performance"]["Fld"], 
        player.misc_stats["Performance"]["Off"], player.misc_stats["Performance"]["Crs"], 
        player.misc_stats["Performance"]["OG"], player.misc_stats["Performance"]["Recov"],
        player.misc_stats["Aerial Duels"]["Won"], player.misc_stats["Aerial Duels"]["Lost"], 
        player.misc_stats["Aerial Duels"]["Won%"]
    ]