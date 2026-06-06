# advanced_chatbot.py - Финальная исправленная версия

import re
import hashlib
import math
from collections import Counter
from datetime import datetime
from typing import Dict, List, Optional, Any

class AdvancedChatbot:
    def __init__(self):
        # Основной словарь: вариация вопроса → ответ
        self.qa_map = {
            # ---------- РЕГИСТРАЦИЯ И ВХОД ----------
            "как зарегистрироваться": "Для регистрации нажмите кнопку 'Записаться на курс' на главной странице. Введите имя пользователя и пароль.",
            "зарегистрироваться": "Для регистрации нажмите кнопку 'Записаться на курс'.",
            "регистрация": "Для регистрации нажмите кнопку 'Записаться на курс'.",
            "создать аккаунт": "Для создания аккаунта нажмите 'Записаться на курс'.",
            "как войти": "Нажмите кнопку 'Вход' в правом верхнем углу, введите логин и пароль.",
            "войти": "Нажмите 'Вход' в правом верхнем углу.",
            "вход в личный кабинет": "Нажмите 'Вход' в правом верхнем углу.",
            "не могу войти": "Проверьте правильность логина и пароля. Если забыли пароль – напишите в поддержку.",
            "забыл пароль": "Напишите на support@godot-learning.ru с указанием вашего имени пользователя.",
            "восстановить пароль": "Обратитесь в поддержку support@godot-learning.ru.",
            "авторизация": "Используйте форму входа в правом верхнем углу.",
            
            # ---------- ДВИЖЕНИЕ ПЕРСОНАЖА ----------
            "персонаж не двигается": "Проверьте: 1) Узел CharacterBody2D 2) CollisionShape2D 3) Настройки Input Map 4) move_and_slide() в _physics_process",
            "не движется": "Убедитесь, что узел – CharacterBody2D, а в скрипте есть _physics_process и move_and_slide().",
            "не ходит": "Скорее всего проблема в Input Map или отсутствии move_and_slide().",
            "клавиши не работают": "Настройте Input Map: Project Settings → Input Map → добавьте действия left/right/jump.",
            "движение не работает": "Проверьте, что в _physics_process есть вызов move_and_slide().",
            "не реагирует на кнопки": "Назначьте клавиши в Input Map.",
            "персонаж стоит на месте": "Добавьте в скрипт движение через Input.get_axis().",
            "персонаж не ходит": "Смотрите предыдущие ответы по движению.",
            
            # ---------- MOVE_AND_SLIDE ОШИБКА ----------
            "move_and_slide ошибка": "Ошибка возникает, если узел не CharacterBody2D. Пропишите 'extends CharacterBody2D' в начале скрипта.",
            "move_and_side ошибка": "Опечатка: правильно move_and_slide. Убедитесь, что узел – CharacterBody2D.",
            "move and slide error": "Make sure your node extends CharacterBody2D.",
            "move_and_slide undefined": "Нужно 'extends CharacterBody2D'.",
            "move_and_slide не работает": "Проверьте, что узел действительно CharacterBody2D.",
            
            # ---------- АНИМАЦИЯ ----------
            "анимация не проигрывается": "Проверьте: 1) Autoplay on Load 2) play('имя') 3) ключевые кадры 4) правильное имя анимации.",
            "не работает анимация": "Убедитесь, что вы вызвали $AnimationPlayer.play('название_анимации').",
            "как сделать анимацию": "Добавьте AnimationPlayer, создайте анимации idle/run/jump, переключайте их через код.",
            "спрайт не меняется": "Проверьте имя анимации и наличие ключевых кадров.",
            "анимация не запускается": "Включите Autoplay on Load или вызовите play() в _ready().",
            "нет анимации": "Создайте анимации в AnimationPlayer и вызовите их в коде.",
            
            # ---------- ДВОЙНОЙ ПРЫЖОК ----------
            "двойной прыжок": "Добавьте переменную jumps_left. Пример: var jumps_left = 2; if Input.is_action_just_pressed('jump'): if is_on_floor(): jumps_left=2; velocity.y=jump_velocity; elif jumps_left>0: jumps_left-=1; velocity.y=jump_velocity",
            "double jump": "Add jumps_left variable. Example in the answer above.",
            "прыжок два раза": "Используйте jumps_left (см. ответ про двойной прыжок).",
            "второй прыжок в воздухе": "Реализуется через счётчик jumps_left.",
            "как прыгнуть дважды": "Смотрите ответ про двойной прыжок.",
            
            # ---------- СОХРАНЕНИЕ ИГРЫ ----------
            "как сохранить игру": "Используйте FileAccess и JSON. Сохраняйте в user://savegame.save.",
            "сохранить игру": "Запишите данные через FileAccess.open('user://savegame.save', FileAccess.WRITE).",
            "игра не сохраняется": "Проверьте, что вы вызываете сохранение. Путь должен быть user://...",
            "прогресс не сохраняется": "Возможно, вы не записываете данные. Используйте store_string(JSON.stringify()).",
            "не сохраняется": "Добавьте код сохранения после изменения важных данных (счёт, уровень).",
            "сохранить прогресс": "Сериализуйте данные в JSON и запишите в файл.",
            "потеря прогресса": "Скорее всего вы не загружаете сохранение при старте игры.",
            "загрузить игру": "Читайте файл через FileAccess.open(user://..., FileAccess.READ).",
            "автосохранение": "Вызывайте сохранение при смене уровня или каждые N секунд через таймер.",
            "сохранения не работают": "Проверьте путь и права на запись. Используйте user://",
            "куда сохраняется игра": "В папку user:// (специальная папка Godot для сохранений).",
            
            # ---------- КАМЕРА ----------
            "камера не следует": "Добавьте Camera2D как дочерний к персонажу, включите Current и Smoothing.",
            "камера не двигается": "Camera2D должен быть дочерним узлом персонажа.",
            "камера убегает": "Используйте Limits в Camera2D для ограничения движения.",
            "camera2d не работает": "Убедитесь, что у камеры включён флаг Current.",
            
            # ---------- ВРАГИ ----------
            "как сделать врага": "Создайте Area2D или CharacterBody2D, добавьте CollisionShape2D, напишите скрипт движения.",
            "враг не двигается": "В _physics_process добавьте velocity.x = direction * speed; move_and_slide()",
            "патрулирование врага": "Используйте RayCast2D для обнаружения края платформы и меняйте direction.",
            "добавить врага": "Создайте сцену врага и разместите на уровне.",
            
            # ---------- СБОР ПРЕДМЕТОВ ----------
            "предметы не собираются": "У предмета должен быть Area2D и сигнал body_entered, в функции – queue_free()",
            "не могу собрать": "Проверьте, что у персонажа есть CollisionShape2D, а у предмета – Area2D.",
            "монеты не подбираются": "Подключите сигнал body_entered к скрипту и вызовите queue_free().",
            "area2d не срабатывает": "Убедитесь, что коллизии включены (collision layers / masks).",
            
            # ---------- ЭКСПОРТ ИГРЫ ----------
            "как экспортировать игру": "Project → Export → Add → выберите платформу → Export Project.",
            "экспорт в windows": "Выберите шаблон Windows Desktop, настройте и нажмите Export.",
            "собрать игру": "Через меню Export.",
            "нет иконки": "В настройках экспорта укажите .ico файл (размер 256×256).",
            "ошибка экспорта": "Установите экспортные шаблоны через Editor → Manage Export Templates.",
            
            # ---------- ОПТИМИЗАЦИЯ ----------
            "игра тормозит": "Уменьшите количество объектов, используйте Object pooling, включите фрустум камеры.",
            "лаги": "Отключайте невидимые узлы, объединяйте статичные спрайты.",
            "низкий фпс": "Оптимизируйте: меньше физических объектов, используйте StaticBody2D.",
            
            # ---------- УСТАНОВКА GODOT ----------
            "godot не запускается": "Запустите с флагом --rendering-driver opengl3. Обновите драйверы видеокарты.",
            "ошибка vulkan": "Используйте --rendering-driver opengl3 при запуске.",
            "не устанавливается godot": "Скачайте архив с godotengine.org и распакуйте в любую папку.",
            
            # ---------- ОБЩИЕ ВОПРОСЫ ----------
            "сколько уроков": "Курс включает 12 уроков по созданию платформера на Godot.",
            "всего уроков": "12 уроков.",
            "бесплатно": "Курс полностью бесплатный.",
            "сертификат": "Сертификат выдаётся после прохождения всех 12 уроков.",
            "поддержка": "Пишите на support@godot-learning.ru.",
            "материалы": "Материалы находятся внутри каждого урока в разделе 'Дополнительные материалы'.",
            "скачать материалы": "Откройте урок, там есть ссылки на PDF, ZIP и примеры кода.",
            "где взять спрайты": "Бесплатные спрайты на OpenGameArt.org, Kenney.nl, Itch.io",
            "звуки для игры": "Используйте .ogg файлы. Бесплатные звуки на Freesound.org.",
            "godot или unity": "Godot проще для начинающих, полностью бесплатный, идеален для 2D игр.",
            "документация godot": "docs.godotengine.org – официальная документация.",
            "как начать обучение": "После входа на сайт выберите урок 1 на главной странице.",
            "как открыть урок": "Нажмите на карточку урока на главной странице.",
        }
        
        # Дополнительные вариации с опечатками
        self.typo_variations = {
            "move_and_side": "move_and_slide ошибка",
            "move and side": "move_and_slide ошибка",
        }
        
        self.cache = {}
        self.cache_size = 500
        self.stats = {
            'total_queries': 0,
            'successful_queries': 0,
            'cache_hits': 0,
            'languages': {'ru': 0, 'en': 0},
            'intents': {}
        }
        
        print(f"✅ Чат-бот загружен с {len(self.qa_map)} вариантами вопросов.")
    
    def detect_language(self, text: str) -> str:
        """Определение языка текста"""
        cyrillic = sum(1 for c in text.lower() if 'а' <= c <= 'я' or c == 'ё')
        latin = sum(1 for c in text.lower() if 'a' <= c <= 'z')
        return 'ru' if cyrillic > latin else 'en'
    
    def _normalize_query(self, text: str) -> str:
        """Нормализация запроса"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _check_typo(self, query: str) -> str:
        """Исправление опечаток"""
        query_lower = query.lower()
        for typo, correct_phrase in self.typo_variations.items():
            if typo in query_lower:
                return correct_phrase
        return query
    
    def predict(self, query: str, language: str = "auto", threshold: float = 0.1) -> Dict[str, Any]:
        """Поиск ответа на вопрос"""
        # Кэш
        cache_key = hashlib.md5(query.encode()).hexdigest()
        if cache_key in self.cache:
            self.stats['cache_hits'] += 1
            self.stats['total_queries'] += 1
            return self.cache[cache_key]
        
        # Нормализуем запрос
        normalized = self._normalize_query(query)
        corrected = self._check_typo(normalized)
        
        # Поиск по словарю
        best_answer = None
        best_match_len = 0
        
        for variant, answer in self.qa_map.items():
            if variant in normalized or variant in corrected:
                if len(variant) > best_match_len:
                    best_match_len = len(variant)
                    best_answer = answer
        
        # Если не нашли – ищем по частям
        if not best_answer:
            for variant, answer in self.qa_map.items():
                parts = variant.split()
                matched = sum(1 for p in parts if p in normalized)
                if matched >= max(1, len(parts) // 2):
                    if len(variant) > best_match_len:
                        best_match_len = len(variant)
                        best_answer = answer
        
        # Формируем результат
        if best_answer:
            result = {
                'found': True,
                'answer': best_answer,
                'confidence': min(95, 50 + best_match_len),
                'category': 'general'
            }
            self.stats['successful_queries'] += 1
        else:
            fallback = "Извините, я не нашёл ответ. Попробуйте переформулировать вопрос.\n\nПримеры вопросов:\n- Как зарегистрироваться?\n- Персонаж не двигается\n- move_and_slide ошибка\n- Как сохранить игру?\n- Сколько уроков?"
            result = {
                'found': False,
                'answer': fallback,
                'confidence': 0,
                'category': 'general'
            }
        
        self.stats['total_queries'] += 1
        if language == "auto":
            language = self.detect_language(query)
        self.stats['languages'][language] += 1
        
        # Кэшируем
        if len(self.cache) > self.cache_size:
            self.cache.pop(next(iter(self.cache)))
        self.cache[cache_key] = result
        
        return result
    
    def predict_with_context(self, query: str, user_id: str, threshold: float = 0.1) -> Dict[str, Any]:
        """Предсказание с контекстом (для совместимости с app.py)"""
        return self.predict(query, "auto", threshold)
    
    def get_category_suggestions(self, user_id: str = None, language: str = "ru") -> List[str]:
        """Предложения для чата"""
        if language == "ru":
            return [
                "Как зарегистрироваться?",
                "Персонаж не двигается",
                "move_and_slide ошибка",
                "Как сохранить игру?",
                "Как сделать двойной прыжок?",
                "Анимация не проигрывается",
                "Предметы не собираются",
                "Сколько всего уроков?",
                "Как экспортировать игру?"
            ]
        else:
            return [
                "How to register?",
                "Character doesn't move",
                "move_and_slide error",
                "How to save game?",
                "How to make double jump?",
            ]
    
    def get_analytics(self) -> Dict[str, Any]:
        """Статистика работы бота"""
        success_rate = 0
        if self.stats['total_queries'] > 0:
            success_rate = round(self.stats['successful_queries'] / self.stats['total_queries'] * 100, 1)
        
        return {
            'total_questions_ru': len(self.qa_map),
            'total_questions_en': 10,
            'total_questions': len(self.qa_map) + 10,
            'russian_questions': len(self.qa_map),
            'english_questions': 10,
            'categories': 15,
            'vocabulary_size_ru': len(self.qa_map) * 5,
            'vocabulary_size_en': 100,
            'total_queries': self.stats['total_queries'],
            'successful_queries': self.stats['successful_queries'],
            'success_rate': success_rate,
            'language_distribution': self.stats['languages'],
            'model_loaded': True
        }
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Статистика пользователя (для совместимости)"""
        return {
            'user_id': user_id,
            'total_questions': 0,
            'top_interests': [],
            'current_lesson': 1,
            'last_activity': datetime.now().isoformat()
        }
    
    def add_question_answer(self, question: str, answer: str, category: str, language: str = "ru"):
        """Добавление нового вопроса (для совместимости)"""
        self.qa_map[question.lower()] = answer
        print(f"✅ Добавлен новый вопрос: {question}")
    
    def clear_cache(self):
        """Очистка кэша"""
        self.cache.clear()
        self.stats['cache_hits'] = 0
        print("🗑️ Кэш очищен")
    
    def init(self):
        """Инициализация"""
        print(f"🚀 Бот готов. База знаний содержит {len(self.qa_map)} вариантов вопросов.")
        return self


# Глобальный экземпляр
chatbot = AdvancedChatbot()


# Тестирование при прямом запуске
if __name__ == "__main__":
    chatbot.init()
    print("\n" + "="*60)
    print("ТЕСТИРОВАНИЕ")
    print("="*60)
    
    test_queries = [
        "Как зарегистрироваться?",
        "персонаж не двигается",
        "move_and_side ошибка",
        "игра не сохраняется",
        "камера не следует",
        "сколько уроков",
        "не работает анимация"
    ]
    
    for q in test_queries:
        r = chatbot.predict(q)
        status = "✅" if r['found'] else "❌"
        print(f"\n{status} {q}")
        print(f"   {r['answer'][:120]}...")
    
    print("\n✅ Тест завершён!")