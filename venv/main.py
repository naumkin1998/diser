import pandas as pd
import end_of_line as eol
import I_poes as Ip
import II_poes as IIp
import Nag_step as Ns

baza = pd.read_excel('print1.xlsx')

# воод данных от пользователя
input_vetv = "1527-1496"
umin = '114'
jn = '270'
# конвертация из строковой информации в числовую
list_yzls = input_vetv.split('-')

# указываетм начало ветви и к  онец расположение защиты
start = int(list_yzls[0])
end = int(list_yzls[1])


set_no_refund = set()
sort_baza_for_no_refund = baza.query(f'(Узел1 == {start} '
                                     f'or Узел2 == {start}) '
                                     f'and Тип == 1')
set_no_refund.update(sort_baza_for_no_refund['Узел1'].tolist())
set_no_refund.update(sort_baza_for_no_refund['Узел2'].tolist())



end_of_line = eol.end_of_line(start, end, baza, '0 пояс 1ступень ', set_no_refund)

set_yz_for_I_poes = Ip.belt_efinition_I_poes(end_of_line, baza, set_no_refund)

set_yzel_for_II_poes = set()

Ip.line_of_I_poes(set_yz_for_I_poes, baza, set_no_refund, set_yzel_for_II_poes)
IIp.belt_efinition_II_poes(set_yzel_for_II_poes, baza)

IIp.line_of_II_poes(set_yzel_for_II_poes, baza, set_no_refund)

print(set_yzel_for_II_poes)

Ns.Load_regim(start, end, umin, jn, baza)
