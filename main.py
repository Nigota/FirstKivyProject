from kivymd.uix.list import OneLineAvatarListItem
from kivymd.app import MDApp
from kivymd.toast import toast

from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty
from kivy.core.window import Window

import json

Window.size = (330, 553)

with open('screens.json', encoding='utf-8') as f:
    '''Открытие файла, в котором хранятся все данные'''
    text = json.load(f)


class MenuButton(Button):
    '''Класс кастомной кнопки'''
    Builder.load_file('applibs/kv/MenuButton.kv')


class Menu(Screen):
    '''Экран меню'''
    Builder.load_file('applibs/kv/Menu.kv')

    def __init__(self, **kwargs):
        '''Загрузка всех кнопок'''
        super().__init__(**kwargs)
        for i in range(1, text["count"] + 1):
            self.sv.buttons.add_widget(MenuButton(text=text[str(i)]["title"]))


class Settings(Screen):
    '''Экран настроек'''
    Builder.load_file('applibs/kv/Setting.kv')


class OK(Screen):
    '''Экран конспекта'''
    Builder.load_file('applibs/kv/OK.kv')

    def __init__(self, n, **kwargs):
        '''Загрузка всех элементов конспекта'''
        super().__init__(**kwargs)
        self.tb.title = text[str(n)]["title"]
        self.tabs.tab_image.image.source = text[n]["image"]
        self.tabs.tab1.label1.text = text[n]["tab1"]["label1"]
        self.tabs.tab2.label2.text = text[n]["tab2"]["label2"]
        self.tabs.tab3.label3.text = text[n]["tab3"]["label3"]

    def answer(self, n, index, ans):
        '''Проверка ответа'''
        if ans == text[n][index]["answer"]:
            toast('Правильно')
        else:
            toast('Не верно(')


class EditOK(Screen):
    '''Экран настроек содержимого конспекта'''
    Builder.load_file('applibs/kv/EditOK.kv')

    def __init__(self, n, **kwargs):
        '''Загрузка содержимого конспекта'''
        super().__init__(**kwargs)
        self.tb.title = text[str(n)]["title"]
        self.tabs.tab_image.image.source = text[n]["image"]
        self.tabs.tab1.task1.text = text[n]["tab1"]["label1"]
        self.tabs.tab2.task2.text = text[n]["tab2"]["label2"]
        self.tabs.tab3.task3.text = text[n]["tab3"]["label3"]


class NavigationItem(OneLineAvatarListItem):
    '''Класс кнопок в боковой панели'''
    icon = StringProperty()


class App(MDApp):
    '''Класс приложения'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.edition = False  # отвечает за редактирование
        self.n = 1  # номер текущего конспекта
        self.title = 'My App'  # имя приложения
        self.theme_cls.primary_palette = 'Cyan'  # цвет в приложении
        self.theme_cls.theme_style = 'Light'  # тема в приложении

    def build(self):
        '''Создание приложения и открытие экрана меню'''
        self.root.screen_mg.add_widget(Menu(name="Menu"))
        self.root.screen_mg.add_widget(Settings(name="Settings"))

    def open_ok(self, n=1):
        '''Открытие конспекта по нажатию кнопки'''
        n = str(text["count"] - n)
        k = OK(n, name=n)
        self.root.screen_mg.transition.direction = 'right'
        self.root.screen_mg.add_widget(k)
        self.root.screen_mg.current = n

    def setting(self):
        '''Переход на экран настроек'''
        self.root.screen_mg.current = 'Settings'

    def add_new_ok(self, t):
        '''Добавление новой кнопки на экран меню'''
        if len(t) > 1:
            btn = MenuButton(text=t)
            self.root.screen_mg.get_screen("Menu").ids.buttons.add_widget(btn)
            self.new_ok()  # создание нового конспекта в хранилище данных
            text[str(text["count"])]["title"] = t

    def new_ok(self):
        '''Добавление в файл данных нового конспекта'''
        text["count"] += 1
        text[str(text["count"])] = {"title": "",
                                    "image": "",
                                    "tab1": {"label1": "", "answer": ""},
                                    "tab2": {"label2": "", "answer": ""},
                                    "tab3": {"label3": "", "answer": ""}}
        self.edition = True  # редактирование было осуществленно

    def edit(self, n):
        '''Открытие экрана редактирования конспекта'''
        self.n = n  # запоминаем номер конспекта, чтобы обращаться к нему (изменять)
        k = EditOK(n, name="Edition")
        self.root.screen_mg.transition.direction = 'right'
        self.root.screen_mg.add_widget(k)
        self.root.screen_mg.current = "Edition"

    def save(self):
        '''Сохранение изменений в конспекте'''
        sc = self.root.screen_mg.current_screen  # текущий экран (экран редактирования)
        # предыдущий экран
        prev_sc = self.root.screen_mg.get_screen(
            self.root.screen_mg.previous())  # предыдущий экран (который редактируем)

        # изменение текстов на экране
        prev_sc.tabs.tab1.label1.text = sc.tabs.tab1.task1.text
        prev_sc.tabs.tab2.label2.text = sc.tabs.tab2.task2.text
        prev_sc.tabs.tab3.label3.text = sc.tabs.tab3.task3.text

        # изменение текстов в файле
        text[self.n]["tab1"]["label1"] = sc.tabs.tab1.task1.text
        text[self.n]["tab2"]["label2"] = sc.tabs.tab2.task2.text
        text[self.n]["tab3"]["label3"] = sc.tabs.tab3.task3.text

        # изменение ответов (если были изменения)
        if len(sc.tabs.tab1.answer1.text) > 0:
            text[self.n]["tab1"]["answer"] = sc.tabs.tab1.answer1.text
        if len(sc.tabs.tab2.answer2.text) > 0:
            text[self.n]["tab2"]["answer"] = sc.tabs.tab2.answer2.text
        if len(sc.tabs.tab3.answer3.text) > 0:
            text[self.n]["tab3"]["answer"] = sc.tabs.tab3.answer3.text

        self.edition = True  # редактирование было осуществленно
        self.back()  # возвращение на предыдущий конспект

    def back(self):
        '''Возвращение на предыдущий экран'''
        sc = self.root.screen_mg.current_screen
        self.root.screen_mg.current = self.root.screen_mg.previous()
        self.root.screen_mg.remove_widget(sc)

    def menu(self):
        sc = self.root.screen_mg.current_screen
        if sc.name != "Menu" and sc.name != "Settings":
            self.root.screen_mg.remove_widget(sc)
        self.root.screen_mg.current = "Menu"

    def on_stop(self):
        '''Сохранение данных на закрытии приложения'''
        if self.edition:
            with open('screens.json', 'w') as f:
                f.write(json.dumps(text))


App().run()
