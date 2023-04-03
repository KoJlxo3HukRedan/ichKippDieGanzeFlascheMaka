 


from bs4 import BeautifulSoup

import requests

def lists_to_dict(keys, values):
    result_dict = {}
    for i in range(len(keys)):
        result_dict[keys[i]] = values[i]
    return result_dict

def first_word(text):
    # Удаляем пробелы в начале и в конце строки
    text = text.strip()
    # Ищем первый пробел в строке
    space_index = text.find(" ")
    if space_index == -1:
        # Если пробел не найден, то возвращаем всю строку
        return text
    else:
        # Если пробел найден, то возвращаем подстроку до первого пробела
        return text[:space_index]


def ToList(text):
   words = []
   current_word = ""
   
   for i in range(len(text)):
    if text[i].isupper():
        if current_word != "":
            words.append(current_word)
        current_word = text[i]
    else:
        current_word += text[i]

   words.append(current_word)

   return words

def ToEnglishName(text):
   translit_dict = {
      'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
      'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
      'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
      'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts',
       'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 
      'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', ' ':'-'
   }
   translit_text = ''
   for char in text:
      if char.lower() in translit_dict:
         translit_text += translit_dict[char.lower()]
      else:
         translit_text += char
   return translit_text

# то были полезные алгоритмы, а теперь сама суть
######################################################################################

#тут нам нужно вывести список всех врачей в городе
def Get_all_doctors(city, part):  #DocType - это будет в кнопках "взрослый", "детский", "стоматолог"
   
   fle = requests.get(f'https://prodoctorov.ru/{ConverterCities(city)}/vrach/')

   site = BeautifulSoup(fle.text, 'lxml')

   lsd = []
   for i in site.find_all('span', class_='b-text-unit__text'):

 
      lsd.append(i.text)

   #lsd_len = len[lsd]
   mid_len = 0
   if len(lsd)%2 == 0:
      mid_len = int(len(lsd)/2)
   else:
      mid_len = int((len(lsd)+1)/2)
   
   for i in range(0, len(lsd)):
      lsd[i] = lsd[i].replace(' ', '')
      lsd[i] = lsd[i].replace('\n', '')

   list1 = []
   
   

   if part == 1:
      for i in range(0, mid_len):
         list1.append(lsd[i])
      

   if part == 2:
      for i in range(mid_len, len(lsd)):
         list1.append(lsd[i])

   return list1
#теперь работаю с url врачей 

#example_url = 'https://prodoctorov.ru/kropotkin/akusher/'
def GetAllDoctors(doctor_profession, city_, page): #page - номер страницы
   fle1 = requests.get(f'https://prodoctorov.ru/{ConverterCities(city_)}/{ConverterCities(doctor_profession)}/?page={page}')
   site1 = BeautifulSoup(fle1.text, 'lxml')
   names_list = list()
   

   for i in site1.find_all('div', class_='b-doctor-card__name'):

    
      names_list.append(i.text)
   return names_list


def Get_id_list(doctor_profession, city_, page):
   fle1 = requests.get(f'https://prodoctorov.ru/{ConverterCities(city_)}/{ConverterCities(doctor_profession)}/?page={page}')
   site1 = BeautifulSoup(fle1.text, 'lxml')
   id_list = list() 
   for i in site1.find_all('div', class_='b-doctor-card'):
      id_list.append(i['data-doctor-id'])
   
   return id_list




def GetDoctorUrlList(doctor_names, id): #doctor_names и id - это оба списки, получаемые из Get_id_list() и GetAllDoctors()
   
   EngDoctorList = list()
   for i in doctor_names:
      EngDoctorList.append(ConverterCities(first_word(i)))
   
   url_list = list()

   for i in range(0, len(EngDoctorList)):
      url_list.append(f'https://prodoctorov.ru/kropotkin/vrach/{id[i]}-{EngDoctorList[i]}/')

   return url_list


# это были основные функции которые понядобятся, а теперь нужно подключить телеграм


# #################################################################################################################################
def ConverterCities(text):
   if text == 'Ростов-На-Дону':
      return 'rostov-na-donu'
   if text == 'Нижний Новгород':
      return 'nnovgorod'
   if text == 'Великий Новгород':
      return 'vnovgorod'
   if text == 'Санкт-Петербург':
      return 'spb'
   else:
      return ToEnglishName(text)

import telebot

from telebot import types
Token = '5117703789:AAELu03aOFNb3w3eRYGKCRFpstj87KragoM'
bot = telebot.TeleBot(Token)

# --------------------------------------------------------------------
#print(Get_all_doctors('кропоткин', part))
city = 'кропоткин'           #                # это наш конфиг и значения по умолчанию
doc_profession = 'Акушер'  #
page = 1
# --------------------------------------------------------------------

