import os
import pandas as pd
from string import Template
import shutil

def end_of_line(start : int, end : int, baza, step : str, set_no_refund : set):
    """

    :param start: начальный ветви расположения защиты
    :param end: конец ветви расположения защиты
    :param baza: исходные данные
    :param step: ступень
    :param set_no_refund:  узлы не возврата
    :return: конец линии
    """
    # сортировка базы данных по исходным данным
    sort_of_vetv = baza.query(f'(Узел1 == {start} and Узел2 == {end})'
                              f'or (Узел1 == {end} and Узел2 == {start})')


    # определяем конец линии или начало
    protection = set()
    protection.update(sort_of_vetv['Nз1'])
    protection.update(sort_of_vetv['Nз2'])
    protection.remove(0)
    nomber_protection = protection.pop()


    # определяем номер элемента(линии)
    number = int(sort_of_vetv.iloc[0]['Nэл.'])

    # определение противоположного конца линии

    sort_of_number_element = baza[(baza['Nэл.'] == number)].query('(Nз1 !=0 or Nз2 !=0)'
                                                                  f'and (Nз1 !={nomber_protection} '
                                                                  f'and Nз2 !={nomber_protection})')

    # определяем номер конца линии
    if (len(sort_of_number_element) == 0):
        return
    yzel1 = int(sort_of_number_element.iloc[0]['Узел1'])
    yzel2 = int(sort_of_number_element.iloc[0]['Узел2'])


    list_yzel = [yzel1, yzel2]
    count_yz = 0
    end_of_line = 0

    # print('начало цикла')
    for yz in list_yzel:
        if (len(baza.query(f'(Nз1 !=0 or Nз2 !=0)'
                        f'and '
                        f'(Узел1 == {yz}'
                        f'or Узел2 == {yz})'))
                > count_yz):
            count_yz = len(baza.query(f'(Nз1 !=0 or Nз2 !=0)'
                                   f'and '
                                   f'(Узел1 == {yz}'
                                   f'or Узел2 == {yz})'))
            end_of_line = yz

    if(end_of_line in set_no_refund):
        return

    number_protection = int(f'{number}{nomber_protection}')
    # print(f'{start}, {end}, {number_protection}, {end_of_line}')


    dictionary_OT = {
        'start' : start, 'end' : end,
        'number_protection' : number_protection,
        'end_of_line' : end_of_line
        }


    """заполнение и сохранение файла по отстройке"""

    if not os.path.isdir("Shablon_for_line"):
         os.mkdir("Shablon_for_line")

    shablon_ot = 'Shablon\-OT_SHE2607.GKZ'
    new_file_ot = f'Shablon_for_line\{step}{start} - {end_of_line} №{number_protection}.GKZ'
    shutil.copyfile(shablon_ot, new_file_ot)


    with open(new_file_ot, 'r') as f:
        src = Template(f.read())
        result = src.substitute(dictionary_OT)
        f.close()
    with open(new_file_ot, 'w+') as f:
        f.truncate(0)
        f.write(result)

    return end_of_line