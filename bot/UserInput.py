# class UserInput:

#     def __init__(self,
#                  command, 
#                  requires_auth = False, 
#                  controller_method = None,
#                  activated_button_layout = None,
#                  reply = None,
#                  ):
#         self.command = command
#         self.requires_auth = requires_auth
#         self.controller_method = controller_method
#         self.activated_button_layout = activated_button_layout
#         self.reply = reply

#     def reg_check(self):
#         _, authorized = DataBase.get_user_auth_status(self.telegram_id)
#         return authorized
    
#     async def change_keyboard_and_reply(self):    
#         keyboard = types.ReplyKeyboardMarkup(keyboard=self.activated_button_layout, resize_keyboard=True)
#         await bot.send_message(self.telegram_id, self.reply, reply_markup=keyboard)
    
#     async def try_execute(self, message:types.Message):

#         self.telegram_id = message.from_id
#         self.invoke_text = message.text

#         if self.requires_auth:

#             success = self.reg_check()
#             if success:
#                 await self.execute()
#             else:
#                 await bot.send_message(self.telegram_id, 'Недоступно для неавторизованных пользователей.')

#         else:
#             await self.execute()

#     async def execute(self):

#         self.controller_method()

#         if self.activated_button_layout:
#             await self.change_keyboard_and_reply()

# # user_inputs = []
# # user_inputs.append( UserInput('/start'), TgController.try_reg_user)

# # for user_input in user_inputs:

# #     @dp.message_handler(Text(equals='/start'))