from client import model_api


'''
response:
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [
        0.0023064255,
        -0.009327292,
        .... (1536 floats total for ada-002)
        -0.0028842222,
      ],
      "index": 0
    }
  ],
  "model": "text-embedding-ada-002",
  "usage": {
    "prompt_tokens": 8,
    "total_tokens": 8
  }
}
'''
def create_embedding(text_list):
    embed_model = "text-embedding-ada-002"

    res = model_api.openai.Embedding.create(
        input=text_list,
        engine=embed_model
    )
    return res