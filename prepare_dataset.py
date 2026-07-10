import json, os, random, itertools

random.seed(42)

data = []

# ═══════ Пул примеров ═══════

# 1. PYTHON BASICS
python_basics = [
    {"q": "Как вывести текст в Python?", "a": "```python\nprint('Привет, мир!')\n```\nФункция `print()` выводит текст в консоль."},
    {"q": "Как объявить переменную?", "a": "```python\nname = 'Анна'\nage = 25\nis_student = True\n```\nТип определяется автоматически. Имена — snake_case."},
    {"q": "Какие типы данных есть в Python?", "a": "Основные: `int`, `float`, `str`, `bool`, `list`, `dict`, `tuple`, `set`, `NoneType`.\n\n```python\na = 42          # int\nb = 3.14        # float\nc = 'текст'     # str\nd = [1, 2, 3]   # list\ne = {'key': 1}  # dict\n```"},
    {"q": "Как сделать список?", "a": "```python\n# Пустой\nmy_list = []\nmy_list = list()\n\n# С элементами\nfruits = ['яблоко', 'банан', 'вишня']\nnumbers = list(range(10))\n```\nСписки изменяемы, индексация с 0."},
    {"q": "Как работает срез? list[1:3] что делает?", "a": "Срез возвращает подсписок:\n```python\na = [0, 1, 2, 3, 4]\na[1:3]    # [1, 2] — с 1 по 2 (3 не вкл)\na[:3]     # [0, 1, 2] — первые 3\na[2:]     # [2, 3, 4] — с 2 до конца\na[::2]    # [0, 2, 4] — каждый второй\na[::-1]   # [4, 3, 2, 1, 0] — reverse\n```\nФормат: `[start:stop:step]`."},
    {"q": "Как проверить, есть ли элемент в списке?", "a": "```python\nfruits = ['яблоко', 'банан', 'вишня']\nif 'банан' in fruits:\n    print('Есть!')\n\n# Индекс элемента\nidx = fruits.index('банан')\n```\nОператор `in` работает для любых коллекций."},
]

# 2. PYTHON FUNCTIONS
python_funcs = [
    {"q": "Как написать функцию?", "a": "```python\ndef greet(name):\n    return f'Привет, {name}!'\n\nprint(greet('Анна'))  # Привет, Анна!\n```\n`def` — определение, `return` — возвращает значение."},
    {"q": "Что такое *args и **kwargs?", "a": "```python\ndef func(*args, **kwargs):\n    # args — кортеж позиционных аргументов\n    # kwargs — словарь именованных\n    print(args)   # (1, 2, 3)\n    print(kwargs) # {'a': 4, 'b': 5}\n\nfunc(1, 2, 3, a=4, b=5)\n```\nПозволяет передавать любое количество аргументов."},
    {"q": "Как вернуть несколько значений?", "a": "```python\ndef get_stats(numbers):\n    return min(numbers), max(numbers), sum(numbers)/len(numbers)\n\nmn, mx, avg = get_stats([1, 2, 3, 4, 5])\n```\nФункция возвращает кортеж, который распаковывается."},
    {"q": "Что такое lambda?", "a": "Анонимная функция в одну строку:\n```python\nsquare = lambda x: x**2\nprint(square(5))  # 25\n\n# Часто с filter/map/sorted\nsorted(pairs, key=lambda x: x[1])\n```\nИспользуется для простых операций."},
    {"q": "Как сделать рекурсию?", "a": "```python\ndef factorial(n):\n    if n <= 1: return 1\n    return n * factorial(n - 1)\n\nprint(factorial(5))  # 120\n```\nВажно: базовый случай (условие выхода) и рекурсивный шаг."},
]

