from client import model_api
from client.model_api import object


def completion(prompt):
    # now query text-davinci-003 WITHOUT context
    res = model_api.openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=0,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    return res['choices'][0]['text'].strip()


def chat(msg) -> object.ChatResponse:
    resp = model_api.openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-4",
        messages=msg
    )
    return object.ChatResponse(resp)

