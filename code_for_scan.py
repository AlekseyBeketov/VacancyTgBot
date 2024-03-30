#!/bot
# -*- coding: UTF-8 -*-
import telebot
import schedule
import time
import sqlite3

from telebot import types
from datetime import datetime, timedelta

bot = telebot.TeleBot('test')

admin_id = 964423991


@bot.message_handler(commands=['employka'])
def startDbEmployee():
    conn = sqlite3.connect('bot_db.sql')
    cur = conn.cursor()
    cur.execute('create table if not exists users (id int primary key, name varchar(30), area_1 int, area_2 int, area_3 int, '
                'area_4 int, area_5 int, area_6 int, area_7 int, area_8 int, zanatost int, dlitelnost int)')
    cur.execute('create table if not exists workers (id int auto_increment primary key, id_emp int, name varchar(30), area_1 int, area_2 int, area_3 int, area_4 int, area_5 int, '
                'area_6 int, area_7 int, area_8 int, zanatost int, dlitelnost int,text varchar(5000), contacts varchar(500),date_of_create datetime)')
    conn.commit()
    cur.close()
    conn.close()

@bot.message_handler(commands=['asd'])
def gg():
    conn = sqlite3.connect('bot_db.sql')
    cur = conn.cursor()
    cur.execute('delete from workers')
    conn.commit()
    cur.close()
    conn.close()
# для ввода команды start
@bot.message_handler(commands=['start'])
def main(message):
    global adm_id
    adm_id = 964423991
    global area_buttons
    area_buttons = {
        "❌ Веб-дизайн и разработка": "❌ Веб-дизайн и разработка",
        "❌ Копирайтинг и контент-маркетинг": "❌ Копирайтинг и контент-маркетинг",
        "❌ Цифровой маркетинг": "❌ Цифровой маркетинг",
        "❌ Администрирование и поддержка сайтов": "❌ Администрирование и поддержка сайтов",
        "❌ Видеомонтаж и анимация": "❌ Видеомонтаж и анимация",
        "❌ Графический дизайн": "❌ Графический дизайн",
        "❌ Переводы и локализация": "❌ Переводы и локализация",
        "❌ Программирование и разработка приложений": "❌ Программирование и разработка приложений",
    }
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Я ищу работу')
    btn2 = types.KeyboardButton('Я — работодатель')
    if (message.from_user.id==adm_id):
        btn3 = types.KeyboardButton('Я — администратор')
        markup.row(btn1,btn2,btn3)
    else:
        markup.row(btn1, btn2)
    sent_message = bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\nСкажи, как бы ты хотел использовать этого бота?', reply_markup=markup)
    bot.register_next_step_handler(sent_message, on_click)

