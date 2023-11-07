'''
Author:fengling
time:2023/10/
'''


# 自定义异常

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name
