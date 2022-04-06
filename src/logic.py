import asyncio
from netschoolapi import NetSchoolAPI
import datetime

async def main():
    d = datetime.date.today()
    if int(d.month) >= 9 and int(d.month) <= 12:
        dt = 1
    else:
        dt = 2
    ns = NetSchoolAPI('') # ссылка на дневник

    await ns.login(
        '',    # Логин
        '',       # Пароль
        '', # Название школы
    )
    if dt == 1:
        dn = await ns.diary(datetime.date(2021, 9, 1), datetime.date(2022, 1, 1))
    if dt == 2:
        dn = await ns.diary(datetime.date(2022, 1, 10), datetime.date(2022, 5, 25))
    otmetki = {}
    cnt = {}
    nada_na_4 = {}
    nada_na_5 = {}
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
    print("На хорошиста надо:")
    if nada_na_4:
        print(nada_na_4)
    else:
        print("А я всё думал, когда же ты начнёшь учиться...")
    print("На отличника надо:")
    if nada_na_5:
        print(nada_na_5)
    else:
        print("Невозможно, колличеству твоих пятёрок нет числа...")
    await ns.logout()

if __name__ == '__main__':
    asyncio.run(main())
