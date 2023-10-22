# Классификация отзывов c [Wildberries](wildberries.ru)

### Описание проекта
Этот репозиторий представляет собой моё исследование в области мультиклассовой
классификации отзывов с популярного маркетплейса [Wildberries](wildberries.ru).
Проект разделен на две версии, каждая из которых включает в себя не только код для
анализа данных, но и инструменты для сбора новых данных через парсер.

### Цели:

- Введение в NLP. До этого я не работал с текстовой информацией
- Создание своего парсера. До этого я не парсил никакие сайты
- Создание различных моделей мультиклассовой классификации, т.е. применение
знаний в области ML на практике

### Структура репозитория:

```Folder PATH listing
|   README.md - англоязычная документация
|   README_ru.md - русскоязычная документация
|   requirements.txt - необходимые модули
|       
|---data - папка с данными, на которых обучались модели
|       .gitattributes
|       dataset.csv - датасет изначальных экспериментов 
|       dataset30.csv - датасет обновлённого исследования
|       roots.txt - служебный файл для нового парсера
|       
|---new_version - доработанные парсер и исследование
|   |---parser - папка с файлами для парсера
|   |   |   models.py
|   |   |   parser.py
|   |           
|   |---research - папка ноутбуков(eng) с экспериментами 
|   |   |   navec_hudlit_v1_12B_500K_300d_100q.tar - предобученные векторные представления слов библиотеки navec
|   |   |   WildberriesReviewsClassificationResearch.ipynb - в разработке
|   |      
|---old_version - первоначальные парсер и исследования
    |---parser - папка с файлами для парсера
    |   |   models.py
    |   |   parser.py
    |         
    |---research - папка ноутбуков(ru, eng) с экспериментами 
        |   WildberriesReviewsClassificationResearch.ipynb
        |   WildberriesReviewsClassificationResearch_ru.ipynb
```