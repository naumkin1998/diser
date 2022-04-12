import pandas as pd
import end_of_line as eol
import I_poes as Ip
import II_poes as IIp
import Nag_step as Ns

# Чтение базы данных
baza = pd.read_excel('print1.xlsx')
# Ввод данных от пользователя
input_vetv = "41-227"
umin = '114'
jn = '270'
# Конвертация из строковой информации в числовую
list_yzls = input_vetv.split('-')
# Переменные определяющие ветвь расположения защиты
start = int(list_yzls[0])
end = int(list_yzls[1])
# Определение узлов не возврата
set_no_refund = set()
sort_baza_for_no_refund = baza.query(f'(Узел1 == {start} '
                                     f'or Узел2 == {start}) '
                                     f'and Тип == 1')
yzel1 = set(sort_baza_for_no_refund['Узел1'])
yzel2 = set(sort_baza_for_no_refund['Узел2'])
set_no_refund.update(yzel1)
set_no_refund.update(yzel2)
# Создание задания на расчет для 1ой ступени защищаемой линии
end_of_line = eol.end_of_line(start, end, baza, '0 пояс 1ступень ', set_no_refund)
# Определение узлов подстанции
set_yz_for_I_poes = Ip.belt_efinition_I_poes(end_of_line, baza, set_no_refund)
set_yzel_for_II_poes = set()
# Создание заданий на расчет для 1ых ступеней линий входящих в состав I-ого пояса
Ip.line_of_I_poes(set_yz_for_I_poes, baza, set_no_refund, set_yzel_for_II_poes)
# Определение узлов подстанции
IIp.belt_efinition_II_poes(set_yzel_for_II_poes, baza)
# Удаление первоночальных узлов при кольцевом строение сети
set_no_refund = set_no_refund.difference(yzel1)
set_no_refund = set_no_refund.difference(yzel2)
# Создание заданий на расчет для 1ых ступеней линий входящих в состав II-ого пояса
IIp.line_of_II_poes(set_yzel_for_II_poes, baza, set_no_refund)
# Создание задания на расчет для ступени отстраивающейся от нагрузочного режима
Ns.Load_regim(start, end, umin, jn, baza)