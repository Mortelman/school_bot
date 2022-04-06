import asyncio
from netschoolapi import NetSchoolAPI
import datetime
import telebot
global nada_na_4, nada_na_5, ns
nada_na_4 = {}
nada_na_5 = {}
log = ''
pas = ''
schl = ''
ns = NetSchoolAPI('https://sgo.tomedu.ru/')

async def calculate():
    global nada_na_4, nada_na_5, log, pas, schl, ns
    d = datetime.date.today()
    if int(d.month) >= 9 and int(d.month) <= 12:
        dt = 1
    else:
        dt = 2
    await ns.login(
        log,
        pas,
        schl,
    )
    if dt == 1:
        dn = await ns.diary(datetime.date(2021, 9, 1), datetime.date(2022, 1, 1))
    if dt == 2:
        dn = await ns.diary(datetime.date(2022, 1, 10), datetime.date(2022, 5, 25))
    otmetki = {}
    cnt = {}
    for i in range(len(dn.schedule)):
        day = dn.schedule[i]
        for j in range(len(day.lessons)):
            less = day.lessons[j]
            for k in range(len(less.assignments)):
                if less.assignments[k].mark:
                    otmetki[less.subject] = otmetki.get(less.subject, 0) + int(less.assignments[k].mark)
                    cnt[less.subject] = cnt.get(less.subject, 0) + 1
    for i in otmetki:
        tmp1 = otmetki[i]
        tmp2 = cnt[i]
        while tmp1 / tmp2 < 3.5:
            tmp1 += 5
            tmp2 += 1
            nada_na_4[i] = nada_na_4.get(i, "") + "5 "
    for i in otmetki:
        tmp1 = otmetki[i]
        tmp2 = cnt[i]
        while tmp1 / tmp2 < 4.5:
            tmp1 += 5
            tmp2 += 1
            nada_na_5[i] = nada_na_5.get(i, "") + "5 "
    await ns.logout()
bot = telebot.TeleBot('5190463708:AAHFf-H4-8ItOzo5JrPD0Mf7spF8R35Uoj0')
@bot.message_handler(content_types=['text', 'document', 'audio'])
def start(message):
    bot.send_message(message.from_user.id, "Доброго времени бытия! Меня зовут Носков Леонид и я могу посчитать тебе необходимые оценки, для хорошего конца учебного периода. Но сначала мне нужны твои личные данные. Напиши свой логин от сетевого города.");
    bot.register_next_step_handler(message, get_login);
def get_login(message):
    global log;
    log = message.text;
    bot.send_message(message.from_user.id, 'Хорошо, теперь напиши свой пароль, пожалуйста. (я не украду, честно)');
    bot.register_next_step_handler(message, get_pass);

def get_pass(message):
    global pas;
    pas = message.text;
    bot.send_message(message.from_user.id, 'И из какой же ты школы?(название школы должно символ в символ повторять название на сетевом городе)');
    bot.register_next_step_handler(message, get_school);

def get_school(message):
    global schl, nada_na_4, nada_na_5
    schl = message.text
    asyncio.run(calculate())
    bot.send_message(message.from_user.id, "На хорошиста надо:");
    if nada_na_4:
        for i in nada_na_4:
            bot.send_message(message.from_user.id, i + ': ' + nada_na_4[i]);
    else:
        bot.send_message(message.from_user.id, "А я всё думал, когда же ты начнёшь учиться...");
    bot.send_message(message.from_user.id, "На отличника надо:");
    if nada_na_5:
        for i in nada_na_5:
            bot.send_message(message.from_user.id, i + ': ' + nada_na_5[i]);
    else:
        bot.send_message(message.from_user.id, "Невозможно, колличеству твоих пятёрок нет числа...");
    nada_na_4 = {}
    nada_na_5 = {}
bot.polling(none_stop=True, interval=0)
