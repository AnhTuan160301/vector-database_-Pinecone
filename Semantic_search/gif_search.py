import dotenv
import pandas as pd
import os
from pinecone import Pinecone
import logging
from pinecone import ServerlessSpec
import time

dotenv.load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD")
PINECONE_REGION = os.getenv("PINECONE_REGION")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
LOGGER = logging.getLogger(__name__)

LOGGER.info("Load The dataset")
df = None
try:

    df = pd.read_csv(
        "data/tgif-v1.0.tsv",
        delimiter="\t",
        names=['url', 'description']
    )

except:
    logging.error("Cannot Load the dataset")
print(df)
pc = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_REGION)
index_name = 'gif-search'

LOGGER.info("Create the index for pinecone")
# check if index already exists (it shouldn't if this is first time)
try:
    if index_name not in pc.list_indexes().names():
        # if does not exist, create index
        pc.create_index(
            index_name,
            dimension=384,
            metric='cosine',
            spec=spec
        )
    # wait for index to be initialized
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)
except:
    logging.error("Cannot Create the index")

index = pc.Index(index_name)

from sentence_transformers import SentenceTransformer
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
retriever = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
retriever.to(device)

from tqdm.auto import tqdm

batch_size = 64

for i in tqdm(range(0, len(df), batch_size)):
    # find end of batch
    i_end = min(i + batch_size, len(df))
    # extract batch
    batch = df.iloc[i:i_end]
    # generate embeddings for batch
    emb = retriever.encode(batch['description'].tolist()).tolist()
    # get metadata
    meta = batch.to_dict(orient='records')
    # create IDs
    ids = [f"{idx}" for idx in range(i, i_end)]
    # add all to upsert list
    to_upsert = list(zip(ids, emb, meta))
    # upsert/insert these records to pinecone
    _ = index.upsert(vectors=to_upsert)

print(index.describe_index_stats())
