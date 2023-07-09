"""Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов не используя методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.
"""

worlds = [b'class', b'function', b'method']

for i in worlds:
    print(f"{type(i)} {i} {len(i)}")
