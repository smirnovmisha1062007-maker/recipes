# Система управления рецептами

Консольное приложение для создания рецептов, масштабирования порций и генерации списка покупок.

## Установка

```bash
git clone <ваш-репозиторий>
cd <папка>
pip install -r requirements.txt
```

## Использование

```python
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe

r = Recipe("Пицца")
r.add_ingredient(Ingredient("Мука", 500, "г"))
r.add_ingredient(Ingredient("Томаты", 200, "г"))

sl = ShoppingList()
sl.add_recipe(r, 2)  # 2 порции
print(sl.get_list())
```

## Тесты

```bash
pytest
```

## Автор

Смирнов Михаил, группа БИ2509
