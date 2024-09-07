import pandas as pd
import os
from sklearn.model_selection import train_test_split

def prepare_dataset(df: pd.DataFrame, file_path, column='Tokens', label='label'):
  prefix = '__label__'
  lines = [f"{prefix}{str(row[label])} {str(row[column])}\n" for _, row in df.iterrows()]
  
  with open(file_path, "w", encoding='utf-8') as f:
    f.writelines(lines)

def split(file_path, frac, stratify=None):
  
  with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
  
  data = pd.DataFrame(lines, columns=['text'])
  
  if stratify:
    data['label'] = data['text'].apply(lambda x: x.split()[0].replace('__label__', ''))
    train, test = train_test_split(data, test_size=frac, stratify=data['label'], shuffle=True)
  else:
    train, test = train_test_split(data, test_size=frac, shuffle=True)
  
  fn = os.path.splitext(file_path)[0]
  with open(f"{fn}.train", "w", encoding='utf-8') as f_train:
    f_train.writelines(train['text'].to_list())
  with open(f"{fn}.test", "w", encoding='utf-8') as f_test:
    f_test.writelines(test['text'].to_list())
