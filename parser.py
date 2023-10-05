import requests
import re
import csv
import os
from models import Items, Feedback, Text, Item


def remove_emojis_and_english(data):
    emoj = re.compile("["
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u"\U0001F680-\U0001F6FF"  # transport & map symbols
                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      u"\U00002500-\U00002BEF"  # chinese char
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
                      u"\ufe0f"  # dingbats
                      u"\u3030"
                      "]+", re.UNICODE)
    data_without_emojis = re.sub(emoj, '', data)
    russian_words = re.findall(r'\b[а-яА-Я]+\b', data_without_emojis)
    result = ' '.join(russian_words)
    return result.lower()


class ParseWB:
    def __init__(self, url: str):
        self.seller_id = self.__get_seller_id(url)

    @staticmethod
    def __get_item_id(url: str):
        regex = "(?<=catalog/).+(?=/detail)"
        item_id = re.search(regex, url)[0]
        return item_id

    def __get_seller_id(self, url):
        response = requests.get(url=f"https://card.wb.ru/cards/detail?nm={self.__get_item_id(url=url)}")
        seller_id = Items.model_validate(response.json()["data"])
        return seller_id.products[0].supplierId

    def parse(self):
        _page = 1
        self.__create_csv()
        while True:
            response = requests.get(
                f'https://catalog.wb.ru/sellers/catalog?dest=-1257786&supplier={self.seller_id}&page={_page}',
            )
            _page += 1
            items_info = Items.model_validate(response.json()["data"])
            if not items_info.products:
                break
            print(f'https://catalog.wb.ru/sellers/catalog?dest=-1257786&supplier={self.seller_id}&page={_page}')
            self.__feedback(items_info)

    @staticmethod
    def __create_csv():
        if not os.path.isfile("dataset.csv"):
            with open("dataset.csv", mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["название", "бренд", "цена", "скидка в %", "цена со скидкой", "кол-во фото в карточке", "плюсы",
                     "минусы", "наличие фото в отзыве", "полезно", "неполезно", "текст отзыва", "рейтинг"])

    @staticmethod
    def __feedback(item_model: Items):
        for product in item_model.products:
            url = f"https://feedbacks1.wb.ru/feedbacks/v1/{product.root}"
            res = requests.get(url=url)
            if res.status_code == 200:
                item = Item.model_validate(product)
                feedback = Feedback.model_validate(res.json())
                if feedback.feedbacks is not None:
                    for f in feedback.feedbacks:
                        f = Text.model_validate(f)
                        with open("dataset.csv", mode="a", newline="", encoding="utf-8") as file:
                            writer = csv.writer(file)
                            writer.writerow([
                                item.name,
                                item.brand,
                                item.priceU,
                                item.sale,
                                item.salePriceU,
                                item.pics,
                                remove_emojis_and_english(f.pros),
                                remove_emojis_and_english(f.cons),
                                f.wbUserDetails.hasPhoto,
                                f.votes.pluses,
                                f.votes.minuses,
                                remove_emojis_and_english(f.text),
                                f.productValuation])


if __name__ == "__main__":
    ParseWB("https://www.wildberries.ru/catalog/131857888/detail.aspx").parse()  # Разные аксессуары

    ParseWB("https://www.wildberries.ru/catalog/140020673/detail.aspx").parse()  # Садовые Растения - семена/растения

    ParseWB("https://www.wildberries.ru/catalog/118988177/detail.aspx").parse()  # OUTVENTURE - активный отдых

    ParseWB("https://www.wildberries.ru/catalog/166708759/detail.aspx").parse()  # ПандаРог - рюкзаки и не только

    ParseWB("https://www.wildberries.ru/catalog/149177787/detail.aspx").parse()  # Аналог Лего - игрушки

    ParseWB("https://www.wildberries.ru/catalog/122643417/detail.aspx").parse()  # BROSCOmebel - мебель

    ParseWB("https://www.wildberries.ru/catalog/153738788/detail.aspx").parse()  # Автотовары

    ParseWB("https://www.wildberries.ru/catalog/36397281/detail.aspx").parse()  # Дом и дача

    ParseWB("https://www.wildberries.ru/catalog/139405588/detail.aspx").parse()  # Лекарства

    ParseWB("https://www.wildberries.ru/catalog/36401818/detail.aspx").parse()  # Ароматы

    ParseWB("https://www.wildberries.ru/catalog/156019541/detail.aspx").parse()  # Мебель

    ParseWB("https://www.wildberries.ru/catalog/159889194/detail.aspx").parse()  # Аксессуары

    ParseWB("https://www.wildberries.ru/catalog/12014683/detail.aspx").parse()  # Sokolov - ювелирка
