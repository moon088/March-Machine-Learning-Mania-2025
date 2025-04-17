import os
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from sklearn.metrics import log_loss,mean_squared_error, mean_absolute_error, roc_auc_score, average_precision_score
from sklearn.calibration import calibration_curve
from sklearn.metrics import root_mean_squared_error

ensemble_list = ["best_feature", "logloss", "spline"]
ensemble_weight = [1, 1, 1]
ensemblenum = 2


years = [2019, 2021, 2022, 2023, 2024]
CURDIR = os.path.dirname(__file__)
INPUT_PATH_BASE = os.path.join(os.path.dirname(CURDIR), "output")
OUTPUT_PATH = os.path.join(os.path.dirname(CURDIR),"output", "ensemble", f"ensemble{ensemblenum}")
os.makedirs(OUTPUT_PATH, exist_ok=True) 


log_file_path = os.path.join(OUTPUT_PATH, "ensemble_log.txt")
with open(log_file_path, "w") as log_file:
    log_file.write("Ensemble Log\n")
    log_file.write("Timestamp: " + str(datetime.datetime.now()) + "\n")
    log_file.write("Ensemble Models and Weights:\n")
    for model, weight in zip(ensemble_list, ensemble_weight):
        log_file.write(f"  {model}: {weight}\n")
    log_file.write("\n")

for year in years:
    print(f"----- Ensemble for {year} -----")
    results = [f"----- Emsemble for {year} -----"]
    
    pred_list = []
    valid_weights = []      
    for model, weight in zip(ensemble_list, ensemble_weight):
        # 例: predictions/feature_engineering_10/2019.csv のように想定
        file_path = os.path.join(INPUT_PATH_BASE, model, f"{model}_{year}.csv")
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        df = pd.read_csv(file_path)

        pred_list.append(df)
        valid_weights.append(weight)
    
    if not pred_list:
        print(f"No valid predictions found for year {year}. Skipping ensemble for this year.")
        continue
    
    total_weight = sum(valid_weights)
    combined_df = pred_list[0][["Season", "T1_TeamID", "T2_TeamID"]].copy()
    ensemble_pred = np.zeros(len(combined_df))
    for df, weight in zip(pred_list, valid_weights):
        ensemble_pred += weight * df["Pred"].values
    ensemble_pred = ensemble_pred / total_weight
    combined_df["Pred"] = ensemble_pred

    output_csv = os.path.join(OUTPUT_PATH, f"ensemble_{year}.csv")
    combined_df.to_csv(output_csv, index=False)
    combined_df["Pred"].astype(int)
    combined_df["Pred"].hist(bins=50)
    plt.figure(figsize=(8, 6))
    combined_df["Pred"].hist(bins=50)
    plt.title("Prediction Histogram")
    plt.xlabel("Pred")
    plt.ylabel("Frequency")
    plt.grid(True)

    plt.savefig(os.path.join(OUTPUT_PATH, f"Prediction_Histgram_filtered_{year}.png"))
    plt.close()
    print(f"Saved ensembled CSV for {year} to {output_csv}")
    

    # cal score
    tourney_file_path = os.path.join(os.path.dirname(CURDIR), "input")
    tourney_results = pd.concat([
    pd.read_csv(os.path.join(tourney_file_path,"MNCAATourneyDetailedResults.csv")),
    pd.read_csv(os.path.join(tourney_file_path,"WNCAATourneyDetailedResults.csv")),
    ], ignore_index=True)
    
 


    def extract_labels_and_preds(sub, tourney):
        """ 試合データから予測値 (Pred) と正解ラベル (label) を抽出する """
        label_data = tourney[["Season", "WTeamID", "LTeamID", "WScore", "LScore"]]
        label_data = label_data.rename(columns={"WTeamID": "T1_TeamID", "LTeamID": "T2_TeamID", "WScore": "T1_Score", "LScore": "T2_Score"})
        temp = label_data.copy()
        temp = temp.rename(columns={"T1_TeamID": "T2_TeamID", "T2_TeamID": "T1_TeamID", "T1_Score": "T2_Score", "T2_Score": "T1_Score"})
        label_data = pd.concat([label_data, temp]).reset_index(drop=True)
        
        label_data = pd.merge(label_data, sub, on=["Season", "T1_TeamID", "T2_TeamID"], how="right")
        label_data["label"] = np.where(label_data["T1_Score"] - label_data["T2_Score"] > 0, 1, 0)
        label_data = label_data.dropna(subset=["Pred"])  # 欠損値を削除
        return label_data[["label", "Pred"]]

    def calculate_metrics(label_data):
        print(label_data.info())
        """ 各評価指標を計算 """
        brier_score = round(mean_squared_error(label_data["label"], label_data["Pred"]), 5)  # Brier Score (MSEと同じ)
        rmse = round(root_mean_squared_error(label_data["label"], label_data["Pred"]), 5)  # RMSE
        logloss_score = round(log_loss(label_data["label"], label_data["Pred"]), 5)  # Log Loss
        mae_score = round(mean_absolute_error(label_data["label"], label_data["Pred"]), 5)  # MAE
        
        return {
            "Brier Score": brier_score,
            "RMSE": rmse,
            "Log Loss": logloss_score,
            "MAE": mae_score
        }

    def plot_calibration_curve(label_data, n_bins=10):
        """ キャリブレーションカーブをプロット """
        prob_true, prob_pred = calibration_curve(label_data["label"], label_data["Pred"], n_bins=n_bins)
        
        plt.figure(figsize=(6,6))
        plt.plot(prob_pred, prob_true, marker="o", label="Model Calibration")
        plt.plot([0, 1], [0, 1], linestyle="--", label="Perfect Calibration")
        plt.xlabel("Predicted Probability")
        plt.ylabel("Actual Probability")
        plt.legend()
        plt.title("Calibration Curve")

    def calculate_auc_metrics(label_data):
        global results
        """ AUC-ROCとAUC-PRを計算 """
        auc_roc = roc_auc_score(label_data["label"], label_data["Pred"])
        auc_pr = average_precision_score(label_data["label"], label_data["Pred"])
        
        results += ["---- AUC -----", f"AUC-ROC: {auc_roc:.4f}", f"AUC-PR: {auc_pr:.4f}", ""]
        

    label_data = extract_labels_and_preds(combined_df, tourney_results)
    score = calculate_metrics(label_data)
    results += ["-----eval metrics-----",
                f"Brier Score: {score['Brier Score']}", 
                f"RMSE: {score['RMSE']}", 
                f"Log Loss: {score['Log Loss']}", 
                f"MAE: {score['MAE']}", ""]

    # キャリブレーションの確認
    plot_calibration_curve(label_data)
    # AUCの評価
    calculate_auc_metrics(label_data)



    with open(log_file_path, "a", encoding="utf-8") as f:
        for line in results:
            f.write(line + "\n")
