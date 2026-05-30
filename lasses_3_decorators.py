from functools import wraps
import time

def is_alive(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if self.health <= 0:
            print(f"{self.name} мертв и не может действовать!")
            return None
        return func(*args, **kwargs)
    return wrapper

def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Начало действия: {func.__name__}")
        result = func(*args, **kwargs)
        print("[LOG] Действие завершено")
        return result
    return wrapper

class Hero:
    def __init__(self, name, hero_class):
        self.name = name
        self.hero_class = hero_class
        if hero_class == "волшебник":
            self.health = 60
            self.mana = 50
        else:
            self.health = 100
            self.mana = 10
        self.spells_names = {}
        self.items = {}

    @is_alive
    def attack(self, damage):
        print(f"Герой нанес урон: {damage}")

    @log_action
    def heal(self, amount):
        self.health += amount

    @is_alive
    def cast_spell(self, spell_name):
        if spell_name in self.spells_names:
            spell = self.spells_names[spell_name]
            if self.mana >= spell["mana_cost"]:
                self.mana -= spell["mana_cost"]
                print(spell_name)
            else:
                print("Недостаточно маны!")
        else:
            print("Заклинание не изучено!")

    def add_spell(self, spell_name, mana_cost=0, attack_damage=0, health_increase=0):
        self.spells_names[spell_name] = {
            "mana_cost": mana_cost,
            "attack_damage": attack_damage,
            "health_increase": health_increase
        }

    def add_item(self, item_name, params):
        if len(self.items) < 6:
            self.items[item_name] = params
        else:
            print("Лимит предметов достигнут!")

def temporary_health_boost(multiplier, duration):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            original = self.health
            self.health = int(self.health * multiplier)
            time.sleep(duration)
            result = func(*args, **kwargs)
            self.health = original
            return result
        return wrapper
    return decorator

def temporary_mana_boost(multiplier, duration):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            if self.hero_class == "волшебник":
                original = self.mana
                self.mana = int(self.mana * multiplier)
                time.sleep(duration)
                result = func(*args, **kwargs)
                self.mana = original
            else:
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

def cooldown(seconds):
    def decorator(func):
        func.last_called = 0
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if now - func.last_called < seconds:
                print(f"Действие на перезарядке! Подождите {seconds - (now - func.last_called):.1f} сек.")
                return None
            func.last_called = now
            return func(*args, **kwargs)
        return wrapper
    return decorator