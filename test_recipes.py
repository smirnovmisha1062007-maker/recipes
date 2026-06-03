import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe


def test_ingredient_init():
    ing = Ingredient("Мука", 500, "г")
    assert ing.name == "Мука"
    assert ing.quantity == 500.0
    assert ing.unit == "г"

def test_ingredient_str():
    assert str(Ingredient("Мука", 500, "г")) == "Мука: 500.0 г"

def test_ingredient_eq_same():
    assert Ingredient("Мука", 100, "г") == Ingredient("Мука", 999, "г")

def test_ingredient_eq_diff_name():
    assert Ingredient("Мука", 100, "г") != Ingredient("Соль", 100, "г")

def test_ingredient_eq_diff_unit():
    assert Ingredient("Мука", 100, "г") != Ingredient("Мука", 100, "кг")

def test_ingredient_invalid_quantity():
    with pytest.raises(ValueError):
        Ingredient("Мука", -1, "г")


def test_recipe_init():
    r = Recipe("Пицца")
    assert r.title == "Пицца"
    assert r.ingredients == []

def test_recipe_add_ingredient():
    r = Recipe("Пицца")
    r.add_ingredient(Ingredient("Мука", 500, "г"))
    assert len(r) == 1

def test_recipe_add_duplicate_sums():
    r = Recipe("Пицца")
    r.add_ingredient(Ingredient("Мука", 300, "г"))
    r.add_ingredient(Ingredient("Мука", 200, "г"))
    assert len(r) == 1
    assert r.ingredients[0].quantity == 500.0

def test_recipe_scale_returns_new():
    r = Recipe("Пицца")
    r.add_ingredient(Ingredient("Мука", 100, "г"))
    scaled = r.scale(2)
    assert scaled is not r
    assert r.ingredients[0].quantity == 100.0

def test_recipe_scale_multiplies():
    r = Recipe("Пицца")
    r.add_ingredient(Ingredient("Мука", 100, "г"))
    assert r.scale(3).ingredients[0].quantity == 300.0

def test_recipe_scale_invalid():
    with pytest.raises(ValueError):
        Recipe("Пицца").scale(-1)

def test_recipe_len():
    r = Recipe("Пицца")
    r.add_ingredient(Ingredient("Мука", 100, "г"))
    r.add_ingredient(Ingredient("Соль", 5, "г"))
    assert len(r) == 2


def test_shopping_add_recipe():
    r = Recipe("Пицца")
    r.add_ingredient(Ingredient("Мука", 100, "г"))
    sl = ShoppingList()
    sl.add_recipe(r, 2)
    assert len(sl._items) == 1

def test_shopping_invalid_portions():
    with pytest.raises(ValueError):
        ShoppingList().add_recipe(Recipe("Пицца"), 0)

def test_shopping_remove_recipe():
    r = Recipe("Пицца")
    r.add_ingredient(Ingredient("Мука", 100, "г"))
    sl = ShoppingList()
    sl.add_recipe(r, 1)
    sl.remove_recipe("Пицца")
    assert sl._items == []

def test_shopping_remove_missing():
    ShoppingList().remove_recipe("Несуществующий")

def test_shopping_get_list_sums():
    r1 = Recipe("Пицца")
    r1.add_ingredient(Ingredient("Мука", 100, "г"))
    r2 = Recipe("Хлеб")
    r2.add_ingredient(Ingredient("Мука", 200, "г"))
    sl = ShoppingList()
    sl.add_recipe(r1, 1)
    sl.add_recipe(r2, 1)
    assert sl.get_list()[0].quantity == 300.0

def test_shopping_get_list_sorted():
    r = Recipe("Тест")
    r.add_ingredient(Ingredient("Яйца", 2, "шт"))
    r.add_ingredient(Ingredient("Мука", 100, "г"))
    sl = ShoppingList()
    sl.add_recipe(r, 1)
    names = [i.name for i in sl.get_list()]
    assert names == sorted(names)

def test_shopping_add():
    r1 = Recipe("Пицца")
    r1.add_ingredient(Ingredient("Мука", 100, "г"))
    r2 = Recipe("Хлеб")
    r2.add_ingredient(Ingredient("Соль", 5, "г"))
    sl1, sl2 = ShoppingList(), ShoppingList()
    sl1.add_recipe(r1, 1)
    sl2.add_recipe(r2, 1)
    combined = sl1 + sl2
    assert len(combined._items) == 2
    assert len(sl1._items) == 1


def test_dietary_str():
    assert str(DietaryRecipe("Пицца", "веган")).startswith("[веган]")

def test_dietary_scale_returns_dietary():
    r = DietaryRecipe("Пицца", "веган")
    r.add_ingredient(Ingredient("Мука", 100, "г"))
    scaled = r.scale(2)
    assert isinstance(scaled, DietaryRecipe)
    assert scaled.diet_type == "веган"