# 3. PYTHON OOP
python_oop = [
    {"q": "Как создать класс?", "a": "```python\nclass Dog:\n    def __init__(self, name):\n        self.name = name\n    \n    def bark(self):\n        return f'{self.name}: Гав!'\n\ndog = Dog('Бобик')\nprint(dog.bark())\n```\n`__init__` — конструктор, `self` — ссылка на экземпляр."},
    {"q": "Что такое наследование?", "a": "```python\nclass Animal:\n    def __init__(self, name):\n        self.name = name\n\nclass Dog(Animal):\n    def bark(self):\n        return f'{self.name}: Гав!'\n```\nДочерний класс получает всё от родительского."},
    {"q": "Как работает super()?", "a": "`super()` вызывает метод родительского класса:\n```python\nclass Child(Parent):\n    def __init__(self, x, y):\n        super().__init__(x)  # вызов Parent.__init__\n        self.y = y\n```\nПолезно при расширении родительских методов."},
    {"q": "Что такое декоратор?", "a": "Функция, оборачивающая другую функцию:\n```python\ndef timer(func):\n    def wrapper(*args, **kwargs):\n        start = time.time()\n        result = func(*args, **kwargs)\n        print(f'{time.time()-start:.2f}s')\n        return result\n    return wrapper\n\n@timer\ndef slow_func():\n    sleep(1)\n```\n`@timer` — синтаксический сахар для `slow_func = timer(slow_func)`."},
    {"q": "Что такое property?", "a": "Декоратор для геттеров/сеттеров:\n```python\nclass Person:\n    @property\n    def full_name(self):\n        return f'{self.first} {self.last}'\n    \n    @full_name.setter\n    def full_name(self, value):\n        self.first, self.last = value.split()\n```\nПозволяет обращаться как к атрибуту, а не методу."},
]

# 4. JAVASCRIPT BASICS
js_basics = [
    {"q": "Как объявить переменную в JS?", "a": "```javascript\nlet name = 'Анна';    // изменяемая\nconst age = 25;       // константа\nvar old = 'не юзай';  // устаревший способ\n```\n`let` и `const` — блочная область видимости."},
    {"q": "Какие типы в JavaScript?", "a": "Примитивы: `string`, `number`, `boolean`, `null`, `undefined`, `symbol`, `bigint`.\nСсылочные: `object`, `array`, `function`.\n\n```javascript\ntypeof 42        // 'number'\ntypeof 'text'    // 'string'\ntypeof []        // 'object'\ntypeof null      // 'object' (исторический баг)\n```"},
    {"q": "Как работают стрелочные функции?", "a": "```javascript\n// Обычная\nfunction add(a, b) { return a + b; }\n\n// Стрелочная\nconst add = (a, b) => a + b;\nconst square = x => x ** 2;\nconst log = () => console.log('hi');\n```\nСтрелочные не имеют своего `this`."},
    {"q": "Как сделать условный оператор?", "a": "```javascript\nif (age >= 18) {\n    console.log('Взрослый');\n} else if (age >= 12) {\n    console.log('Подросток');\n} else {\n    console.log('Ребёнок');\n}\n\n// Тернарный\nconst status = age >= 18 ? 'Взрослый' : 'Ребёнок';\n```"},
    {"q": "Как работает && и ||?", "a": "```javascript\n// && — возвращает первое falsy или последнее\n'hi' && 0 && 'bye'  // 0\n'hi' && 42         // 42\n\n// || — возвращает первое truthy или последнее\nnull || 0 || 'hi'  // 'hi'\nnull || 42         // 42\n\n// ?? — только для null/undefined\nnull ?? 'default'  // 'default'\n0 ?? 'default'     // 0\n```"},
]

# 5. JAVASCRIPT ARRAYS
js_arrays = [
    {"q": "Как добавить элемент в массив?", "a": "```javascript\nconst arr = [1, 2, 3];\narr.push(4);      // [1, 2, 3, 4] — в конец\narr.unshift(0);   // [0, 1, 2, 3, 4] — в начало\n\n// Иммутабельно:\nconst b = [...arr, 5];\n```"},
    {"q": "Как работает map()?", "a": "```javascript\nconst nums = [1, 2, 3];\nconst doubled = nums.map(x => x * 2);\n// [2, 4, 6]\n\nconst users = [{name: 'Анна'}, {name: 'Иван'}];\nconst names = users.map(u => u.name);\n// ['Анна', 'Иван']\n```\nСоздаёт новый массив, применяя функцию к каждому элементу."},
    {"q": "Разница filter и find?", "a": "- `filter` — возвращает ВСЕ подходящие элементы (массив)\n- `find` — возвращает ПЕРВЫЙ подходящий или undefined\n\n```javascript\nconst nums = [1, 2, 3, 4, 5];\nnums.filter(x => x > 3) // [4, 5]\nnums.find(x => x > 3)   // 4\n```"},
    {"q": "Как работает reduce()?", "a": "Сворачивает массив в одно значение:\n```javascript\nconst sum = [1, 2, 3].reduce((acc, x) => acc + x, 0);\n// 6\n\nconst max = [1, 5, 2, 9].reduce((a, b) => a > b ? a : b);\n// 9\n\n// Группировка\nconst grouped = items.reduce((acc, item) => {\n  (acc[item.type] ||= []).push(item);\n  return acc;\n}, {});\n```"},
]

