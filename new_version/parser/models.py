from typing import List, Optional
from pydantic import BaseModel


class Item(BaseModel):
    """Товар. Нужен только его поле с глобальным идентификатором"""
    root: int


class Items(BaseModel):
    """Список товаров"""
    products: List[Item]


class Feedback(BaseModel):
    """Отзыв. Для модели нужны поля с текстом и оценкой"""
    text: str = None
    productValuation: int = None


class Feedbacks(BaseModel):
    """Список отзывов"""
    feedbacks: Optional[List[Feedback]] = None


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
