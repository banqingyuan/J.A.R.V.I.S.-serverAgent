import pinecone
import os


key = os.environ.get("pinecone_app_key", "")
if key == "":
    raise Exception('pinecone_app_key not config')
else:
    pinecone.init(
        api_key=key,
        environment="us-west1-gcp"
    )