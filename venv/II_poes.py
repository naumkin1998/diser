import pandas as pd
import end_of_line as eol

def belt_efinition_II_poes(set_yzel_for_II_poes : set, baza):
    '''
    Поиск узлов подстанций для II пояса
    :param set_yzel_for_II_poes: Множество узлов для II пояса
    :param baza: DataFrame база данных
    :return: Обновленное множество узлов для  II пояса
    '''
    for yz in set_yzel_for_II_poes:
        sort_baza_of_end_of_line = baza.query(f'(Узел1 == {yz} '
                                              f'or Узел2 == {yz}) '
                                              f'and Тип == 1')
        set_yzel_for_II_poes.update(sort_baza_of_end_of_line['Узел1'].tolist())
        set_yzel_for_II_poes.update(sort_baza_of_end_of_line['Узел2'].tolist())
    return set_yzel_for_II_poes

