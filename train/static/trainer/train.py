import fasttext

def train(
  model_path, input, model_type='cbow', lr=0.05, dim=100, ws=5, epoch=10, 
  minCount=5, minn=3, maxn=6, neg=5, thread=8
):
  model = fasttext.train_supervised(
    input=input,
    #model=model_type,
    lr=lr,
    dim=dim,
    ws=ws,
    epoch=epoch,
    minCount=minCount,
    minn=minn,
    maxn=maxn,
    neg=neg,
    thread=thread
  )
  model.save_model(model_path)
  return model