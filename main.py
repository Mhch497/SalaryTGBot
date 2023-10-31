import telebot
import requests, json
import datetime
import time
from notion.client import NotionClient

my_ID = 742785301


TOKEN = "6292984012:AAGfxQoLRmJv5GtGf0e9PFM3UhryY7goHNo"

bot = telebot.TeleBot(TOKEN)
# bot.polling(none_stop=True, interval=0)
NOTION_API_KEY = 'secret_EnG9TIy3ZUSbG0Ha4mPipAl99FWiI2fcQqLsXXWrN0N'
NOTION_DB_ID = '0ccb0aaa47bc4404a143a8f3899013f6'
headers = {
    "Authorization": "Bearer " + NOTION_API_KEY,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

today_lessons = []
def readDatabase(databaseID, headers): #чтение информации из БД Notion
    readUrl = f"https://api.notion.com/v1/databases/{databaseID}/query"
    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code) # print(res.text)
    with open('./full-properties.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)
        for result in data['results']:

            if int(result['properties']['День']['rich_text'][0]['plain_text'] )== weekday:
                # if result['properties']['Время конца']['rich_text'][0]['plain_text'][:5] == str_now[:5]:

                    # ask_lesson(result['properties']['Название']['rich_text'][0]['plain_text'])
                dict_lesson = {}
                dict_lesson['School'] = result['properties']['Место']['title'][0]['plain_text']
                dict_lesson['Date'] = result['properties']['День']['rich_text'][0]['plain_text']
                dict_lesson['Name'] = result['properties']['Название']['rich_text'][0]['plain_text']
                dict_lesson['EndTime'] = result['properties']['Время конца']['rich_text'][0]['plain_text']
                today_lessons.append(dict_lesson)
        today_lessons.reverse()

# def check_time():



@bot.callback_query_handler(func=lambda call: True) #Обработка нажатия кнопок
def callback_worker(call):
    global Mess
    if call.data == "lessons": #call.data это callback_data, которую мы указали при объявлении кнопки

        Mess = False
        today = datetime.date.today()
        global weekday
        # weekday = today.weekday() + 1
        weekday = 4
        readDatabase(NOTION_DB_ID, headers)
        lessons_message = ''
        if len(today_lessons) >= 1:
            i = 1
            for elem in today_lessons:
                lessons_message += f"{str(i)} - {elem['Name']}\n"
                i += 1
            bot.send_message(call.message.chat.id,'Занятия сегодня: \n' + lessons_message)
    elif call.data == "working_off":
        bot.send_message(call.message.chat.id, 'Сколько она длилась?')
    elif call.data == "background_job":
        pass
    elif call.data == "Yes":
        bot.send_message(my_ID, 'Сколько было детей?')

        Mess = True
        bot.polling()

    elif call.data == "No":
        bot.send_message(my_ID, 'Ок')

def get_started(): #Тестовая  проверка работы кнопок
    # bot.send_message(message.from_user.id, 'Привет, выбери кнопку')
    global Mess
    Mess = False
    keyboard = telebot.types.ReplyKeyboardMarkup()  # наша клавиатура
    key_salary = telebot.types.InlineKeyboardButton(text='Какие занятия сегодня?', callback_data='lessons')
    keyboard.add(key_salary)  # добавляем кнопку в клавиатуру
    key_working_off = telebot.types.InlineKeyboardButton(text='Добавить отработку', callback_data='working_off')
    keyboard.add(key_working_off)
    key_working_off = telebot.types.InlineKeyboardButton(text='Фоновая работа', callback_data='background_job')
    keyboard.add(key_working_off)
    bot.send_message(my_ID, text='Привет, выбери кнопку', reply_markup=keyboard)
    bot.polling()
def ask_lesson(lesson): #Кнопки на заполнение, было ли занятие
    # bot.send_message(message.from_user.id, 'Привет, выбери кнопку')
    keyboard = telebot.types.InlineKeyboardMarkup()  # наша клавиатура
    key_salary = telebot.types.InlineKeyboardButton(text='Да', callback_data='Yes')
    keyboard.add(key_salary)  # добавляем кнопку в клавиатуру
    key_working_off = telebot.types.InlineKeyboardButton(text='Нет', callback_data='No')
    keyboard.add(key_working_off)

    bot.send_message(my_ID, text=f'Занятиие {lesson} состоялось?', reply_markup=keyboard)
    global Mess
    Mess = False
    bot.polling()



@bot.message_handler(content_types=['text']) #Вроде  получает сообщения
def get_text_messages(message):
    if Mess:
        try:
            message = int(message.text)
            bot.send_message(my_ID, text=f'На занятии было {message} учеников')
        except:
            bot.send_message(my_ID, text=f'Необходимо ввести число')



if __name__ == '__main__':
    get_started()
    while True:
        if str(datetime.datetime.now().time())[:5] == '09:00:00'[:5]:

            today = datetime.date.today()
            weekday = today.weekday() + 1
            readDatabase(NOTION_DB_ID, headers)
            if len(today_lessons) == 0:
                bot.send_message(my_ID, 'Список сегодняшних занятий пуст') #Добавить тоже проверку, чтобы не спамилось
            time.sleep(60-datetime.datetime.now().time().second)
        now = datetime.datetime.now().time()
        str_now = str(now)
        if len(today_lessons) >= 1:
            if today_lessons[0]['EndTime'][:3] == str_now[:3]:
                ask_lesson(today_lessons[0]['Name'])
                today_lessons.pop(0)


        # bot.infinity_polling()
    # responseDatabase('b13d1dd620f24692b62ecc6e998e0758', headers)

    # client = NotionClient(token_v2="Bearer " + NOTION_API_KEY)
    # page = client.get_block('https://www.notion.so/466745a938fd403982735173ee2bc4b2')
    # print(page.title)

# now = datetime.now()
# curr_time = now.strftime("%H:%M")
# while True:
#     time.sleep(1)
#     if curr_time == "12:00":
#         print('pass')
#         bot.send_message(....)