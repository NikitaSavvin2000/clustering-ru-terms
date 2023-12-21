import pandas as pd  # Fix: Import pandas as pd
import tensorflow_hub as hub
from sklearn.manifold import TSNE
import umap
import matplotlib.pyplot as plt  # Fix: Import matplotlib.pyplot as plt
# %matplotlib inline

# Loading Universal Sentence Encoder
module_url = 'https://tfhub.dev/google/universal-sentence-encoder-large/5'
embed = hub.load(module_url)

# Loading source data
df = pd.read_csv('amazon-fine-food-reviews.gz', nrows=100000, usecols=['Id', 'Score', 'Text'])

embedded_text = embed(df['Text']).numpy()

# Performing t-SNE embedding with the default settings
sne_embedded = TSNE(n_components=2, n_jobs=8, verbose=1).fit_transform(embedded_text)  # Fix: Use embedded_text
emb_df_tsne = pd.DataFrame(sne_embedded, columns=['x', 'y'])  # Fix: Provide column names

# Plotting the t-SNE result
plt.figure(figsize=(10, 8))  # Fix: Set a reasonable figure size
plt.scatter(x=emb_df_tsne['x'], y=emb_df_tsne['y'], c='DarkBlue')
plt.title('t-SNE Embedding')
plt.show()

# Performing UMAP embedding with the default settings
reducer = umap.UMAP(metric='cosine', verbose=True)
umap_embedding = reducer.fit_transform(embedded_text)
emb_df_umap = pd.DataFrame(umap_embedding, columns=['x', 'y'])  # Fix: Provide column names

# Plotting the UMAP result
plt.figure(figsize=(10, 8))  # Fix: Set a reasonable figure size
plt.scatter(x=emb_df_umap['x'], y=emb_df_umap['y'], c='DarkBlue')
plt.title('UMAP Embedding')
plt.show()
