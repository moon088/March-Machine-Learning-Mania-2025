#2022MAN 提出形式に変換
import os 
import pandas as pd
import numpy as np

#この二つ変える
dir = "[2022, 2023, 2024]_best_param"
filename = "2022_best_param.csv"

CURRENT_DIR = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(os.path.dirname(CURRENT_DIR),"output", dir, filename))
sample_sub = pd.read_csv(os.path.join(os.path.dirname(CURRENT_DIR), "input", "SampleSubmission2022M.csv"))
temp = df.copy()
temp = temp.rename(columns={"T1_TeamID": "T2_TeamID", "T2_TeamID": "T1_TeamID"})
df = pd.concat([df, temp]).reset_index()


sub = sample_sub.copy()
sub['Season'] = sub['ID'].apply(lambda x: int(x.split('_')[0]))
sub["T1_TeamID"] = sub['ID'].apply(lambda x: int(x.split('_')[1]))
sub["T2_TeamID"] = sub['ID'].apply(lambda x: int(x.split('_')[2]))
sub = pd.merge(sub, df, on=["Season", "T1_TeamID", "T2_TeamID"], how="left")
#print(sub.head())
print(len(sub["Pred_y"].unique()))

fin = sub[["ID", "Pred_y"]]
#fin.info() #67でOK
fin = fin.rename(columns={"Pred_y": "Pred"})
fin["Pred"] = fin["Pred"].fillna(100000)
fin.to_csv(os.path.join(os.path.dirname(CURRENT_DIR), "make_csv", filename), index=None)