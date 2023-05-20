class Request:
    def __init__(self, telegram_id: int, request_type: int):
        self.telegram_id = telegram_id
        self.request_type = request_type

#     def to_json(self):
#         return json.dumps({
#             'telegram_id': self.telegram_id,
#             'request_type': self.request_type
#         })

# # Example usage:
# telegram_id = 123456789
# request_type = 1

# req = Request(telegram_id, request_type)
# json_data = req.to_json()
# print(json_data)
