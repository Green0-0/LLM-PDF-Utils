import json

import requests

class Sampler:
    temperature : float
    top_p : float
    repetition_penalty : float
    max_tokens : int

    def __init__(self, temperature : float = 0.75, top_p : float = 0.9, repetition_penalty : float = 1.05, max_tokens : int = 4096):
        """
        Initialize a Sampler instance with optional parameters for controlling
        the behavior of text generation.

        Args:
            temperature (float, optional): Controls randomness in predictions. 
                Higher values result in more random completions. Defaults to 1.
            top_p (float, optional): Probability threshold for nucleus sampling.
                Defaults to 0.9.
            max_tokens (int, optional): Maximum number of new tokens to generate.
                Defaults to 512.
        """
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens

class Model:
    url: str # URL of the OpenAI API
    api_key: str # API key for the OpenAI API
    model: str # type of model to use for the completion
    sampler : Sampler
    
    def __init__(self, url : str = None, model : str = None, api_key : str = None, sampler : Sampler = Sampler()):
        """
        Initialize a Model instance with optional parameters for URL, model type, and API key.

        Args:
            url (str, optional): The URL of the OpenAI API. Defaults to None.
            model (str, optional): The type of model to use for completion. Defaults to None.
            api_key (str, optional): The API key for authenticating with the OpenAI API. Defaults to None.
        """
        self.url = url
        self.model = model
        self.api_key = api_key
        self.sampler = sampler

    def get_completion(self, input : str, base64_image = None, image_type : str = "jpeg") -> str:        
        """
        Get the completion of a given chat, automatically parses code when appropriate.

        Args:
            input (str): The text to complete.
            base64_image (str, optional): The base64 encoded image to include. Defaults to None.
            image_type (str, optional): The type of the image. Defaults to "jpeg".

        Returns:
            str: The completion of the chat.
        """
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        message = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": input
                }
            ]
        }
        if base64_image is not None:
            message["content"].append({"type": "image_url", "image_url": f"data:image/{image_type};base64,{base64_image}"})
        data = {
            'model': self.model,
            'messages': [message],
            'stream': False,
            'temperature': self.sampler.temperature,
            'top_p': self.sampler.top_p,
            'max_tokens': self.sampler.max_tokens,
        }
        response = json.loads(requests.post(self.url, headers=headers, json=data).text)
        response = response['choices'][0]['message']['content']
        return response