previous_message = ''

@bot.message_handler(commands=['start'])
def welcome(message):
   bot.send_message(message.chat.id, 'вас приветствует бот для быстрого поиска врачей по всей РФ. Вот список доступных комманд \n /set_city - выбрать населенный пункт. Пишите его на русском (например: Гулькевичи) \n /set_doctor - выбрать врача который вам нужен (например "терапевт") \n /profs - вывести всех возможных врачей в выбранном вами населенном пункте (если врачей там нет - выведет "None") \n /config - вывести ваш конфиг поиска (город, врач, который вас интересует)\n \n /search_by_config - искать по выбранному конфигу \n /next - вывести следующую страницу ')
   global page
   page = 1
@bot.message_handler(commands=['config'])
def config(message):
   bot.send_message(message.chat.id, f'ваш населенный пункт - это {city}, нужный вам врач - {doc_profession}')
   global page
   page = 1
@bot.message_handler(commands=['set_city'])
def set_city(message):
   bot.send_message(message.chat.id, 'введите ваш населенный пункт: ')
   global page
   page = 1
   global previous_message
   print(previous_message)
   previous_message = '/set_city'
   
   
@bot.message_handler(commands=['set_doctor'])
def set_doctor(message):
   bot.send_message(message.chat.id, 'введите специальность врача которая вас интересует (например "терапевт")')
   global page
   page = 1
   
   global previous_message
   previous_message = '/set_doctor'


@bot.message_handler(commands=['profs'])
def professions(message):
   global previous_message
   previous_message = '/profs'
   list1 = Get_all_doctors(city, 1)
   list2 = Get_all_doctors(city, 2)
   bot.send_message(message.chat.id, f'вот список всех возможных врачей в выбранном населенном пункте ({city})')
   bot.send_message(message.chat.id, f'{list1}')
   bot.send_message(message.chat.id, f'{list2}')
   global page
   page = 1   


@bot.message_handler(commands=['search_by_config'])
def SearchByConfig(message):
   global page
   id_list = Get_id_list(doc_profession, city, page)
   
   doc_names_list = GetAllDoctors(doc_profession, city, page)

   url_list = GetDoctorUrlList(doc_names_list, id_list)

   IdAndNames_list = list()

   for i in range(0, len(doc_names_list)):
      IdAndNames_list.append(doc_names_list[i] + ' ' + url_list[i])  
   BotText = ''
   for i in IdAndNames_list:
      BotText += i +'\n'
   if len(IdAndNames_list) == 0:
      bot.send_message(message.chat.id, '*404* \n Врачей по конфигу нет. Выберите другой город или другого врача. Возможно вы допустили ошибку в названии города или врача, либо выбранный вами город не поддерживается этим ботом')
   else:
      bot.send_message(message.chat.id, f"воспроизводится поиск врачей по конфигу \n{BotText}\n(если хотите вывести конфиг - пишите /config, следующас страница - /next)")

@bot.message_handler(commands=['next'])
def next(message):
   global page
   page+=1
   
   id_list = Get_id_list(doc_profession, city, page)
   
   doc_names_list = GetAllDoctors(doc_profession, city, page)

   url_list = GetDoctorUrlList(doc_names_list, id_list)

   IdAndNames_list = list()

   for i in range(0, len(doc_names_list)):
      IdAndNames_list.append(doc_names_list[i] + ' ' + url_list[i])  
   BotText = ''
   for i in IdAndNames_list:
      BotText += str(i) +'\n'
   if len(IdAndNames_list) == 0:
      bot.send_message(message.chat.id, 'все врачи были уже выведены ранее, на этой странице нет врачей')
   else:
      bot.send_message(message.chat.id, f"воспроизводится поиск врачей по конфигу \n{BotText}\n(если хотите вывести конфиг - пишите /config, следующас страница - /next)")





@bot.message_handler(content_types=['text']) #до меня дошла гениальная стратегия-костыль на этом обосранном pyTelegramApi
def CommandManager(message):                # скорее всего можно было бы сделать легче на других апи, но времени уже нема

   global previous_message

   global city
   global doc_profession

   if previous_message == '/set_city':
      
      city = message.text
      bot.send_message(message.chat.id, f'вы изменили населенный пункт на "{message.text}", хотите вывести все возможные специальности врачей в вашем городе, тогда пишите (или нажмите) /profs')

   if previous_message == '/set_doctor':
      

      doc_profession = message.text

      bot.send_message(message.chat.id, f'вы изменили специализацию врача на "{message.text}"')

bot.infinity_polling()