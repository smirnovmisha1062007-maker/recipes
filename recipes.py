class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self) -> float:
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if float(value) <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float(value)

    def __str__(self) -> str:
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self) -> str:
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Ingredient):
            return NotImplemented
        return self.name == other.name and self.unit == other.unit


class Recipe:
    def __init__(self, title: str, ingredients: list = None):
        self.title = title
        self.ingredients = []
        if ingredients:
            for ing in ingredients:
                self.add_ingredient(ing)

    def add_ingredient(self, ingredient: Ingredient):
        for existing in self.ingredients:
            if existing == ingredient:
                existing.quantity += ingredient.quantity
                return
        self.ingredients.append(
            Ingredient(ingredient.name, ingredient.quantity, ingredient.unit)
        )

    @staticmethod
    def is_valid_ratio(ratio) -> bool:
        try:
            return float(ratio) > 0
        except (TypeError, ValueError):
            return False

    def scale(self, ratio: float) -> "Recipe":
        if not Recipe.is_valid_ratio(ratio):
            raise ValueError("Коэффициент масштабирования должен быть положительным числом")
        new_recipe = Recipe(self.title)
        for ing in self.ingredients:
            new_recipe.ingredients.append(
                Ingredient(ing.name, ing.quantity * ratio, ing.unit)
            )
        return new_recipe

    def __len__(self) -> int:
        return len(self.ingredients)

    def __str__(self) -> str:
        lines = [f"Рецепт: {self.title}"]
        for ing in self.ingredients:
            lines.append(f"  - {ing}")
        return "\n".join(lines)


class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled = recipe.scale(portions)
        for ing in scaled.ingredients:
            self._items.append((ing, recipe.title))

    def remove_recipe(self, title: str):
        self._items = [(ing, t) for ing, t in self._items if t != title]

    def get_list(self) -> list:
        totals = {}
        for ing, _ in self._items:
            key = (ing.name, ing.unit)
            totals[key] = totals.get(key, 0.0) + ing.quantity
        result = [Ingredient(name, qty, unit) for (name, unit), qty in totals.items()]
        result.sort(key=lambda x: x.name)
        return result

    def __add__(self, other: "ShoppingList") -> "ShoppingList":
        if not isinstance(other, ShoppingList):
            return NotImplemented
        combined = ShoppingList()
        combined._items = self._items.copy() + other._items.copy()
        return combined

    def __str__(self) -> str:
        lines = ["Список покупок:"]
        for ing in self.get_list():
            lines.append(f"  - {ing}")
        return "\n".join(lines)


class DietaryRecipe(Recipe):
    def __init__(self, title: str, diet_type: str, ingredients: list = None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float) -> "DietaryRecipe":
        base = super().scale(ratio)
        new_recipe = DietaryRecipe(base.title, self.diet_type)
        new_recipe.ingredients = base.ingredients
        return new_recipe

    def __str__(self) -> str:
        lines = super().__str__().split("\n")
        lines[0] = f"[{self.diet_type}] {self.title}"
        return "\n".join(lines)
