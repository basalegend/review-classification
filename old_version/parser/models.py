from typing import List, Optional
from pydantic import BaseModel


class Item(BaseModel):
    """Товар. Содержит поля с основной информацией"""
    root: int
    supplierId: int
    name: str
    brand: str
    priceU: int
    sale: int
    salePriceU: int
    pics: int

class Items(BaseModel):
    """Список товаров"""
    products: List[Item]


class PhotoAndCountry(BaseModel):
    """Поле страны и наличия фото к отзвы"""
    hasPhoto: bool = None


class Votes(BaseModel):
    """Сколько пользователей посчитали отзыв полезным/бесполезным"""
    pluses: int
    minuses: int


class Text(BaseModel):
    """Текст отзыва с достоинствами и недостатками, полями 2-х моделей сверху и оценкой самого отзыва"""
    wbUserDetails: PhotoAndCountry
    pros: str = None
    cons: str = None
    votes: Votes
    text: str = None
    productValuation: int


class Feedback(BaseModel):
    """Массив с отзывами"""
    feedbackCountWithText: int
    valuation: str
    feedbacks: Optional[List[Text]]
