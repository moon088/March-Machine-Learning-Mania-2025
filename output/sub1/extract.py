import pandas as pd
from itertools import combinations
import os 
CUR = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(CUR, "sub1_2025.csv"))

man_seed = [
    1120, 1106,
    1257, 1166,
    1276, 1471,
    1401, 1463,
    1279, 1314,
    1235, 1252,
    1266, 1307,
    1277, 1136,
    1196, 1313,
    1163, 1328,
    1272, 1161,
    1268, 1213,
    1281, 1179,
    1403, 1423,
    1242, 1116,
    1385, 1303,
    1181, 1291,
    1280, 1124,
    1332, 1251,
    1112, 1103,
    1140, 1433,
    1458, 1285,
    1388, 1435,
    1104, 1352,
    1222, 1188,
    1211, 1208,
    1155, 1270,
    1345, 1219,
    1228, 1400, 1462, 
    1246, 1407,
    1417, 1429,
    1397, 1459,
]
woman_seed= [
    3417, 3380,
    3350, 3210,
    3279, 3123,
    3124, 3213,
    3199, 3206,
    3261, 3361,
    3277, 3217,
    3301, 3436,
    3425, 3422,
    3143, 3280,
    3243, 3193,
    3246, 3251,
    3234, 3293,
    3228, 3195,
    3329, 3355,
    3163, 3117,
    3400, 3219, 3456,  # "/"があったため個別の要素に
    3228, 3166,
    3397, 3378,
    3326, 3286,
    3276, 3235,
    3323, 3372,
    3257, 3304,
    3395, 3192,
    3376, 3399,
    3428, 3231,
    3104, 3453,
    3268, 3313,
    3452, 3162, 3449,  # "/"があったため個別の要素に
    3314, 3333,
    3435, 3332,
    3181, 3250,
]


man_combinations = [f"2025_{min(m1, m2)}_{max(m1, m2)}" for m1, m2 in combinations(man_seed, 2)]
woman_combinations = [f"2025_{min(w1, w2)}_{max(w1, w2)}" for w1, w2 in combinations(woman_seed, 2)]
team_combinations = man_combinations + woman_combinations

filtered_df = df[df['ID'].isin(team_combinations)]

# 結果をCSVに保存
filtered_df.to_csv("filtered_teams.csv", index=False)

print("抽出したデータを 'filtered_teams.csv' に保存しました。")
