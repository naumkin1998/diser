import pandas as pd
import end_of_line as eol

def belt_efinition_I_poes(end_of_line : int, baza, set_no_refund : set):
    '''
    Фильтрация подстанции по присоединенным шинам
    :param end_of_line: Номер конца линии (подстанция)
    :param baza: DataFrame
    :param set_no_refund: Узлы не возврата
    :return: Узлы подстанций с которой электрически связан конец линии
    '''

    # отсортировка базы по номеру end_of_line() подстация
    sort_baza_of_end_of_line = baza.query(f'(Узел1 == {end_of_line} '
                                          f'or Узел2 == {end_of_line}) '
                                          f'and Тип == 1')
    set_yz_for_I_poes = set()
    set_yz_for_I_poes.update(sort_baza_of_end_of_line['Узел1'].tolist())
    set_yz_for_I_poes.update(sort_baza_of_end_of_line['Узел2'].tolist())
    set_no_refund.update(set_yz_for_I_poes)
    return set_yz_for_I_poes

def line_of_I_poes(set_yz_for_I_poes, baza, set_no_refund, set_yzel_for_II_poes):
    """

    :param set_yz_for_I_poes:
    :param baza:
    :param set_no_refund:
    :param set_yzel_for_II_poes:
    :return:
    """
    for yz in set_yz_for_I_poes:
        set_ez_for_line = set()
        sort_baza_of_end_of_line = baza.query(f'(Узел1 == {yz} or Узел2 == {yz}) '
                                              f'and (Тип == 0)'
                                              f'and (Nз1 !=0 or Nз2 !=0)')
        set_ez_for_line.update(set(sort_baza_of_end_of_line['Узел1'].tolist()))
        set_ez_for_line.update(set(sort_baza_of_end_of_line['Узел2'].tolist()))
        set_ez_for_line.remove(yz)
        for i in set_ez_for_line:
            ii = eol.end_of_line(yz, i, baza, '1 пояс 1ступень ', set_no_refund)
            if(ii != None):
                set_yzel_for_II_poes.add(ii)
    return set_yzel_for_II_poes

