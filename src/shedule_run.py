import papermill as pm
import time
import os
from datetime import datetime


experiment_list = [ "spline"]
years = [ 2021, 2022, 2023, 2024, 2025]
NOTEBOOK_PATH = os.path.join(os.path.dirname(__file__), "1stplace_solution_2023.ipynb")
print(NOTEBOOK_PATH)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR) 

for exp in experiment_list:
    for year in years: 
        print(f"----- start {exp} {year} -----")
        start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        exp = f"{exp}"
        print(f"Starting experiment: {exp}")
        pm.execute_notebook(
            NOTEBOOK_PATH,      
            f"{exp}_{start_time}.ipynb",  
            parameters={'EXP_NUM': exp, 'PREDICT_YEAR': year}
            
        )
        print(f"Finished experiment: {exp}")
        time.sleep(60)  
