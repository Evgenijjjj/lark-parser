# Инструкция

Python 3.8
MacOS 11.0.1

1. ```python -m venv env```
2. ```. ./env/bin/activate```
3. ```pip install -r libs.txt```
4. Установить graphviz. Для brew: ```brew install graphviz```
5. Написать код в <input_file_name>.txt
6. ```python parser.py <input_file_name>.txt <output_file_name>.png```
7. Результат выполнения: абстрактное синтаксическое дерево находится в файле <output_file_name>.png
