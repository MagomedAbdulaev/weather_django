Из всего выше перечисленного сделано всё, кроме докер контейнера, также был вопрос по поводу этого пунката: будет сохраняться история поиска для каждого пользователя, и будет API, показывающее сколько раз вводили какой город .
Регистрацию/авторизацию делать не нужно было, но показывать историю поиска каждого пользователя нужно, поэтому я использовал сессии, которые сохраняют для каждого пользователя свои значения(у каждого свое),
я написал функцию представления и она возвращает шаблон, можно было сделать вместо render JsonResponse, ибо это api, но я решил для читаемости рендерить шаблон html. Я не использовал никакие сторонние бд, только SQLite.
Также у меня был список всех городов в json формате файлом, оттуда и брались подсказки. Для обращения к api погоды я использовал requests. Сам проект запускается обычной командой python manage.py runserver  