# 6. REACT
react_examples = [
    {"q": "Как создать компонент в React?", "a": "```jsx\nfunction MyComponent({ name }) {\n  return <div>Привет, {name}!</div>;\n}\n\n// Использование\n<MyComponent name=\"Анна\" />\n```\nКомпонент — функция, возвращающая JSX."},
    {"q": "Как использовать useState?", "a": "```jsx\nimport { useState } from 'react';\n\nfunction Counter() {\n  const [count, setCount] = useState(0);\n  \n  return (\n    <button onClick={() => setCount(c => c + 1)}>\n      {count}\n    </button>\n  );\n}\n```\n`useState` возвращает пару [значение, функция-сеттер]."},
    {"q": "Как передать данные из родителя в ребёнка?", "a": "```jsx\nfunction Parent() {\n  const [data, setData] = useState('привет');\n  return <Child message={data} />;\n}\n\nfunction Child({ message }) {\n  return <div>{message}</div>;\n}\n```\nДанные передаются через props (атрибуты JSX)."},
    {"q": "Что такое JSX?", "a": "Синтаксическое расширение JavaScript для React:\n```jsx\nconst element = (\n  <div className=\"container\">\n    <h1>Заголовок</h1>\n    {items.map(item => <p key={item.id}>{item.text}</p>)}\n  </div>\n);\n```\nJSX компилируется в `React.createElement()`."},
    {"q": "Как обработать форму в React?", "a": "```jsx\nfunction LoginForm() {\n  const [email, setEmail] = useState('');\n  const handleSubmit = (e) => {\n    e.preventDefault();\n    console.log(email);\n  };\n  \n  return (\n    <form onSubmit={handleSubmit}>\n      <input value={email} \n             onChange={e => setEmail(e.target.value)} />\n      <button type=\"submit\">Войти</button>\n    </form>\n  );\n}\n```\nКонтролируемые компоненты — value + onChange."},
]

# 7. GIT
git_examples = [
    {"q": "Как создать репозиторий Git?", "a": "```bash\ngit init                    # новый репозиторий\ngit clone <url>             # скопировать существующий\ngit remote add origin <url> # привязать удалённый\n```"},
    {"q": "Как сделать коммит?", "a": "```bash\ngit add .           # добавить все файлы\ngit commit -m \"fix: исправил баг\"  # создать коммит\n\n# Или коротко:\ngit commit -am \"fix: исправил баг\"\n```\nХорошие коммиты: глагол + краткое описание."},
    {"q": "Как создать ветку?", "a": "```bash\ngit branch feature     # создать ветку\ngit checkout feature   # переключиться\ngit checkout -b feature  # создать + переключиться\n\n# Современный способ:\ngit switch -c feature\n```"},
    {"q": "Как объединить ветки?", "a": "```bash\n# Сначала переключиться в целевую ветку\ngit switch main\ngit merge feature\n\n# Если конфликт:\n# 1. Исправить конфликтные файлы\n# 2. git add .\n# 3. git commit\n```"},
    {"q": "Как откатить изменения?", "a": "```bash\ngit restore file.txt           # отменить изменения в файле\ngit reset HEAD~1 --soft        # отменить коммит, оставить изменения\ngit reset HEAD~1 --hard        # отменить коммит, удалить изменения\ngit revert HEAD                # создать новый коммит, отменяющий изменения\n```"},
]

