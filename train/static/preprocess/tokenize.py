import esprima
import pandas as pd
import os
from tqdm import tqdm
from glob import glob

class Tokenizer:
  def __init__(self, parse_depth='Type'):
    self.__set_parse_depth(parse_depth=parse_depth)
    
  def __set_parse_depth(self, parse_depth):
    self.type = True if 'Type' in parse_depth else False
    self.id = True if 'ID' in parse_depth else False
    self.literal = True if 'Literal' in parse_depth else False

  def __tokenize(self, script):
    try:
      ast = esprima.parseScript(script)
      return ast
    except:
      try:
        ast = esprima.parseModule(script)
        return ast
      except:
        return None

  def __dfs(self, ast):
    stack = [ast]
    tokens = []

    while stack:
      node = stack.pop()

      if self.id and isinstance(node, esprima.nodes.Identifier):
        tokens.append(node.name)
      elif self.literal and isinstance(node, esprima.nodes.Literal):
        tokens.append(str(node.value))
      elif self.type and isinstance(node, esprima.nodes.Node):
        if hasattr(node, 'type'):
          tokens.append(node.type)

        for _, value in reversed(list(vars(node).items())):
          if isinstance(value, list):
            for item in reversed(value):
              if isinstance(item, esprima.nodes.Node):
                stack.append(item)
          elif isinstance(value, esprima.nodes.Node):
            stack.append(value)

    return tokens
  
  def __read(self, fp):
    for encoding in ['utf-8', 'utf-16']:
      try:
        with open(fp, 'r', encoding=encoding) as f:
          return f.read()
      except (UnicodeDecodeError, FileNotFoundError):
        continue
    return None
  
  def run(self, src_path, dst_path=None, parse_depth=None):
    
    if parse_depth:
      self.__set_parse_depth(parse_depth=parse_depth)
      
    tokenized = []
    files = [f for f in glob(os.path.join(src_path, '**', '*'), recursive=True) if os.path.isfile(f)]
    for file in tqdm(files, desc="Tokenizing.. "):
      script = self.__read(file)
      if script:
        ast = self.__tokenize(script)
        if ast:
          tokens = self.__dfs(ast)
          if tokens:
            tokenized.append(' '.join(tokens))
    df = pd.DataFrame(tokenized, columns=['Tokens'])
    
    if dst_path:
      df.to_csv(dst_path, index=False, encoding='utf-8', escapechar='\\', errors='ignore')
    
    return df