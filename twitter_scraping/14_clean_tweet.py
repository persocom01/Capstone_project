import pandas as pd
import sys
import io
import json
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

import_path = r'.\data\#michellewilliams.csv'
data = pd.read_csv(import_path, low_memory=False)
print(data.isnull().sum())
df = data[['id_str', 'full_text', ]]
print(df.head())
