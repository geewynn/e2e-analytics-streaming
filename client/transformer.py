import numpy as np
import pandas as pd


df = pd.read_csv('data.csv', encoding='unicode_escape')

df['json'] = df.to_json(orient='records', lines=True).splitlines()

dfjson = df['json']
np.savetxt(r'./output.txt', dfjson.values, fmt='%s')
