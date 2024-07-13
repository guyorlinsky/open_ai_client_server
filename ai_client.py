
"""
this file is made for choosing and creating a bot.
"""
if __name__ == "__main__":
    from ai_bot_mode1 import AIBotMode1
    from ai_bot_model2 import AIBotMode2

    mode = input("Enter desired bot mode: 1 or 2: ")
    while mode not in ('1', '2'):
        mode = input("Enter desired bot mode: 1 or 2: ")

    username = input("Enter desired bot user name: ")

    if mode == '1':
        lines_to_response = int(input("Enter the number of lines after which the bot should respond: "))
        bot_client = AIBotMode1(username, lines_to_response)
    else:
        interval = int(input("Enter the number of seconds after which the bot should respond: "))
        bot_client = AIBotMode2(username, interval)
