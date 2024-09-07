from url_model import detector
import os
import pprint
import time

start = time.time()

model_path = 'url_model/model'
detector = detector.URLDetector(model_path=model_path)

end_model_load = time.time()

data_path = 'test/url/data'
files = os.listdir(data_path)
urls= []
for file in files:
  with open(os.path.join(data_path, file), 'r', encoding='utf-8') as f:
    url = f.read()
    urls.append(url)
    
end_data_load = time.time()

preds = detector.predict(urls)
pprint.pprint(preds)

end_prediction = time.time()

print(f"load model: {end_model_load-start}")
print(f"load data: {end_data_load-end_model_load}")
print(f"predict: {end_prediction-end_data_load}")