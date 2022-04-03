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


def line_of_II_poes(set_yzel_for_II_poes, baza, set_no_refund):
    for yz in set_yzel_for_II_poes:
        set_ez_for_line = set()
        sort_baza_of_end_of_line = baza.query(f'(Узел1 == {yz} or Узел2 == {yz}) '
                                              f'and (Тип == 0)'
                                              f'and (Nз1 !=0 or Nз2 !=0)')
        set_ez_for_line.update(set(sort_baza_of_end_of_line['Узел1'].tolist()))
        set_ez_for_line.update(set(sort_baza_of_end_of_line['Узел2'].tolist()))
        set_ez_for_line.remove(yz)
        for i in set_ez_for_line:
            eol.end_of_line(yz, i, baza, '2 пояс 1ступень ', set_no_refund)