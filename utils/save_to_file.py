import json
import pandas as pd

def save_to_file_json(data, file_path):
    """
    Save the given data to a file in JSON format.
    
    Args:
        data (dict): The data to save.
        file_path (str): The path to the file where the data will be saved.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=False)
    print(f"Data saved to {file_path}")

def save_to_file_csv(data, file_path):
    """
    Save the given data to a file in CSV format.
    
    Args:
        data (dict): The data to save.
        file_path (str): The path to the file where the data will be saved.
    """
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")