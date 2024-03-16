import requests
import os
from dotenv import load_dotenv


load_dotenv()


def summarize(text: str, temperature: float=0.9, min_length: int=500, max_length: int=1000) -> str:
    API_URL = "https://api-inference.huggingface.co/models/Falconsai/text_summarization"
    headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"Status Code: {response.status_code} | from hf_falconsai text summarization")
        
    output = query({
        "inputs": text,
        "parameters": {
            "max_length": max_length, 
            "min_length": min_length, 
            "do_sample": True, 
            "temperature": temperature
        },
    })

    return output[0]['summary_text']


if __name__ == "__main__":
    text = "The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct."
    text = "Hello world!"
    print(summarize(text))