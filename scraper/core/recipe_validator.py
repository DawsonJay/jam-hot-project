"""
Shared recipe validation logic for jam recipes.

This module provides consistent validation logic across all adapters
to determine if a recipe is actually a jam recipe.
"""

from typing import List, Dict, Any


def is_jam_recipe(recipe_data: Dict[str, Any]) -> bool:
    """
    Validate that a recipe is actually a jam recipe using shared logic.
    
    A recipe is considered a jam recipe if:
    1. It has jam-related keywords in title/description, AND
    2. It has jam-making ingredients, AND  
    3. It does NOT have "jam" as an ingredient (recipes that use jam, not make jam), AND
    4. It doesn't have non-jam indicators in the title, AND
    5. It has a valid rating (not zero or missing)
    
    Args:
        recipe_data: Dictionary containing recipe data
        
    Returns:
        bool: True if this is a jam recipe, False otherwise
    """
    title = recipe_data.get("title", "").lower()
    description = recipe_data.get("description", "").lower()
    ingredients = recipe_data.get("ingredients", [])
    
    # 1. Check for jam-related keywords in title or description
    jam_keywords = ["jam", "jelly", "preserve", "marmalade", "conserve"]
    has_jam_keyword = (
        any(keyword in title for keyword in jam_keywords) or
        any(keyword in description for keyword in jam_keywords)
    )
    
    if not has_jam_keyword:
        return False
    
    # 2. Check for jam-making ingredients
    jam_ingredients = ["sugar", "pectin", "lemon juice", "lime juice", "citric acid"]
    has_jam_ingredients = False
    
    for ingredient in ingredients:
        if isinstance(ingredient, dict):
            ingredient_name = ingredient.get("name", "").lower()
        else:
            ingredient_name = str(ingredient).lower()
            
        if any(jam_ing in ingredient_name for jam_ing in jam_ingredients):
            has_jam_ingredients = True
            break
    
    if not has_jam_ingredients:
        return False
    
    # 3. Check if recipe has "jam" as an ingredient (recipes that USE jam, not MAKE jam)
    # But exclude legitimate jam-making ingredients like "jam sugar"
    has_jam_as_ingredient = False
    jam_making_ingredients = ["jam sugar", "jam sugar", "preserving sugar", "jam setting sugar"]
    
    for ingredient in ingredients:
        if isinstance(ingredient, dict):
            ingredient_name = ingredient.get("name", "").lower()
        else:
            ingredient_name = str(ingredient).lower()
            
        # Check if this is a jam-making ingredient (legitimate)
        is_jam_making_ingredient = any(jam_ing in ingredient_name for jam_ing in jam_making_ingredients)
        
        # Look for "jam" as a standalone word or in phrases like "strawberry jam"
        # but only if it's not a jam-making ingredient
        if "jam" in ingredient_name and not is_jam_making_ingredient:
            # Use regex to find "jam" as a whole word
            import re
            if re.search(r'\bjam\b', ingredient_name):
                has_jam_as_ingredient = True
                break
    
    if has_jam_as_ingredient:
        return False
    
    # 4. Check for non-jam indicators in title
    non_jam_keywords = [
        "cake", "cupcake", "muffin", "bread", "cookie", "pie", "tart",
        "sandwich", "toast", "pancake", "waffle", "crepe", "danish",
        "cheesecake", "trifle", "parfait", "sundae", "milkshake",
        "smoothie", "cocktail", "sauce", "glaze", "frosting", "icing",
        "filling", "topping", "spread", "dip", "salad", "dressing",
        "marinade", "rub", "seasoning", "garnish", "popsicle", "frozen",
        "ice cream", "sorbet", "granita", "sherbet", "bar", "bars",
        "doughnut", "doughnuts", "donut", "donuts", "crostata", "tarts",
        "pastry", "pastries", "scuffin", "roll", "egg roll", "fried",
        "baked", "oven", "flour", "baking powder", "baking soda", "yeast",
        "dough", "drink", "beverage", "mocktail", "juice",
        # Additional non-jam indicators
        "sponge", "scones", "scone", "baguette", "turnovers", "turnover",
        "board", "grazing", "chicken", "thighs", "rice", "peas", "beef",
        "pork", "fish", "salmon", "tuna", "shrimp", "pasta", "noodles",
        "soup", "stew", "casserole", "slow cooker", "crockpot", "roast",
        "grilled", "bbq", "barbecue", "breakfast", "lunch", "dinner",
        "main course", "side dish", "appetizer", "starter", "entree",
        "pizza", "burger", "wrap", "quesadilla", "tacos", "enchiladas"
    ]
    
    has_non_jam_indicators = any(keyword in title for keyword in non_jam_keywords)
    
    if has_non_jam_indicators:
        return False
    
    # 5. Check for valid rating (not zero or missing)
    rating = recipe_data.get("rating")
    if rating is None or rating == 0 or rating == 0.0:
        return False
    
    # If we get here, it's a valid jam recipe
    return True
