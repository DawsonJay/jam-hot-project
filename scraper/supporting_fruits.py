"""
Supporting fruits in jam making.

These fruits are typically used for pectin, acidity, or bulk rather than as primary ingredients.
They are commonly added to jam recipes to help with gelling, acidity, or to bulk up the recipe.
"""

SUPPORTING_FRUITS = [
    # Citrus fruits (pectin and acidity)
    "lemon",      # Pectin and acidity
    "lime",       # Pectin and acidity  
    "orange",     # Pectin (especially peel)
    
    # High pectin fruits
    "apple",      # Bulk and pectin
]

def is_supporting_fruit(fruit_name):
    """
    Check if a fruit is typically used as a supporting ingredient.
    
    Args:
        fruit_name (str): The fruit name to check (case-insensitive)
        
    Returns:
        bool: True if the fruit is typically supporting, False otherwise
    """
    return fruit_name.lower() in SUPPORTING_FRUITS

def get_supporting_fruits():
    """
    Get the list of supporting fruits.
    
    Returns:
        list: List of supporting fruit names
    """
    return SUPPORTING_FRUITS.copy()

if __name__ == "__main__":
    # Test the supporting fruits functions
    print("Supporting fruits in jam making:")
    for fruit in SUPPORTING_FRUITS:
        print(f"  - {fruit}")
    
    print(f"\nTotal supporting fruits: {len(SUPPORTING_FRUITS)}")
    
    # Test the is_supporting_fruit function
    test_fruits = ["strawberry", "lemon", "blueberry", "apple", "lime", "orange", "peach"]
    print(f"\nTesting fruit classification:")
    for fruit in test_fruits:
        is_supporting = is_supporting_fruit(fruit)
        status = "SUPPORTING" if is_supporting else "PRIMARY"
        print(f"  {fruit}: {status}")