def on_click(message):
    global emp
    if message.text == 'Я ищу работу':
        emp=0
        conn = sqlite3.connect('bot_db.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM user_ads")
        cur.close()
        conn.close()
        employee_name(message)
    elif message.text == 'Я — работодатель':
        emp=1
        employee_name(message)
    elif message.text == 'Я — администратор' and message.chat.id==admin_id:
        emp=2
        bot.send_message(message.chat.id, f'Ну че, {message.from_user.first_name}, погнали! \n\nВведите Id работодателя')
        bot.register_next_step_handler(message, employee_name)

def insert_emp_id(message):

    employee_name(message)


def employee_name(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    if emp==0:
        bot.send_message(message.chat.id, 'Отлично! Для начала давай заполним твою анкету 📝', reply_markup=markup)
        bot.send_message(message.chat.id, 'Представься пожалуйста, чтобы я мог к тебе обращаться 🙂')
    if emp==1:
        bot.send_message(message.chat.id, 'Отлично! Для начала давайте заполним анкету Вашего объявления 📝', reply_markup=markup)
        bot.send_message(message.chat.id, 'Представьтесь пожалуйста, чтобы я мог к Вам обращаться 🙂')
    if emp==2:
        global emp_id
        emp_id = message.text.strip()
        bot.send_message(message.chat.id, 'Введите имя работодателя', reply_markup=markup)
    bot.register_next_step_handler(message, employee_areas)

def employee_areas(message):
    global emp_name
    emp_name=message.from_user.first_name
    global emp_adm_name
    if emp!=2:
        emp_name = message.text.strip()
    if emp==2:
        emp_adm_name = message.text.strip()

    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('❌ Веб-дизайн и разработка')
    btn2 = types.KeyboardButton('❌ Копирайтинг и контент-маркетинг')
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton('❌ Цифровой маркетинг')
    btn4 = types.KeyboardButton('❌ Администрирование и поддержка сайтов')
    markup.row(btn3, btn4)
    btn5 = types.KeyboardButton('❌ Видеомонтаж и анимация')
    btn6 = types.KeyboardButton('❌ Графический дизайн')
    markup.row(btn5, btn6)
    btn7 = types.KeyboardButton('❌ Переводы и локализация')
    btn8 = types.KeyboardButton('❌ Программирование и разработка приложений')
    markup.row(btn7, btn8)



    btn9 = types.KeyboardButton('Далее')
    markup.row(btn9)
    if emp==0:
        bot.send_message(message.chat.id, f'Хорошо, {emp_name}. Теперь давай выберем области, в которых ты хотел бы работать\n\n'
                                          f'1. Веб-дизайн и разработка: создание уникальных дизайнов, верстка, адаптивный дизайн, UI/UX оптимизация;\n\n'
                                          f'2. Копирайтинг и контент-маркетинг: написание продающих текстов, SEO оптимизация, создание контента для блогов и социальных сетей;\n\n'
                                          f'3. Цифровой маркетинг: настройка рекламных кампаний, аналитика, SEO, SMM, контекстная реклама;\n\n'
                                          f'4. Администрирование и поддержка сайтов: обновление контента, управление хостингом, обеспечение безопасности, техническая поддержка;\n\n'
                                          f'5. Видеомонтаж и анимация: создание и монтаж видеороликов, анимация логотипов, спецэффекты;\n\n'
                                          f'6. Графический дизайн: разработка логотипов, фирменного стиля, баннеров, иллюстраций;\n\n'
                                          f'7. Переводы и локализация: письменный и устный перевод, адаптация контента под разные регионы;\n\n'
                                          f'8. Программирование и разработка приложений', reply_markup=markup)
    if emp==1:
        bot.send_message(message.chat.id, f'Хорошо, {emp_name}. Теперь выберем области, которые связаны с вашим объявлением\n\n'
                                          f'1. Веб-дизайн и разработка: создание уникальных дизайнов, верстка, адаптивный дизайн, UI/UX оптимизация;\n\n'
                                          f'2. Копирайтинг и контент-маркетинг: написание продающих текстов, SEO оптимизация, создание контента для блогов и социальных сетей;\n\n'
                                          f'3. Цифровой маркетинг: настройка рекламных кампаний, аналитика, SEO, SMM, контекстная реклама;\n\n'
                                          f'4. Администрирование и поддержка сайтов: обновление контента, управление хостингом, обеспечение безопасности, техническая поддержка;\n\n'
                                          f'5. Видеомонтаж и анимация: создание и монтаж видеороликов, анимация логотипов, спецэффекты;\n\n'
                                          f'6. Графический дизайн: разработка логотипов, фирменного стиля, баннеров, иллюстраций;\n\n'
                                          f'7. Переводы и локализация: письменный и устный перевод, адаптация контента под разные регионы;\n\n'
                                          f'8. Программирование и разработка приложений', reply_markup=markup)
    if emp==2:
        bot.send_message(message.chat.id, f'Хорошо, {message.from_user.first_name}. Сейчас выбираем области для вакансии', reply_markup=markup)
    bot.register_next_step_handler(message, employee_pick)

selected_areas = set()  # Список выбранных областей

def employee_pick(message):
    def toggle_area_selection(button_text):
        if button_text.startswith("✅"):
            return button_text.replace("✅", "❌", 1)  # Заменяем только первое вхождение "✅" на "❌"
        elif button_text.startswith("❌"):
            return button_text.replace("❌", "✅", 1)  # Заменяем только первое вхождение "❌" на "✅"


    if message.text == "Далее":
        global formatted_areas
        formatted_areas = format_areas()
        bot.send_message(message.chat.id, f"Выбранные области:\n{formatted_areas}")
        global area1,area2,area3,area4,area5,area6,area7,area8
        area1,area2,area3,area4,area5,area6,area7,area8=0,0,0,0,0,0,0,0
        if "Веб-дизайн и разработка" in formatted_areas:
            area1=1
        if "Копирайтинг и контент-маркетинг" in formatted_areas:
            area2=1
        if "Цифровой маркетинг" in formatted_areas:
            area3=1
        if "Администрирование и поддержка сайтов" in formatted_areas:
            area4=1
        if "Видеомонтаж и анимация" in formatted_areas:
            area5=1
        if "Графический дизайн" in formatted_areas:
            area6=1
        if "Переводы и локализация" in formatted_areas:
            area7=1
        if "Программирование и разработка приложений" in formatted_areas:
            area8=1

        if emp==0:
            conn = sqlite3.connect('bot_db.sql')
            cur = conn.cursor()
            cur.execute("DELETE FROM users")
            cur.execute(
                    "insert into users (id, name, area_1, area_2, area_3, area_4, area_5, area_6, area_7, area_8, zanatost, dlitelnost) "
                    "values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                    message.from_user.id, emp_name, area1, area2, area3, area4, area5, area6, area7, area8, 0, 0))
            conn.commit()
            cur.close()
            conn.close()


        # conn = sqlite3.connect('bot_db.sql')
        # cur = conn.cursor()
        # cur.execute('select* from users')
        # users=cur.fetchall()
        # info=''
        # for el in users:
        #     info+=f'Id: {el[0]}, \nИмя: {el[1]}, \n1:{el[2]},\n2:{el[3]},\n3:{el[4]},\n4:{el[5]},\n5:{el[6]},\n6:{el[7]},\n7:{el[8]},\n8:{el[9]},\nЗанятость:{el[10]},\nДлительность:{el[11]}'
        # cur.close()
        # conn.close()
        # bot.send_message(message.chat.id,info)

        markup = types.ReplyKeyboardRemove(selective=False)

        employee_zanatost(message)
        return




    if message.text in area_buttons:
        button_text = area_buttons[message.text]
        button_text_with_status = toggle_area_selection(button_text)
        area_buttons.pop(message.text,None)
        area_buttons[button_text_with_status] = button_text_with_status

    markup = types.ReplyKeyboardMarkup()
    i=0
    for button_text in area_buttons.values():
        if i%2==0:
            btn1=types.KeyboardButton(button_text)
            i+=1
        else:
            btn2=types.KeyboardButton(button_text)
            markup.row(btn1, btn2)
            i+=1

    btn9 = types.KeyboardButton("Далее")
    markup.row(btn9)
    bot.register_next_step_handler(message, employee_pick)
    if "Далее" not in message.text:
        if emp==0:
            bot.send_message(message.chat.id,f"Отлично, если ты хочешь, ты можешь выбрать или убрать еще несколько областей\n\n"
                                             f"Чтобы подтвердить выбранные✅ области, нажми кнопку ДАЛЕЕ",reply_markup=markup)
        if emp==1:
            bot.send_message(message.chat.id,f"Отлично, если хотите, Вы можете выбрать или убрать еще несколько областей. "
                                             f"\n\nВаше объявление будет отправлено тем пользователям, с которыми у Вас совпадает хотя бы 1 выбранная область\n\n"
                                             f"Чтобы подтвердить выбранные✅ области, нажмите кнопку ДАЛЕЕ",reply_markup=markup)

def format_areas():
    formatted_areas = ""
    for button_text, status in area_buttons.items():
        if status.startswith("✅"):
            formatted_areas += f"{button_text.replace('❌ ', '✅ ')}\n"
    return formatted_areas

def employee_zanatost(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Полная занятость')
    btn2 = types.KeyboardButton('Частичная занятость')
    btn3 = types.KeyboardButton('Проектная работа')
    markup.row(btn1, btn2, btn3)
    sent_message = bot.send_message(message.chat.id, 'Хорошо, теперь определимся с занятостью 🕒\n\nПолная занятость: работа 8 часов в день, 5 дней в неделю;\n\nЧастичная занятость: '
                                                     'работа определенное количество часов в день или неделю, например, 4 часа в день или 20 часов в неделю;\n\nПроектная работа: '
                                                     'работа на временной основе для выполнения конкретного проекта или задания',reply_markup=markup)
    bot.register_next_step_handler(sent_message, zan_click)

def zan_click(message):
    global zanatost
    zanatost= message.text
    global zan
    if emp!=1:
        conn = sqlite3.connect('bot_db.sql')
        cur = conn.cursor()
        if message.text == 'Полная занятость':
            zan=0
            if emp==0:
                cur.execute(f"update users set zanatost=0 where id={message.from_user.id}")
        elif message.text == 'Частичная занятость':
            zan=1
            if emp==0:
                cur.execute(f"update users set zanatost=1 where id={message.from_user.id}")
        elif message.text == 'Проектная работа':
            zan=2
            if emp==0:
                cur.execute(f"update users set zanatost=2 where id={message.from_user.id}")
        conn.commit()
        cur.close()
        conn.close()

    employee_dlitelnost(message)

def employee_dlitelnost(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Краткосрочная работа')
    btn2 = types.KeyboardButton('Одноразовая работа')
    btn3 = types.KeyboardButton('Долгосрочная работа')
    markup.row(btn1, btn2, btn3)
    if emp==0:
        sent_message = bot.send_message(message.chat.id,'Отлично, теперь выбери насколько длительный период работы ты рассматриваешь 📅\n\nКраткосрочная работа: 1 месяц, 2 месяца и т.д;\n\n'
                                                        'Одноразовая работа: одноразовое задание или проект;\n\nДолгосрочная работа: на постоянной основе, '
                                                        'без определенного срока окончания', reply_markup=markup)
    if emp==1:
        sent_message = bot.send_message(message.chat.id,'Отлично, теперь выберите насколько длительный период Вы ищете работника 📅\n\nКраткосрочная работа: 1 месяц, 2 месяца и т.д;\n\n'
                                                        'Одноразовая работа: одноразовое задание или проект;\n\nДолгосрочная работа: на постоянной основе, '
                                                        'без определенного срока окончания', reply_markup=markup)
    if emp==2:
        sent_message = bot.send_message(message.chat.id,'Теперь выберите насколько длительный период ищут работников 📅', reply_markup=markup)
    bot.register_next_step_handler(sent_message, dlit_click)

def dlit_click(message):
    global dlitelnost
    dlitelnost=message.text
    global dlit
    if emp!=1:
        conn = sqlite3.connect('bot_db.sql')
        cur = conn.cursor()
        if message.text == 'Краткосрочная работа':
            dlit=0
            if emp==0:
                cur.execute(f"update users set dlitelnost=0 where id={message.from_user.id}")
        elif message.text == 'Одноразовая работа':
            dlit=1
            if emp==0:
                cur.execute(f"update users set dlitelnost=1 where id={message.from_user.id}")
        elif message.text == 'Долгосрочная работа':
            dlit=2
            if emp==0:
                cur.execute(f"update users set dlitelnost=2 where id={message.from_user.id}")
        conn.commit()
        cur.close()
        conn.close()

    if emp==0:
        emp_info(message)
    else:
        work_text(message)

def work_text(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    if emp==1:
        sent_message=bot.send_message(message.chat.id, f'{emp_name}, Ваша анкета почти готова! Теперь отправьте сюда текст, который будет в объявлении 🧾', reply_markup=markup)
    if emp==2:
        sent_message=bot.send_message(message.chat.id, f'{message.from_user.first_name}, сюда нужно занести текст, который будет в объявлении 🧾', reply_markup=markup)
    bot.register_next_step_handler(sent_message, text_click)

def text_click(message):
    global w_text
    w_text = message.text

    work_contacts(message)

def work_contacts(message):
    if emp==1:
        sent_message=bot.send_message(message.chat.id, 'Финальный шаг: оставьте контакты, по которым, в случае чего, можно будет с Вами связаться 👤 ☎️ 📩')
    if emp==2:
        sent_message=bot.send_message(message.chat.id, 'Финальный шаг: Внесите контакты пользователя 👤 ☎️ 📩')
    bot.register_next_step_handler(sent_message, contact_click)

def contact_click(message):
    global w_contact
    w_contact = message.text
    global current_datetime
    current_datetime = datetime.now()
    if emp==2:
        conn = sqlite3.connect('bot_db.sql')
        cur = conn.cursor()
        cur.execute(
            "insert into workers (id_emp, name, area_1, area_2, area_3, area_4, area_5, area_6, "
            "area_7, area_8, zanatost, dlitelnost, text, contacts,date_of_create) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                emp_id, emp_adm_name, area1, area2, area3, area4, area5, area6, area7, area8, zan, dlit, w_text,
                w_contact,current_datetime)
        )
        conn.commit()
        cur.close()
        conn.close()

    work_info(message)

def work_info(message):
    markup = types.ReplyKeyboardMarkup()
    if emp==1:
        btn1 = types.KeyboardButton('Отправить объявление на проверку модераторам 💼')
        btn2 = types.KeyboardButton('Заполнить анкету заново 📝')
        markup.row(btn1)
        markup.row(btn2)
    if emp==2:
        btn1 = types.KeyboardButton('Главное меню 💼')
        btn2 = types.KeyboardButton('Заполнить анкету заново 📝')
        markup.row(btn1)
        markup.row(btn2)
    sent_message=bot.send_message(message.chat.id, f'{emp_name}, Ваше объявление готово! 📋\n\n'
                                      f'Выбранные области:\n{formatted_areas}'
                                      f'\nЗанятость: {zanatost}'
                                      f'\nЖелаемая длительность: {dlitelnost}',reply_markup=markup)

    bot.send_message(message.chat.id, f'Текст вашего объявления:\n{w_text}')
    bot.send_message(message.chat.id, f'Контакты для связи:\n{w_contact}')

    bot.register_next_step_handler(sent_message, final_check_work)

def final_check_work(message):
    if message.text == 'Заполнить анкету заново 📝':
        main(message)
    elif message.text=='Отправить объявление на проверку модераторам 💼':
        bot.send_message(adm_id,'НОВОЕ ОБЪЯВЛЕНИЕ!')
        bot.send_message(adm_id,f'Id: {message.from_user.id}'
                         f'\nИмя: {emp_name}'
                                   f'\nВыбранные области:\n{formatted_areas}'
                                      f'\nЗанятость: {zanatost}'
                                      f'\nДлительность: {dlitelnost}')
        bot.send_message(adm_id,f'Текст:\n{w_text}'
                                   f'\n\nКонтакты:\n{w_contact}')



        bot.send_message(message.chat.id,'Ваше объявление будет направлено модераторам для проверки, после чего оно автоматически будет рассылаться пользователям 📩'
                                         '\n\nТеперь, если Вы хотите, Вы можете добавить другое объявление или смотреть объявления других работодателей')
        main(message)
    if ((message.text=='Главное меню 💼') and (emp==2)):
        conn = sqlite3.connect('bot_db.sql')
        cur = conn.cursor()
        cur.execute("drop view new_ad_notification")
        cur.execute(
            "CREATE VIEW new_ad_notification AS SELECT id FROM users WHERE (((area_1 = 1 AND %s = 1) OR"
            "(area_2 = 1 AND %s = 1) OR"
            "(area_3 = 1 AND %s = 1) OR"
            "(area_4 = 1 AND %s = 1) OR"
            "(area_5 = 1 AND %s = 1) OR"
            "(area_6 = 1 AND %s = 1) OR"
            "(area_7 = 1 AND %s = 1) OR"
            "(area_8 = 1 AND %s = 1)) AND zanatost = %s AND dlitelnost = %s)"
            % (area1, area2, area3, area4, area5, area6, area7, area8, zan, dlit)
        )
        cur.execute('select* from workers')
        workers=cur.fetchall()
        info=''
        for el in workers:
            info+=(f'Id: {el[1]}, \nИмя: {el[2]}, \n1:{el[3]},\n2:{el[4]},\n3:{el[5]},\n4:{el[6]},'
                   f'\n5:{el[7]},\n6:{el[8]},\n7:{el[9]},\n8:{el[10]},\nЗанятость:{el[11]},\nДлительность:{el[12]}\nТекст:{el[13]},\nКонтакты:{el[14]},\nВремя:{el[15]}\n\n')

        notification_users = cur.execute("SELECT id FROM new_ad_notification").fetchall()
        for user_id in notification_users:
            ad_text = w_text
            send_ad_to_user(user_id[0], ad_text)
            schedule.run_pending()
            time.sleep(1)
        cur.close()
        conn.close()
        bot.send_message(message.chat.id,info)
        main(message)


def emp_info(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Искать объявления 💼')
    btn2 = types.KeyboardButton('Заполнить анкету заново 📝')
    markup.row(btn1)
    markup.row(btn2)


@bot.message_handler(func=lambda message: message.text == 'Искать объявления 💼')
def final_check_user(message):
    global user_id
    user_id = message.from_user.id  # Идентификатор текущего пользователя
    notification_mode(user_id)


def notification_mode(user_id):
    conn = sqlite3.connect('bot_db.sql')
    cur = conn.cursor()
    cur.execute("drop view user_ads")
    cur.execute(
        "CREATE VIEW user_ads AS SELECT workers.id_emp AS user_id, workers.text AS ad_text FROM workers JOIN users ON ((users.area_1 = 1 AND workers.area_1 = 1) OR"
        "(users.area_2 = 1 AND workers.area_2 = 1) OR"
        "(users.area_3 = 1 AND workers.area_3 = 1) OR"
        "(users.area_4 = 1 AND workers.area_4 = 1) OR"
        "(users.area_5 = 1 AND workers.area_5 = 1) OR"
        "(users.area_6 = 1 AND workers.area_6 = 1) OR"
        "(users.area_7 = 1 AND workers.area_7 = 1) OR"
        "(users.area_8 = 1 AND workers.area_8 = 1)) WHERE users.zanatost = workers.zanatost AND users.dlitelnost = workers.dlitelnost;")
    conn.commit()

    # Получение объявлений пользователя из представления
    ads = cur.execute("SELECT ad_text FROM user_ads").fetchall()
    #cur.execute("SELECT * FROM user_ads")
    for ad in ads:
        ad_text = ad[0]
        #bot.send_message(user_id,f'{ad_text}')
        # Отправка объявления пользователю
        #schedule.every(1).minutes.do(send_ad_to_user, user_id, ad_text)
        send_ad_to_user(user_id,ad_text)
        schedule.run_pending()
        time.sleep(5)

    cur.close()
    conn.close()

def send_ad_to_user(user_id, ad_text):
    bot.send_message(user_id, ad_text)

    # Запускаем задачу каждый день в определенное время
    schedule.every().day.at("02:00").do(delete_old_records)

    # Бесконечный цикл для выполнения задачи по расписанию
    #while True:
    #    schedule.run_pending()
    #    time.sleep(1)

def delete_old_records():
    conn = sqlite3.connect('bot_db.sql')
    #cur = conn.cursor()

    current_datetime = datetime.now()
    #print(datetime.now())
    #two_weeks_ago = current_datetime - timedelta(weeks=2)
    #two_weeks_ago = current_datetime - timedelta(seconds=30)

    #cur.execute("DELETE FROM workers WHERE date_of_create < DATE_SUB(NOW(), INTERVAL 3 MINUTE)")

    conn.commit()
    conn.close()

@bot.message_handler(func=lambda message: message.text == 'Заполнить анкету заново 📝')
def zanovo(message):
    if emp==0:
        conn = sqlite3.connect('bot_db.sql')
        cur = conn.cursor()
        cur.execute(f"delete from users where id={message.from_user.id}")
        conn.commit()
        cur.close()
        conn.close()
    main(message)

bot.polling(none_stop=True)

