from preprocess.tokenize import Tokenizer
from preprocess.prepare_dataset import prepare_dataset, split
from trainer.train import train
import pandas as pd

data_path = 'train/data/'
raw_benign_path = data_path + 'raw/benign'
raw_malicious_path = data_path + 'raw/malicious'
benign_token_path = data_path + 'tokens/benign.csv'
malicious_token_path = data_path + 'tokens/malicious.csv'

tokenizer = Tokenizer()
ben_tokens = tokenizer.run(raw_benign_path, benign_token_path)
mal_tokens = tokenizer.run(raw_malicious_path, malicious_token_path)

#ben_tokens = pd.read_csv(benign_token_path)
#mal_tokens = pd.read_csv(malicious_token_path)
ben_tokens['label'] = 'benign'
mal_tokens['label'] = 'malicious'
df = pd.concat([ben_tokens, mal_tokens], ignore_index=True)

input_path = data_path + 'data/tokens.txt'
prepare_dataset(df, input_path)
split(input_path, 0.2, stratify=True)

model = train(
  model_path='train/model1.bin',
  input=data_path+'data/tokens.train',
)

model.test(data_path+'data/tokens.test')