# 8. ALGORITHMS
algo_examples = [
    {"q": "Что такое временная сложность O(n)?", "a": "**O(n)** — линейная сложность. Время растёт пропорционально размеру данных.\n\n```python\n# O(n) — один проход\nfor x in arr:\n    print(x)\n\n# O(n²) — вложенные циклы\nfor x in arr:\n    for y in arr:\n        print(x, y)\n```\nИгнорируем константы: O(2n) = O(n)."},
    {"q": "Напиши сортировку пузырьком", "a": "```python\ndef bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        swapped = False\n        for j in range(n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n                swapped = True\n        if not swapped: break\n    return arr\n```\nСложность: O(n²). Простая, но медленная."},
    {"q": "Что такое стек?", "a": "Структура данных LIFO (Last In, First Out):\n```python\nstack = []\nstack.append(1)  # push\nstack.append(2)\nstack.pop()      # 2 — удаляем последний\n```\nКак стопка тарелок: последнюю положил — первую берёшь."},
    {"q": "Что такое очередь?", "a": "Структура FIFO (First In, First Out):\n```python\nfrom collections import deque\n\nqueue = deque()\nqueue.append(1)    # enqueue\nqueue.append(2)\nqueue.popleft()    # 1 — удаляем первый\n```\nКак очередь в магазине: первый пришёл — первый ушёл."},
    {"q": "Как развернуть строку?", "a": "```python\n# Python\ns[::-1]  # 'привет' -> 'тевирп'\n\n# JavaScript\ns.split('').reverse().join('')\n\n# Ручная\nresult = ''\nfor ch in s:\n    result = ch + result\n```"},
]

# 9. HTML/CSS
html_css = [
    {"q": "Как сделать адаптивную вёрстку?", "a": "```css\n/* Mobile-first */\n.container {\n    display: grid;\n    grid-template-columns: 1fr;\n}\n\n@media (min-width: 768px) {\n    .container {\n        grid-template-columns: repeat(2, 1fr);\n    }\n}\n\n@media (min-width: 1024px) {\n    .container {\n        grid-template-columns: repeat(3, 1fr);\n    }\n}\n```\nНачинай с мобильной версии, добавляй breakpoints для больших экранов."},
    {"q": "Что такое flexbox?", "a": "Одномерная раскладка CSS:\n```css\n.container {\n    display: flex;\n    justify-content: space-between;  /* по главной оси */\n    align-items: center;            /* по поперечной */\n    gap: 16px;\n}\n\n.item {\n    flex: 1;  /* все элементы равной ширины */\n}\n```\nУдобно для навигации, карточек, центрирования."},
]

# 10. LINUX/TERMUX
linux_examples = [
    {"q": "Как посмотреть список файлов?", "a": "```bash\nls                  # простой список\nls -la              # подробный, включая скрытые\nls -lh              # с размерами (human readable)\nls *.py             # только .py файлы\n```"},
    {"q": "Как посмотреть содержимое файла?", "a": "```bash\ncat file.txt        # весь файл\nless file.txt       # постранично (q — выход)\nhead -10 file.txt   # первые 10 строк\ntail -20 file.txt   # последние 20 строк\ntail -f log.txt     # следить за изменениями\n```"},
    {"q": "Как найти файл?", "a": "```bash\nfind . -name \"*.py\"              # по имени\nfind . -type f -size +10M         # файлы больше 10MB\ngrep -r \"search\" .               # поиск текста\nlocate file.txt                   # быстрый поиск (но need updatedb)\n```"},
    {"q": "Как дать права на файл?", "a": "```bash\nchmod +x script.sh      # сделать исполняемым\nchmod 755 script.sh     # rwxr-xr-x (владелец: всё, группа: rx, все: rx)\nchmod 600 secret.txt    # rw------- (только владелец)\nchown user:group file   # сменить владельца\n```"},
    {"q": "Как посмотреть процессы?", "a": "```bash\nps aux                  # все процессы\nps aux | grep python    # фильтр по python\ntop                     # в реальном времени (q — выход)\nhtop                    # улучшенный top\nkill -9 PID             # убить процесс по PID\n```"},
]

