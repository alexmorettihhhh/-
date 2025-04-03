import telebot
import re


TOKEN = ''
bot = telebot.TeleBot(TOKEN)

def text_to_binary(text):
    try:
        binary = ' '.join(format(ord(char), '016b') for char in text)
        if len(binary) > 4000:
            return "Ошибка: сообщение слишком длинное"
        return binary
    except Exception:
        return "Ошибка при конвертации текста"

def binary_to_text(binary):
    try:
        binary = ''.join(binary.split())
        if not re.match(r'^[01]+$', binary):
            return "Ошибка: строка должна содержать только 0 и 1"
        
        if len(binary) % 16 != 0:
            return "Ошибка: неверный формат двоичного кода"
            
        text = ''
        for i in range(0, len(binary), 16):
            char_code = int(binary[i:i+16], 2)
            text += chr(char_code)
        return text
    except Exception:
        return "Ошибка при конвертации. Проверьте формат ввода"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для конвертации текста в двоичный код и обратно.\n"
                         "Просто отправь мне текст, и я переведу его в двоичный код.\n"
                         "Или отправь двоичный код (только 0 и 1), и я переведу его обратно в текст.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()
    if not text:
        bot.reply_to(message, "Пожалуйста, отправьте текст или двоичный код")
        return
        
    if re.match(r'^[01\s]+$', text):
        result = binary_to_text(text)
    else:
        result = text_to_binary(text)
    
    bot.reply_to(message, result)

if __name__ == '__main__':
    bot.polling(none_stop=True) 