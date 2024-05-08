# OptFALT
Программа OptFALT призвана упростить процедуру эскизного (концептуального) проектирования небольших БПЛА самолётного типа. Нашей целью было дать разработчикам простой и быстрый инструмент оценки ключевых геометрических параметров и лётно-технических данных проектируемого самолёта. Программа позволяет быстро менять конфигурацию аппарата: изменять целевые показатели полезной нагрузки, дальности, скорости, времени полёта, рассматривать различные конструкционные материалы, аэродинамические профили, силовые установки, конструктивные схемы. 

Программа в относительно грубом приближении итерационно решает уравнение существования самолёта. На данный момент (без доработок кода) она подходит для проектирования самолётов нормальной аэродинамической схемы с классической электрической силовой установкой. Подразумевается, что пользователь может настраивать внутренний цикл программы под свою задачу.

# INPUT
SETTINGS.py. Настройки решателя. Содержит константы и расположения модулей программы.

PARAMS.csv. Здесь даются данные для расчёта массы самолёта. Массы компонентов, погонные плотности материалов и тд. Это основной файл, с которым работает пользователь. В нём заданы используемые технологии и конструктивные решения. От того, насколько детально описан аппарат в данном файле зависит точность итогового решения. Подразумевается итерационное уточнение, расширение файла параметров по мере проработки деталей проекта в процессе проектирования.

PERFORMANCE.py Содержит требуемые характеристики. Например, крейсерскую скорость, полезную нагрузку, время полёта и тд. Добавление новых требований требует изменения внутреннего цикла программы.

# OUTPUT
GEOM.py. Содержит рациональные геометрические параметры самолёта, к которым сошёлся алгоритм в ходе работы. То, насколько эти параметры соотносятся с реальностью, зависит от точности описания технологии в PARAMS.py, а также степени продвинутости алгоритма во внутреннем цикле.

AERO.py. Содержит крейсерские характеристики для геометрии из GEOM.csv

# Зависимости
Программа написана на языке Python 3.10. Необходим интерпретатор python. 
На данный момент для работы с программой используются блокноты Jupyter-lab. Установка: https://jupyter.org/install
Программа использует в качестве расчётного модуля программу XFoil6.99.exe. Установка: https://web.mit.edu/drela/Public/web/xfoil/
В качестве модулей реализованы библеотеки:
-Аэродинамических функций. aerolib.py
-Работы с XFoil. xfoillib.py


