import json
from pprint import pprint

import boto3


class BedrockService():

    def __init__(self) -> None:
        self.__bedrock_runtime = boto3.client('bedrock-runtime', region_name='eu-central-1')
        print('\nAI initiated\n')

    def invoke_model(self, prompt):
        response = self.__bedrock_runtime.invoke_model(**{
            "modelId": "anthropic.claude-3-haiku-20240307-v1:0",
            "contentType": "application/json",
            "accept": "application/json",
            "body": json.dumps({
                "anthropic_version": "bedrock-2023-05-31" ,
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            # { # optional
                            #     "type": "image",
                            #     "source": {
                            #         "type": "base64" ,
                            #         "media_type": "image/jpeg",
                            #         "data": encoded_string
                            #     },
                            # },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        
                        ]
                    }
                ]
            })
        })

        res = json.loads(response.get('body').read()).get('content')[0].get('text')
        # pprint(res)
        print(res)
        return res

if __name__ == "__main__":
    service = BedrockService()
    res = service.invoke_model("How many times I need to throw a dice to be sure I get 6?")
    pprint(res)