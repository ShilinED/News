from django import template

register = template.Library()

# Список слов, которые будут цензурироваться
censura = ['содомит', 'урнинг']

# Декоратор, который регистрирует функцию как фильтр шаблона
@register.filter()
# Определение функции фильтра
def censor(word):
   # Проверяем, является ли входное слово строкой
   if isinstance(word, str):
      # Итерируем по списку слов для цензуры
      for i in censura:
         # Заменяем все вхождения цензурируемого слова, кроме первой буквы, на звездочки
         word = word.replace(i[1:], '*' * len(i[1:]))
   else:
       # Если входное значение не строка, выбрасываем исключение
       raise ValueError(
          'custom_filters -> censor -> A string is expected, but a different data type has been entered')
   # Возвращаем отфильтрованное слово
   return word
