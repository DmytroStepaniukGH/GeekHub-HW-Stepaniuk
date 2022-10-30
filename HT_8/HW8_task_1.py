"""
1. Програма-світлофор.
   Створити програму-емулятор світлофора для авто і пішоходів. Після
   запуска програми на екран виводиться в лівій половині - колір
   автомобільного, а в правій - пішохідного світлофора. Кожну 1 секунду
   виводиться поточні кольори. Через декілька ітерацій - відбувається зміна
   кольорів - логіка така сама як і в звичайних світлофорах (пішоходам
   зелений тільки коли автомобілям червоний).
   Приблизний результат роботи наступний:
      Red        Green
      Red        Green
      Red        Green
      Red        Green
      Yellow     Red
      Yellow     Red
      Green      Red
      Green      Red
      Green      Red
      Green      Red
      Yellow     Red
      Yellow     Red
      Red        Green
"""
import time


def traffic_light():
    while True:
        for i in range(12):
            time.sleep(1)
            if i < 4:
                print('Red\t    Green')
            elif 4 <= i <= 5:
                print('Yellow\tRed')
            elif 5 < i < 10:
                print('Green\tRed')
            else:
                print('Yellow\tRed')


if __name__ == "__main__":
    traffic_light()
