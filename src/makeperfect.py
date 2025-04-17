#2022MANの完璧なファイル生成
import os 
import pandas as pd
import numpy as np

#この二つ変える
filename = "perfect.csv"

CURRENT_DIR = os.path.dirname(__file__)
sample_sub = pd.read_csv(os.path.join(os.path.dirname(CURRENT_DIR), "input", "SampleSubmission2022M.csv"))
tourney_man = pd.read_csv(os.path.join(os.path.dirname(CURRENT_DIR), "input", "MNCAATourneyDetailedResults.csv"))
tourney_man = tourney_man[tourney_man["Season"]==2022]

temp = tourney_man.copy()
temp = temp.rename(columns={"WTeamID": "LTeamID", "LTeamID": "WTeamID", "WScore": "LScore", "LScore": "WScore"})
tourney_man = pd.concat([tourney_man, temp]).reset_index()
tourney_man = tourney_man.rename(columns={"WTeam_ID": "T1_TeamID", "LTeamID": "T2_TeamID"})
tourney_man["win"] = np.where(tourney_man["WScore"]-tourney_man["LScore"]>0, 1, 0)
tourney_man = tourney_man.rename(columns={"WTeamID": "T1_TeamID", "LTeamID": "T2_TeamID"})
print(tourney_man.head())
print(tourney_man.tail())

sub = sample_sub.copy()
sub['Season'] = sub['ID'].apply(lambda x: int(x.split('_')[0]))
sub["T1_TeamID"] = sub['ID'].apply(lambda x: int(x.split('_')[1]))
sub["T2_TeamID"] = sub['ID'].apply(lambda x: int(x.split('_')[2]))
sub = pd.merge(sub, tourney_man, on=["Season", "T1_TeamID", "T2_TeamID"], how="left")


fin = sub[["ID", "win"]]
fin = fin.rename(columns={"win": "Pred"})
print(fin.info())
#fin["Pred"] = fin["Pred"].fillna(1000000000)
fin.to_csv(os.path.join(os.path.dirname(CURRENT_DIR), "make_csv", filename), index=None)