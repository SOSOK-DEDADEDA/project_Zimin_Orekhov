# dataset.py - Расширенный датасет для чат-бота
# Содержит все вопросы, ответы и вариации для обучения

import json
import re
from pathlib import Path

class GodotDataset:
    """Класс для управления датасетом вопросов-ответов по Godot"""
    
    def __init__(self):
        self.questions_ru = []
        self.answers_ru = []
        self.questions_en = []
        self.answers_en = []
        self.categories = []
        
        # Карта категорий (для быстрого доступа)
        self.category_map = {
            "регистрация": "Регистрация и вход",
            "аккаунт": "Аккаунт пользователя",
            "обучение": "Начало обучения",
            "уроки": "Структура курса",
            "тесты": "Прохождение тестов",
            "материалы": "Дополнительные материалы",
            "поддержка": "Техническая поддержка",
            "сертификат": "Сертификация",
            "прогресс": "Прогресс обучения",
            "установка": "Установка и настройка",
            "движение": "Движение персонажа",
            "анимация": "Анимация спрайтов",
            "физика": "Физика и гравитация",
            "коллизии": "Коллизии и столкновения",
            "скриптинг": "Скрипты и GDScript",
            "платформы": "Платформы и препятствия",
            "сигналы": "Сигналы и события",
            "враги": "Враги и AI",
            "сохранение": "Сохранение прогресса",
            "камера": "Камера и слежение",
            "звуки": "Звуки и музыка",
            "оптимизация": "Оптимизация игры",
            "экспорт": "Экспорт и публикация",
            "интерфейс": "Пользовательский интерфейс",
            "документация": "Документация и ресурсы"
        }
        
    def create_basic_dataset(self):
        """Создание базового датасета о сайте и курсе"""
        
        # Базовые русские вопросы
        ru_basic = [
            ("Как зарегистрироваться на сайте?", 
             "Для регистрации нажмите кнопку 'Записаться на курс' на главной странице. Заполните форму с именем пользователя и паролем. После регистрации вы автоматически войдете в систему.", 
             "регистрация"),
             
            ("Как войти в личный кабинет?", 
             "Нажмите кнопку 'Вход' в правом верхнем углу. Введите имя пользователя и пароль.", 
             "аккаунт"),
             
            ("Как начать обучение?", 
             "После входа перейдите на главную страницу и выберите любой урок. Рекомендуется начинать с первого урока.", 
             "обучение"),
             
            ("Сколько всего уроков в курсе?", 
             "Курс включает 12 уроков. Сейчас доступны первые 3 урока, остальные будут добавляться.", 
             "уроки"),
             
            ("Как пройти тест?", 
             "В конце урока нажмите 'Пройти тест' и ответьте на вопросы текстом.", 
             "тесты"),
             
            ("Где скачать материалы к уроку?", 
             "Материалы находятся в разделе 'Дополнительные материалы' внутри каждого урока.", 
             "материалы"),
             
            ("Как связаться с поддержкой?", 
             "Напишите на support@godot-learning.ru. Мы отвечаем в течение 24 часов.", 
             "поддержка"),
             
            ("Что делать если забыл пароль?", 
             "Напишите на support@godot-learning.ru с указанием вашего имени пользователя.", 
             "аккаунт"),
             
            ("Какой движок Godot используется?", 
             "Курс использует Godot 4.x. Скачать можно с godotengine.org", 
             "документация"),
             
            ("Нужно ли платить за курс?", 
             "Курс полностью бесплатный. Все материалы доступны без оплаты.", 
             "обучение"),
             
            ("Выдаете ли вы сертификаты?", 
             "Да, после прохождения всех 12 уроков вы получите сертификат.", 
             "сертификат"),
             
            ("Как отслеживать прогресс?", 
             "На главной странице под каждым уроком отображается процент прогресса.", 
             "прогресс"),
        ]
        
        # Базовые английские вопросы
        en_basic = [
            ("How to register on the site?", 
             "Click 'Sign up' in the top right corner. Fill in username and password. After registration you'll be automatically logged in.", 
             "registration"),
             
            ("How to login?", 
             "Click the 'Login' button in the top right corner. Enter your username and password.", 
             "account"),
             
            ("How to start learning?", 
             "After login, go to the main page and choose any lesson. It's recommended to start from lesson 1.", 
             "learning"),
             
            ("How many lessons are there?", 
             "The course includes 12 lessons. First 3 lessons are available now.", 
             "lessons"),
             
            ("How to take a quiz?", 
             "At the end of each lesson click 'Take Quiz' and answer the questions with text.", 
             "quizzes"),
             
            ("Where to download materials?", 
             "Materials are in the 'Additional Materials' section inside each lesson.", 
             "materials"),
             
            ("How to contact support?", 
             "Email us at support@godot-learning.ru. We reply within 24 hours.", 
             "support"),
             
            ("Forgot password?", 
             "Email support@godot-learning.ru with your username.", 
             "account"),
             
            ("Which Godot version is used?", 
             "The course uses Godot 4.x. Download from godotengine.org", 
             "documentation"),
             
            ("Is the course free?", 
             "Yes, the course is completely free.", 
             "learning"),
             
            ("Do you provide certificates?", 
             "Yes, after completing all 12 lessons you will receive a certificate.", 
             "certificate"),
        ]
        
        for q, a, c in ru_basic:
            self.questions_ru.append(q)
            self.answers_ru.append(a)
            if c not in self.categories:
                self.categories.append(c)
        
        for q, a, c in en_basic:
            self.questions_en.append(q)
            self.answers_en.append(a)
            if c not in self.categories:
                self.categories.append(c)
        
        return self
    
    def create_godot_extended_dataset(self):
        """Создание расширенного датасета по Godot (12 уроков)"""
        
        # ==================== УРОК 1: УСТАНОВКА ====================
        lesson1_ru = [
            ("Мой ребенок не может пройти первый урок, не создается файл проекта, что делать?", 
             "Проверьте: 1) Права на запись в папке Documents 2) Запустите Godot от имени администратора 3) На диске достаточно места (минимум 500 МБ) 4) Путь к проекту не содержит русских букв и пробелов.", 
             "установка"),
             
            ("Godot не запускается после установки, выдает ошибку Vulkan", 
             "Запустите Godot с флагом --rendering-driver opengl3. Для этого создайте ярлык и в свойствах добавьте этот параметр. Или установите последние драйверы видеокарты.", 
             "установка"),
             
            ("Не могу найти кнопку 'Новый проект' в Godot", 
             "Кнопка 'New Project' находится на стартовом экране Godot. Если вы уже в редакторе, нажмите Project → New Project в верхнем меню.", 
             "интерфейс"),
             
            ("При создании проекта ошибка 'Invalid project path'", 
             "Путь к проекту не должен содержать русские буквы, пробелы и специальные символы. Используйте только латиницу, цифры и знак подчеркивания. Пример: C:/GodotProjects/MyGame", 
             "установка"),
             
            ("Godot зависает при открытии большого проекта", 
             "Попробуйте: 1) Закрыть другие программы 2) Уменьшить качество в настройках редактора 3) Отключить предпросмотр в панели FileSystem 4) Увеличить выделенную память в настройках.", 
             "оптимизация"),
        ]
        
        # ==================== УРОК 2: ДВИЖЕНИЕ ПЕРСОНАЖА ====================
        lesson2_ru = [
            ("У ребенка персонаж не двигается при нажатии клавиш, в чем проблема?", 
             "Пошаговая проверка:\n1) Добавлен ли узел CharacterBody2D?\n2) Есть ли скрипт на персонаже?\n3) Настроены ли входные действия в Project Settings → Input Map?\n4) Правильно ли указаны названия действий в коде?\n5) Вызывается ли move_and_slide() в конце _physics_process?", 
             "движение"),
             
            ("Ошибка 'Identifier not found: move_and_slide' в Godot", 
             "Убедитесь, что ваш узел наследуется от CharacterBody2D или RigidBody2D. Узел Node2D не имеет метода move_and_slide(). Проверьте extends в начале скрипта.", 
             "скриптинг"),
             
            ("Персонаж падает слишком медленно, как настроить гравитацию?", 
             "Измените значение переменной gravity. Типичное значение для платформера — 980. Добавьте в код:\nvar gravity = 980\n\nfunc _physics_process(delta):\n    velocity.y += gravity * delta\n    move_and_slide()", 
             "физика"),
             
            ("Персонаж проходит сквозь стены, как исправить?", 
             "Проблема в коллизиях. Проверьте:\n1) Добавлен ли CollisionShape2D к персонажу?\n2) Есть ли форма коллизии (RectangleShape2D/CircleShape2D)?\n3) У стен есть StaticBody2D с CollisionShape2D?\n4) Вызывается ли move_and_slide() после изменения velocity?", 
             "коллизии"),
             
            ("Как сделать двойной прыжок в платформере?", 
             "Добавьте переменную jumps_left:\nvar jumps_left = 2\n\nfunc _physics_process(delta):\n    if Input.is_action_just_pressed('jump'):\n        if is_on_floor():\n            jumps_left = 2\n            velocity.y = jump_velocity\n        elif jumps_left > 0:\n            jumps_left -= 1\n            velocity.y = jump_velocity", 
             "физика"),
             
            ("Как сделать персонажа, который бежит быстрее при удержании Shift?", 
             "Добавьте проверку на удержание Shift:\nvar speed = 300\nvar sprint_speed = 600\n\nfunc _physics_process(delta):\n    var current_speed = sprint_speed if Input.is_action_pressed('sprint') else speed", 
             "движение"),
        ]
        
        # ==================== УРОК 3: АНИМАЦИЯ ====================
        lesson3_ru = [
            ("Анимация не проигрывается в Godot, что делать?", 
             "Проверьте:\n1) Включен ли авто-воспроизведение (Autoplay on Load) в AnimationPlayer?\n2) Вызвали ли $AnimationPlayer.play('имя_анимации') в коде?\n3) Есть ли ключевые кадры в анимации?\n4) Правильно ли указано имя анимации (регистр важен).", 
             "анимация"),
             
            ("Спрайты для анимации дергаются, как это исправить?", 
             "Проблемы:\n1) Убедитесь, что все спрайты в анимации имеют одинаковый размер\n2) Используйте AnimatedSprite2D вместо AnimationPlayer для простых анимаций\n3) Настройте скорость анимации в FPS (обычно 12-24 кадра в секунду)\n4) Проверьте pivot/offset каждого кадра", 
             "анимация"),
             
            ("Как сделать анимацию бега и прыжка с переключением?", 
             "Создайте анимации в AnimationPlayer: 'idle', 'run', 'jump', 'fall'. В скрипте:\nif not is_on_floor():\n    if velocity.y > 0:\n        play('fall')\n    else:\n        play('jump')\nelif direction != 0:\n    play('run')\nelse:\n    play('idle')", 
             "анимация"),
             
            ("Где брать спрайты для игры? Как их добавить в Godot?", 
             "Источники спрайтов:\n1) Нарисовать в Paint, GIMP или Krita\n2) Скачать с OpenGameArt.org (бесплатно)\n3) Использовать сайт itch.io (много бесплатных ассетов)\n\nКак добавить: перетащите PNG файл в панель FileSystem, затем перетащите на сцену или создайте Sprite2D и выберите текстуру.", 
             "ресурсы"),
             
            ("Как сделать анимацию входа/выхода персонажа на сцену?", 
             "Создайте анимацию 'enter' или 'exit' в AnimationPlayer. В ней измените позицию или масштаб. Затем в коде дождитесь окончания анимации:\n$AnimationPlayer.play('enter')\nawait $AnimationPlayer.animation_finished", 
             "анимация"),
        ]
        
        # ==================== УРОК 4: ФИЗИКА ====================
        lesson4_ru = [
            ("Персонаж прыгает один раз, а потом не может прыгнуть снова", 
             "Проблема в том, что is_on_floor() не работает из-за коллизий. Проверьте:\n1) Добавлен ли CollisionShape2D с правильной формой\n2) Вызывается ли move_and_slide() после изменения velocity.y\n3) Не заблокирована ли коллизия в слоях (collision layers)\n4) Добавлен ли персонажу CollisionShape2D в виде прямоугольника", 
             "физика"),
             
            ("Как добавить движущиеся платформы?", 
             "Способ 1: Перемещайте StaticBody2D через AnimationPlayer (создайте анимацию движения туда-сюда)\nСпособ 2: Используйте Path2D и PathFollow2D для сложных траекторий\nСпособ 3: В скрипте платформы используйте _process(delta) для изменения позиции", 
             "платформы"),
             
            ("Персонаж слишком скользкий на платформах, как уменьшить трение?", 
             "Проблема в том, что move_and_slide() сохраняет горизонтальную скорость. Добавьте торможение:\nif is_on_floor():\n    velocity.x = lerp(velocity.x, direction * speed, 0.2)\nelse:\n    velocity.x = lerp(velocity.x, direction * speed, 0.05)\n\nИли используйте переменную friction = 0.8 на земле", 
             "физика"),
             
            ("Как сделать платформы, которые разрушаются после прыжка?", 
             "Создайте платформу с Area2D. При сигнале body_entered проверьте, что это персонаж и он сверху (velocity.y > 0). Затем запустите анимацию разрушения и удалите через таймер.\n\nfunc on_body_entered(body):\n    if body.name == 'Player' and body.velocity.y > 0:\n        $AnimationPlayer.play('break')\n        await $AnimationPlayer.animation_finished\n        queue_free()", 
             "платформы"),
        ]
        
        # ==================== УРОК 5: СБОР ПРЕДМЕТОВ ====================
        lesson5_ru = [
            ("Предметы не собираются при касании, хотя есть Area2D", 
             "Проверьте:\n1) У предмета есть узел Area2D с CollisionShape2D\n2) На персонаже есть CollisionShape2D\n3) Подключен сигнал body_entered к скрипту\n4) В функции обработки есть queue_free()\n5) Правильно настроены collision layers и masks", 
             "сигналы"),
             
            ("Как отображать счет на экране? Как обновлять его при сборе монет?", 
             "Шаги:\n1) Создайте Label в интерфейсе\n2) В глобальном скрипте (Autoload) объявите var score = 0\n3) При сборе монеты: Global.score += 1\n4) Обновляйте текст Label: $Label.text = 'Счет: ' + str(Global.score)\n\nДля создания Autoload: Создайте скрипт и добавьте в Project Settings → Autoload", 
             "интерфейс"),
             
            ("Как добавить звук сбора монеты?", 
             "1) Добавьте к монете узел AudioStreamPlayer2D\n2) Загрузите звуковой файл в свойство Stream\n3) В функции сбора монеты вызовите $AudioStreamPlayer2D.play()\n4) После этого можно вызвать queue_free() или использовать await для задержки\n\nСовет: Используйте звуки в формате .ogg для лучшей производительности", 
             "звуки"),
             
            ("Как сделать таймер обратного отсчета для уровня?", 
             "1) Добавьте узел Timer\n2) В настройках установите Wait Time (например, 60 секунд)\n3) Включите One Shot\n4) В скрипте:\n   $Timer.start()\n   $Timer.timeout.connect(_on_timeout)\n5) В _on_timeout() покажите сообщение о поражении и перезапустите уровень", 
             "интерфейс"),
        ]
        
        # ==================== УРОК 6: ВРАГИ ====================
        lesson6_ru = [
            ("При касании врага персонаж умирает, но и враг исчезает. Как сделать, чтобы враг оставался?", 
             "Не удаляйте врага в функции столкновения. Вместо этого:\n1) На враге используйте сигнал body_entered\n2) При касании запускайте анимацию смерти персонажа\n3) Перезапускайте уровень через Timer\n\nПример:\nfunc _on_enemy_body_entered(body):\n    if body.name == 'Player':\n        body.die()\n        # враг НЕ удаляется", 
             "враги"),
             
            ("Как сделать врага, который ходит по платформе туда-обратно?", 
             "Создайте скрипт для врага:\nvar direction = 1\nvar speed = 50\n\nfunc _physics_process(delta):\n    position.x += direction * speed * delta\n    \n    # Проверка края платформы\n    if not $RayCast2D.is_colliding():\n        direction *= -1\n        $RayCast2D.position.x = $RayCast2D.position.x * -1\n    \n    # Проверка стены\n    if $WallRayCast.is_colliding():\n        direction *= -1", 
             "враги"),
             
            ("Как сделать, чтобы персонаж мог прыгать на врагов и убивать их?", 
             "Добавьте на врага две области:\n- Area2D для поражения сверху (small, вверху)\n- Area2D для убийства (вся остальная область)\n\nЕсли касание сверху (velocity.y > 0):\n    враг умирает, персонаж подпрыгивает\nИначе:\n    персонаж получает урон\n\nКод:\nif body.velocity.y > 0:\n    enemy.queue_free()\n    body.velocity.y = -300\nelse:\n    body.die()", 
             "игровая_логика"),
        ]
        
        # ==================== УРОК 7-12 (кратко) ====================
        lesson7_ru = [
            ("Как сохранить прогресс игры и загрузить его?", 
             "Используйте FileAccess для сохранения в файл user://savegame.save\n\nСохранение:\nvar save_data = {'level': 3, 'score': 150}\nvar file = FileAccess.open('user://savegame.save', FileAccess.WRITE)\nfile.store_string(JSON.stringify(save_data))\n\nЗагрузка:\nvar file = FileAccess.open('user://savegame.save', FileAccess.READ)\nvar data = JSON.parse_string(file.get_as_text())", 
             "сохранение"),
        ]
        
        lesson8_ru = [
            ("Как сделать главное меню с кнопками Start, Options и Exit?", 
             "1) Создайте новую сцену с узлом Control\n2) Добавьте кнопки Button через интерфейс\n3) Для каждой кнопки подключите сигнал pressed\n\nКод для Start:\nget_tree().change_scene_to_file('res://level1.tscn')\n\nКод для Exit:\nget_tree().quit()\n\nКод для Options:\n# открыть окно настроек", 
             "интерфейс"),
        ]
        
        lesson9_ru = [
            ("Камера не следует за персонажем, что делать?", 
             "1) Добавьте узел Camera2D как дочерний к персонажу\n2) Установите свойство 'Current' в true\n3) Настройте Smoothing для плавного слежения\n4) Для ограничения движения камеры используйте Limits\n5) Для эффекта параллакса создайте несколько слоев с фоном", 
             "камера"),
        ]
        
        lesson10_ru = [
            ("Музыка в игре не проигрывается, хотя файл добавлен", 
             "Проверьте:\n1) Формат файла (поддерживаются .ogg, .mp3, .wav)\n2) AudioStreamPlayer добавлен на сцену\n3) Для фоновой музыки включите Autoplay и Loop\n4) Проверьте громкость в инспекторе (Volume dB)\n5) Убедитесь, что звук не отключен в системе\n6) Попробуйте переконвертировать файл в .ogg", 
             "звуки"),
        ]
        
        lesson11_ru = [
            ("Игра тормозит на слабом компьютере, что можно сделать?", 
             "Оптимизация:\n1) Уменьшите количество объектов на сцене (объедините статичные объекты)\n2) Используйте низко-полигональные модели для 3D\n3) Включите фрустум камеры (Culling)\n4) Используйте Object pooling для врагов и пуль\n5) Снизьте разрешение текстур\n6) Отключите невидимые узлы через visibility\n7) Используйте меньше физических объектов (StaticBody вместо RigidBody)", 
             "оптимизация"),
        ]
        
        lesson12_ru = [
            ("При экспорте игры в Windows получается файл без иконки", 
             "В настройках экспорта (Project → Export) выберите платформу Windows. В разделе 'Application' укажите путь к ICO файлу в поле 'Icon'. Требования к иконке:\n- Формат .ico\n- Размер 256x256 пикселей\n- 32-битная глубина цвета\n\nМожно создать иконку онлайн на сайте icoconverter.com", 
             "экспорт"),
             
            ("Игра после экспорта не запускается на другом компьютере", 
             "Возможные причины:\n1) Отсутствуют Visual C++ Redistributable на целевом компьютере\n2) Пути к файлам абсолютные (должны быть относительные)\n3) Не хватает прав на запись\n4) Экспортный шаблон не совпадает с версией Godot\n5) В игре используются неэкспортированные ресурсы\n\nРешение: настройте пути через 'res://' и 'user://'", 
             "экспорт"),
        ]
        
        # Собираем все уроки
        all_lessons = [
            lesson1_ru, lesson2_ru, lesson3_ru, lesson4_ru,
            lesson5_ru, lesson6_ru, lesson7_ru, lesson8_ru,
            lesson9_ru, lesson10_ru, lesson11_ru, lesson12_ru
        ]
        
        for lesson in all_lessons:
            for q, a, c in lesson:
                self.questions_ru.append(q)
                self.answers_ru.append(a)
                if c not in self.categories:
                    self.categories.append(c)
        
        return self
    
    def create_variations(self):
        """Создание вариаций вопросов (синонимы и перефразирования)"""
        
        variation_templates = {
            # Вариации для вопросов об установке
            "не создается файл": [
                "файл не создается", "не могу создать файл", "файл не появляется",
                "проект не создается", "не получается создать проект"
            ],
            
            # Вариации для вопросов о движении
            "не двигается": [
                "не движется", "стоит на месте", "не реагирует на кнопки",
                "не ходит", "не перемещается", "застыл на месте"
            ],
            
            # Вариации для ошибок
            "move_and_slide": [
                "move and slide", "move_and_slide ошибка", "move_and_slide не работает",
                "move and slide error", "move_and_slide undefined"
            ],
            
            # Вариации для анимации
            "анимация": [
                "не работает анимация", "анимация не включается", "не показывает анимацию",
                "не проигрывается анимация", "анимация персонажа не работает"
            ],
            
            # Вариации для прыжка
            "прыжок": [
                "прыжок не работает", "не может прыгнуть", "не подпрыгивает",
                "не взлетает", "не отрывается от земли"
            ],
            
            # Вариации для гравитации
            "гравитация": [
                "гравитация не работает", "не падает вниз", "не притягивается к земле",
                "не работает притяжение", "персонаж не падает"
            ],
            
            # Вариации для регистрации
            "зарегистрироваться": [
                "регистрация", "создать аккаунт", "завести профиль",
                "регистрация на сайте", "как создать учетную запись"
            ],
        }
        
        # Создаем новые вопросы на основе шаблонов
        new_questions_ru = []
        new_answers_ru = []
        
        for i, q in enumerate(self.questions_ru):
            for pattern, variations in variation_templates.items():
                if pattern in q.lower():
                    answer = self.answers_ru[i]
                    category = self.categories[i % len(self.categories)]
                    
                    for var in variations:
                        new_q = q.lower().replace(pattern, var)
                        # Сохраняем оригинальный регистр где возможно
                        new_questions_ru.append(new_q.capitalize())
                        new_answers_ru.append(answer)
                        if category not in self.categories:
                            self.categories.append(category)
                    break
        
        # Добавляем вариации в датасет
        self.questions_ru.extend(new_questions_ru)
        self.answers_ru.extend(new_answers_ru)
        
        print(f"🔄 Добавлено {len(new_questions_ru)} вариаций русских вопросов")
        
        return self
    
    def create_english_extended(self):
        """Создание расширенного английского датасета"""
        
        en_extended = [
            ("My child can't complete the first lesson, the project file won't create, what to do?", 
             "Check: 1) Write permissions in Documents folder 2) Run Godot as administrator 3) Enough disk space (minimum 500MB) 4) Project path has no Cyrillic letters or spaces.", 
             "installation"),
             
            ("Character doesn't move when pressing keys, what's the problem?", 
             "Step by step check:\n1) Is CharacterBody2D node added?\n2) Is there a script attached?\n3) Are input actions configured in Project Settings → Input Map?\n4) Are action names correct in code?\n5) Is move_and_slide() called at the end of _physics_process?", 
             "movement"),
             
            ("Error 'Identifier not found: move_and_slide' in Godot", 
             "Make sure your node extends CharacterBody2D or RigidBody2D. Node2D doesn't have move_and_slide(). Check 'extends' at the beginning of your script.", 
             "scripting"),
             
            ("Animation doesn't play in Godot, what to do?", 
             "Check:\n1) Is Autoplay on Load enabled in AnimationPlayer?\n2) Did you call $AnimationPlayer.play('animation_name')?\n3) Are there keyframes in the animation?\n4) Is the animation name spelled correctly (case sensitive)?", 
             "animation"),
             
            ("How to make double jump in platformer?", 
             "Add jumps_left variable:\nvar jumps_left = 2\n\nfunc _physics_process(delta):\n    if Input.is_action_just_pressed('jump'):\n        if is_on_floor():\n            jumps_left = 2\n            velocity.y = jump_velocity\n        elif jumps_left > 0:\n            jumps_left -= 1\n            velocity.y = jump_velocity", 
             "physics"),
             
            ("Items don't collect on touch, even with Area2D", 
             "Check:\n1) Does the item have Area2D with CollisionShape2D?\n2) Does the player have CollisionShape2D?\n3) Is the body_entered signal connected to the script?\n4) Is queue_free() called in the handler function?\n5) Are collision layers and masks configured correctly?", 
             "signals"),
             
            ("How to add moving platforms?", 
             "Option 1: Move StaticBody2D via AnimationPlayer\nOption 2: Use Path2D and PathFollow2D for complex trajectories\nOption 3: In platform script, use _process(delta) to change position", 
             "platforms"),
             
            ("How to save game progress and load it?", 
             "Use FileAccess to save to user://savegame.save\n\nSaving:\nvar save_data = {'level': 3, 'score': 150}\nvar file = FileAccess.open('user://savegame.save', FileAccess.WRITE)\nfile.store_string(JSON.stringify(save_data))\n\nLoading:\nvar file = FileAccess.open('user://savegame.save', FileAccess.READ)\nvar data = JSON.parse_string(file.get_as_text())", 
             "save_load"),
        ]
        
        for q, a, c in en_extended:
            self.questions_en.append(q)
            self.answers_en.append(a)
            if c not in self.categories:
                self.categories.append(c)
        
        return self
    
    def build_full_dataset(self):
        """Построение полного датасета"""
        
        print("📚 Создание полного датасета...")
        
        self.create_basic_dataset()
        self.create_godot_extended_dataset()
        self.create_english_extended()
        self.create_variations()
        
        print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
        print(f"   Русских вопросов: {len(self.questions_ru)}")
        print(f"   Английских вопросов: {len(self.questions_en)}")
        print(f"   Всего категорий: {len(self.categories)}")
        print(f"   Категории: {', '.join(sorted(set(self.categories)))}")
        
        return self
    
    def save_to_json(self, filepath='dataset.json'):
        """Сохранение датасета в JSON файл"""
        
        data = {
            'questions_ru': self.questions_ru,
            'answers_ru': self.answers_ru,
            'questions_en': self.questions_en,
            'answers_en': self.answers_en,
            'categories': self.categories,
            'category_map': self.category_map,
            'stats': {
                'total_ru': len(self.questions_ru),
                'total_en': len(self.questions_en),
                'total_categories': len(self.categories)
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Датасет сохранен в {filepath}")
        return self
    
    def load_from_json(self, filepath='dataset.json'):
        """Загрузка датасета из JSON файла"""
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.questions_ru = data['questions_ru']
            self.answers_ru = data['answers_ru']
            self.questions_en = data['questions_en']
            self.answers_en = data['answers_en']
            self.categories = data['categories']
            self.category_map = data.get('category_map', self.category_map)
            
            print(f"✅ Датасет загружен из {filepath}")
            print(f"   Русских вопросов: {len(self.questions_ru)}")
            print(f"   Английских вопросов: {len(self.questions_en)}")
            return True
            
        except FileNotFoundError:
            print(f"⚠️ Файл {filepath} не найден")
            return False
        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")
            return False


# Создаем экземпляр датасета
dataset = GodotDataset()

# Если файл существует - загружаем, иначе создаем новый
if not dataset.load_from_json('dataset.json'):
    dataset.build_full_dataset().save_to_json('dataset.json')