from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def loadSentencesFromFile(file_path = 'data.txt'):
  with open(file_path, 'r', encoding='utf-8') as file:
    sentences = [line.strip() for line in file]
  return   sentences

def getEmbeddingsAsDictionary(sentences):

  model = SentenceTransformer("all-MiniLM-L6-v2")
  print(model)  
  # Sentences are encoded by calling model.encode()
  embeddings = model.encode(sentences)
  result=dict()
  #This line assigns the current embedding to a key in the result dictionary. The key is the current sentence from the iteration. Essentially, this line is building or updating a dictionary where each key is a sentence from sentences and its value is the corresponding embedding from embeddings.
  for sentence, embedding in zip(sentences, embeddings):
    result[sentence]=embedding
  return result  

def compare(result):
  comparison_results = []
  for i in range(len(sentences)):
    embedding_1=result.get(sentences[i])
    for  j in range(i+1,len(sentences)):
          embedding_2=result.get(sentences[j])
          sim=cosine_similarity(embedding_1.reshape(1, -1),embedding_2.reshape(1, -1))
          sim=sim[0][0]
          #print(f"similarity between \'{sentences[i]}\' and \'{sentences[j]}\' is {sim:.2f}")
          comparison_results.append({'sentence_1': sentences[i], 'sentence_2': sentences[j], 'similarity': sim})
    df = pd.DataFrame(comparison_results)
    df = df.sort_values(by='similarity', ascending=False)

  return df    

sentences=loadSentencesFromFile()
print("[INFO] Sentences loaded")
print(sentences)
result=getEmbeddingsAsDictionary(sentences)
print("[INFO] Embeddings calculated")
df=compare(result)
print("[INFO] Comparison done")
print(df.head())
