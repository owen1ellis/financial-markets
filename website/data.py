import pandas as pd

# Load the data into this 
def load_data(file_path):
    return pd.read_csv(file_path)
data = pd.read_csv(file_path)