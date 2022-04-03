import pandas as pd
from string import Template
import shutil

def Load_regim(start : int, end : int, umin : int, jn : int, baza):
    ''''''
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

    number_protection = int(f'{number}{nomber_protection}')

    dictionary_OT = {
        'start': start, 'end': end,
        'number_protection': number_protection,
        'umin' : umin,
        'jn' : jn
    }
    shablon_ot = 'Shablon\-NG_SHE2607.GKZ'
    new_file_ot = f'Shablon_for_line\Наг_Режим_{start} - {end} №{number_protection}.GKZ'
    shutil.copyfile(shablon_ot, new_file_ot)


    with open(new_file_ot, 'r') as f:
        src = Template(f.read())
        result = src.substitute(dictionary_OT)
        f.close()
    with open(new_file_ot, 'w+') as f:
        f.truncate(0)
        f.write(result)