# Reviews Classification with [Wildberries](https://www.wildberries.ru/)

### Project Description
This repository represents my research in the field of multiclass classification of reviews from the popular
marketplace [Wildberries](wildberries.ru). The project is divided into two versions, each of them includes not
only code for data analysis but also tools for collecting new data through a parser.

### Goals:

- Introduction to NLP. I had not worked with textual information.
- Creating my own parser. I had not parsed any websites.
- Developing various multiclass classification models, i.e., applying knowledge in the field of ML in practice.

### Repository Structure:

```Folder PATH listing
|   README.md - English documentation
|   README_ru.md - Russian documentation
|   requirements.txt - required modules
|       
|---data - folder with data used for model training
|       .gitattributes
|       dataset.csv - dataset from initial experiments
|       dataset30.csv - dataset from updated research
|       roots.txt - util file for the new parser
|       
|---new_version - improved parser and research
|   |---parser - folder with files for the parser
|   |   |   models.py
|   |   |   parser.py
|   |           
|   |---research - notebook (in English) with experiments 
|   |   |   navec_hudlit_v1_12B_500K_300d_100q.tar - pretrained word vector representations from the navec library
|   |   |   WildberriesReviewsClassificationResearch_new.ipynb - in development
|   |      
|---old_version - initial parser and research
    |---parser - folder with files for the parser
    |   |   models.py
    |   |   parser.py
    |         
    |---research - notebooks (in Russian and English) with experiments 
        |   WildberriesReviewsClassificationResearch.ipynb
        |   WildberriesReviewsClassificationResearch_ru.ipynb
```