# 11. SQL
sql_examples = [
    {"q": "Как сделать SQL запрос?", "a": "```sql\nSELECT * FROM users;\nSELECT name, email FROM users WHERE age > 18;\nSELECT COUNT(*) FROM orders WHERE status = 'pending';\n```\n`SELECT` — выборка, `FROM` — таблица, `WHERE` — фильтр."},
    {"q": "Как объединить две таблицы?", "a": "```sql\nSELECT u.name, o.total\nFROM users u\nJOIN orders o ON u.id = o.user_id\nWHERE o.total > 100;\n\n-- LEFT JOIN — все пользователи, даже без заказов\nLEFT JOIN orders o ON u.id = o.user_id\n```\n`JOIN` соединяет строки по условию."},
    {"q": "Как вставить данные?", "a": "```sql\nINSERT INTO users (name, email) \nVALUES ('Иван', 'ivan@mail.com');\n\n-- Несколько строк\nINSERT INTO users (name, email) VALUES\n    ('Анна', 'anna@mail.com'),\n    ('Пётр', 'petr@mail.com');\n```"},
]

# ALL CATEGORIES
categories = [
    ("Python Основы", python_basics),
    ("Python Функции", python_funcs),
    ("Python ООП", python_oop),
    ("JavaScript Основы", js_basics),
    ("JavaScript Массивы", js_arrays),
    ("React", react_examples),
    ("Git", git_examples),
    ("Алгоритмы", algo_examples),
    ("HTML/CSS", html_css),
    ("Linux/Termux", linux_examples),
    ("SQL", sql_examples),
]

# ═══════ ГЕНЕРАЦИЯ ═══════

# Вариации вопросов
question_templates = [
    "{}",
    "Объясни, {}",
    "Расскажи про {}",
    "Как работает {}",
    "{} — что это?",
    "Как использовать {}",
    "{} пример кода",
    "Подробно: {}",
    "Для чего нужно {}",
    "Объясни простыми словами: {}",
    "{} как это работает?",
    "Расскажи подробно про {}",
    "В чём суть {}",
    "{} объясни с примерами",
]

extra_variations = [
    " с примерами",
    " на русском",
    " для начинающих",
    " понятным языком",
]

for cat_name, items in categories:
    for item in items:
        base_q = item["q"].rstrip("?")
        
        # Добавляем оригинал
        data.append({
            "instruction": item["q"],
            "input": "",
            "output": item["a"]
        })
        
        # Вариации вопроса
        for tmpl in random.sample(question_templates, min(5, len(question_templates))):
            q_variant = tmpl.format(base_q.lower())
            if q_variant != item["q"]:
                data.append({
                    "instruction": q_variant,
                    "input": "",
                    "output": item["a"]
                })
        
        # Вариации с уточнениями
        for suffix in extra_variations:
            data.append({
                "instruction": base_q + suffix + "?",
                "input": "",
                "output": item["a"]
            })

# Add combined questions (if we have 2+ items, create combos)
for cat_name, items in categories:
    if len(items) >= 2:
        combo = random.sample(items, 2)
        q1 = combo[0]["q"].rstrip("?").lower()
        q2 = combo[1]["q"].rstrip("?").lower()
        data.append({
            "instruction": f"Объясни разницу между {q1} и {q2}",
            "input": "",
            "output": f"**{combo[0]['q']}**:\n{combo[0]['a']}\n\n**{combo[1]['q']}**:\n{combo[1]['a']}"
        })

# Удаляем дубликаты
seen = set()
unique_data = []
for item in data:
    key = item["instruction"]
    if key not in seen:
        seen.add(key)
        unique_data.append(item)

random.shuffle(unique_data)

# Сохраняем
os.makedirs("training_data", exist_ok=True)
with open("training_data/code_tutor_dataset.json", "w", encoding="utf-8") as f:
    json.dump(unique_data, f, ensure_ascii=False, indent=2)

print(f"✅ Создано {len(unique_data)} уникальных примеров")
print(f"📁 Файл: training_data/code_tutor_dataset.json")
print(f"📦 Размер: {os.path.getsize('training_data/code_tutor_dataset.json')} байт")
