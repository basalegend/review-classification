from typing import List, Optional
from pydantic import BaseModel


# Модели обновлённого парсера
class Item(BaseModel):
    """Товар. Нужен только его поле с глобальным идентификатором"""
    root: int


class Items(BaseModel):
    """Список товаров"""
    products: List[Item]


class NewFeedback(BaseModel):
    """Отзыв. Для модели нужны поля с текстом и оценкой"""
    text: str = None
    productValuation: int = None


class NewFeedbacks(BaseModel):
    """Список отзывов"""
    feedbacks: Optional[List[NewFeedback]] = None


class Chd(BaseModel):
    """Подкатегория подкатегории)))"""
    id: int = None
    parent: int = None
    name: str = None
    seo: str = None
    url: str = None
    shard: str = None
    query: str = None


class Child(BaseModel):
    """Подкатегория основнйо категории"""
    id: int = None
    parent: int = None
    name: str = None
    seo: str = None
    url: str = None
    shard: str = None
    query: str = None
    childs: Optional[List[Chd]] = None


class Category(BaseModel):
    """Категория товаров"""
    id: int = None
    name: str = None
    url: str = None
    shard: str = None
    childs: Optional[List[Child]] = None


# Модели для старого парсера
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
