import json
from json import JSONDecodeError
from pprint import pprint as pp

from classes.exceptions import BadDataSource


class DataBase:
    POST_PATH = "/data/posts.json"

    def __init__(self, path):
        self.path = path

    def load_date(self):
        """Загружает данные из файла"""
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except(FileNotFoundError, JSONDecodeError):
            raise BadDataSource("JSON поврежден")

        return data

    def _save_data(self, data):
        """Перезаписываем переданные данные в файл"""
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def get_all(self):
        """ Отдаем полный список данных"""
        data = self.load_date()
        return data

    def search(self, substring):
        """Отдает посты"""
        posts = self.load_date()
        substring = substring.lower()
        search_posts = [post for post in posts if substring in post["content"].lower()]
        return search_posts

    def add(self, post):
        """Добавляет в хранилище постов новый пост"""
        #if type(post) != dict:
            #raise TypeError("Пост не может быть добавлен")
        posts = self.get_all()
        posts.append(post)
        self._save_data(posts)


#db = DataBase("../test/mosk_posts.json")
#post = {"pic": "...", "content": "...."}

#POST_PATH = "/data/posts.json"
#pp(db.add(post))
