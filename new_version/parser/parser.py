import requests
import re
import csv
import os
from models import Items, Category, Feedbacks


class Parser:
    def __init__(self):
        # инициализация идентификаторов товаров
        # self.request_params = self.__init_request_params()
        # self.roots = self.__init_roots()

        with open("../../data/roots.txt", 'r') as file:
            my_list = file.readlines()
        self.roots = [int(item.strip()) for item in my_list]
        self.__parse()

    def __parse(self):
        """Метод сбора отзывов. Делаем запрос к каждой из 144698 страничек с отзывами, и если запрос непустой,
        парсим до 1000(макс.число на 1 странице) комментариев."""
        self.__create_csv()

        for root in self.roots:
            response = requests.get(f"https://feedbacks1.wb.ru/feedbacks/v1/{root}")
            if not response:
                response = requests.get(f"https://feedbacks2.wb.ru/feedbacks/v1/{root}")
                if not response:
                    continue
            if response.json():
                feedbacks = Feedbacks.parse_obj(response.json()).feedbacks
                if feedbacks:
                    for f in feedbacks:
                        if f.text != "":
                            if len(self.remove_emojis_and_english(f.text).split()) >= 30:
                                with open("../../data/new_dataset30.csv", mode="a", newline="",
                                          encoding="utf-8") as file:
                                    writer = csv.writer(file)
                                    writer.writerow([self.remove_emojis_and_english(f.text), f.productValuation])

    @staticmethod
    def __init_request_params():
        """Метод сбора параметров категорий и подкатегорий с главной страницы wildberries.ru
        Нужна для подтягивания аргументов всех категорий и подкатегорий, к которым будем делать запрос и
        искать идентификаторы(root) товаров"""
        request_params = list()
        response = requests.get(url="https://static-basket-01.wb.ru/vol0/data/main-menu-ru-ru-v2.json")
        for cat in response.json():
            cat = Category.parse_obj(cat)
            cats_child = cat.childs
            if cats_child:
                for ch in cats_child:
                    child = ch.childs
                    if child:
                        for c in child:
                            request_params.append({"shard": c.shard, "query": c.query})
                    else:
                        request_params.append({"shard": ch.shard, "query": ch.query})

        return request_params.copy()

    def __init_roots(self):
        """Метод сбора всех идентификаторов товаров. Проходимся по всем категориям и подкатегориям
        и собираем руты топ-100 товаров каждой из них, записываем их все в файл. Это необходимо для ускорения сбора
        отзывов к товарам"""
        roots = list()
        for params in self.request_params:
            shard = params['shard']
            query = params['query']
            response = requests.get(
                url=f"https://catalog.wb.ru/catalog/{shard}/catalog?appType=1&{query}&dest=-1257786")
            if response:
                products = Items.parse_obj(response.json()["data"]).products
                for pr in products:
                    roots.append(pr.root)
        with open("../../data/roots.txt", 'w') as file:
            for item in roots:
                file.write(str(item) + '\n')
        return roots.copy()

    @staticmethod
    def __create_csv():
        """Метод создания csv файла, в который будем собирать отзывы с Wildberries."""
        if not os.path.isfile("../../data/dataset30.csv"):
            with open("../../data/dataset30.csv", mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["text", "rating"])

    @staticmethod
    def remove_emojis_and_english(data):
        """Метод, который убирает эмоджи и другие символы, оставляет только русские слова и приводит их к нижнему регистру"""
        emojis = re.compile("["
                            u"\U0001F600-\U0001F64F"
                            u"\U0001F300-\U0001F5FF"
                            u"\U0001F680-\U0001F6FF"
                            u"\U0001F1E0-\U0001F1FF"
                            u"\U00002500-\U00002BEF"
                            u"\U00002702-\U000027B0"
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            u"\U0001f926-\U0001f937"
                            u"\U00010000-\U0010ffff"
                            u"\u2640-\u2642"
                            u"\u2600-\u2B55"
                            u"\u200d"
                            u"\u23cf"
                            u"\u23e9"
                            u"\u231a"
                            u"\ufe0f"
                            u"\u3030"
                            "]+", re.UNICODE)
        data_without_emojis = re.sub(emojis, '', data)
        russian_words = re.findall(r'\b[а-яА-Я]+\b', data_without_emojis)
        result = ' '.join(russian_words)
        return result.lower()


if __name__ == "__main__":
    Parser()
