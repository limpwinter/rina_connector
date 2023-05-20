class Response:
    def __init__(self, text: str, image: str):
        self.text = text
        self.image = image

#     @classmethod
#     def from_json(cls, json_data):
#         data = json.loads(json_data)
#         return cls(data['text'], data['image'])

# # Example usage:
# json_data = '{"text": "Hello, world!", "image": "image.jpg"}'

# response = Response.from_json(json_data)
# print(response.text)
# print(response.image)
