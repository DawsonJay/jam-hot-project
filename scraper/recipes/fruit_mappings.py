"""
Comprehensive fruit mapping system for jam recipes.

This module provides mappings from various fruit name variations to standardized
AI model names. Covers traditional jam fruits with regional variations.
"""

# Comprehensive fruit mapping dictionary
# Key: standardized AI name
# Value: dictionary with variations and AI name
FRUIT_MAP = {
    # Berries
    "strawberry": {
        "variations": [
            "strawberry", "strawberries", "fresh strawberry", "fresh strawberries",
            "frozen strawberry", "frozen strawberries", "wild strawberry", "wild strawberries",
            "strawberry puree", "strawberry pulp", "strawberry jam", "strawberry preserve"
        ],
        "ai_name": "strawberry"
    },
    
    "blueberry": {
        "variations": [
            "blueberry", "blueberries", "fresh blueberry", "fresh blueberries",
            "frozen blueberry", "frozen blueberries", "wild blueberry", "wild blueberries",
            "blueberry puree", "blueberry pulp", "highbush blueberry", "lowbush blueberry"
        ],
        "ai_name": "blueberry"
    },
    
    "raspberry": {
        "variations": [
            "raspberry", "raspberries", "fresh raspberry", "fresh raspberries",
            "frozen raspberry", "frozen raspberries", "wild raspberry", "wild raspberries",
            "raspberry puree", "raspberry pulp", "red raspberry", "black raspberry"
        ],
        "ai_name": "raspberry"
    },
    
    "blackberry": {
        "variations": [
            "blackberry", "blackberries", "fresh blackberry", "fresh blackberries",
            "frozen blackberry", "frozen blackberries", "wild blackberry", "wild blackberries",
            "blackberry puree", "blackberry pulp", "dewberry", "dewberries"
        ],
        "ai_name": "blackberry"
    },
    
    "elderberry": {
        "variations": [
            "elderberry", "elderberries", "fresh elderberry", "fresh elderberries",
            "elderberry puree", "elderberry pulp", "sambucus", "elder"
        ],
        "ai_name": "elderberry"
    },
    
    "cranberry": {
        "variations": [
            "cranberry", "cranberries", "fresh cranberry", "fresh cranberries",
            "frozen cranberry", "frozen cranberries", "cranberry puree", "cranberry pulp"
        ],
        "ai_name": "cranberry"
    },
    
    "gooseberry": {
        "variations": [
            "gooseberry", "gooseberries", "fresh gooseberry", "fresh gooseberries",
            "gooseberry puree", "gooseberry pulp", "cape gooseberry", "cape gooseberries"
        ],
        "ai_name": "gooseberry"
    },
    
    "currant": {
        "variations": [
            "currant", "currants", "red currant", "red currants", "black currant", "black currants",
            "white currant", "white currants", "fresh currant", "fresh currants",
            "currant puree", "currant pulp"
        ],
        "ai_name": "currant"
    },
    
    # Stone Fruits
    "peach": {
        "variations": [
            "peach", "peaches", "fresh peach", "fresh peaches", "frozen peach", "frozen peaches",
            "peach puree", "peach pulp", "white peach", "white peaches", "yellow peach", "yellow peaches",
            "cling peach", "cling peaches", "freestone peach", "freestone peaches"
        ],
        "ai_name": "peach"
    },
    
    "apricot": {
        "variations": [
            "apricot", "apricots", "fresh apricot", "fresh apricots", "dried apricot", "dried apricots",
            "apricot puree", "apricot pulp", "apricot jam", "apricot preserve"
        ],
        "ai_name": "apricot"
    },
    
    "plum": {
        "variations": [
            "plum", "plums", "fresh plum", "fresh plums", "frozen plum", "frozen plums",
            "plum puree", "plum pulp", "damson plum", "damson plums", "italian plum", "italian plums",
            "santa rosa plum", "santa rosa plums"
        ],
        "ai_name": "plum"
    },
    
    "cherry": {
        "variations": [
            "cherry", "cherries", "fresh cherry", "fresh cherries", "frozen cherry", "frozen cherries",
            "cherry puree", "cherry pulp", "sweet cherry", "sweet cherries", "sour cherry", "sour cherries",
            "bing cherry", "bing cherries", "rainier cherry", "rainier cherries"
        ],
        "ai_name": "cherry"
    },
    
    "nectarine": {
        "variations": [
            "nectarine", "nectarines", "fresh nectarine", "fresh nectarines",
            "nectarine puree", "nectarine pulp", "white nectarine", "white nectarines"
        ],
        "ai_name": "nectarine"
    },
    
    # Citrus Fruits
    "orange": {
        "variations": [
            "orange", "oranges", "fresh orange", "fresh oranges", "orange juice", "orange zest",
            "orange peel", "blood orange", "blood oranges", "navel orange", "navel oranges",
            "valencia orange", "valencia oranges", "mandarin orange", "mandarin oranges"
        ],
        "ai_name": "orange"
    },
    
    "lemon": {
        "variations": [
            "lemon", "lemons", "fresh lemon", "fresh lemons", "lemon juice", "lemon zest",
            "lemon peel", "meyer lemon", "meyer lemons", "eureka lemon", "eureka lemons"
        ],
        "ai_name": "lemon"
    },
    
    "lime": {
        "variations": [
            "lime", "limes", "fresh lime", "fresh limes", "lime juice", "lime zest",
            "lime peel", "key lime", "key limes", "persian lime", "persian limes"
        ],
        "ai_name": "lime"
    },
    
    "grapefruit": {
        "variations": [
            "grapefruit", "grapefruits", "fresh grapefruit", "fresh grapefruits",
            "grapefruit juice", "grapefruit zest", "pink grapefruit", "pink grapefruits",
            "red grapefruit", "red grapefruits", "white grapefruit", "white grapefruits"
        ],
        "ai_name": "grapefruit"
    },
    
    # Tropical Fruits
    "mango": {
        "variations": [
            "mango", "mangoes", "mangos", "fresh mango", "fresh mangoes", "fresh mangos",
            "frozen mango", "frozen mangoes", "frozen mangos", "mango puree", "mango pulp",
            "ataulfo mango", "ataulfo mangoes", "honey mango", "honey mangoes"
        ],
        "ai_name": "mango"
    },
    
    "pineapple": {
        "variations": [
            "pineapple", "pineapples", "fresh pineapple", "fresh pineapples",
            "frozen pineapple", "frozen pineapples", "pineapple puree", "pineapple pulp",
            "pineapple juice", "canned pineapple", "canned pineapples"
        ],
        "ai_name": "pineapple"
    },
    
    "passion_fruit": {
        "variations": [
            "passion fruit", "passionfruit", "passion-fruit", "passion fruits", "passionfruits",
            "fresh passion fruit", "fresh passionfruit", "passion fruit puree", "passion fruit pulp",
            "passion fruit juice", "purple passion fruit", "yellow passion fruit"
        ],
        "ai_name": "passion_fruit"
    },
    
    "dragon_fruit": {
        "variations": [
            "dragon fruit", "dragonfruit", "dragon-fruit", "pitaya", "pitahaya", "strawberry pear",
            "red dragon fruit", "white dragon fruit", "yellow dragon fruit",
            "fresh dragon fruit", "frozen dragon fruit", "dragon fruit puree", "dragon fruit pulp"
        ],
        "ai_name": "dragon_fruit"
    },
    
    "papaya": {
        "variations": [
            "papaya", "papayas", "fresh papaya", "fresh papayas", "frozen papaya", "frozen papayas",
            "papaya puree", "papaya pulp", "papaya juice", "hawaiian papaya", "hawaiian papayas"
        ],
        "ai_name": "papaya"
    },
    
    # Other Traditional Jam Fruits
    "apple": {
        "variations": [
            "apple", "apples", "fresh apple", "fresh apples", "frozen apple", "frozen apples",
            "apple puree", "apple pulp", "apple sauce", "granny smith apple", "granny smith apples",
            "honeycrisp apple", "honeycrisp apples", "gala apple", "gala apples",
            "cooking apple", "cooking apples", "eating apple", "eating apples"
        ],
        "ai_name": "apple"
    },
    
    "pear": {
        "variations": [
            "pear", "pears", "fresh pear", "fresh pears", "frozen pear", "frozen pears",
            "pear puree", "pear pulp", "pear sauce", "bartlett pear", "bartlett pears",
            "anjou pear", "anjou pears", "bosc pear", "bosc pears", "asian pear", "asian pears"
        ],
        "ai_name": "pear"
    },
    
    "quince": {
        "variations": [
            "quince", "quinces", "fresh quince", "fresh quinces", "quince puree", "quince pulp",
            "quince paste", "quince jam", "quince preserve"
        ],
        "ai_name": "quince"
    },
    
    "fig": {
        "variations": [
            "fig", "figs", "fresh fig", "fresh figs", "dried fig", "dried figs",
            "fig puree", "fig pulp", "fig jam", "fig preserve", "black fig", "black figs",
            "green fig", "green figs", "brown turkey fig", "brown turkey figs"
        ],
        "ai_name": "fig"
    },
    
    "rhubarb": {
        "variations": [
            "rhubarb", "fresh rhubarb", "frozen rhubarb", "rhubarb puree", "rhubarb pulp",
            "rhubarb jam", "rhubarb preserve", "rhubarb compote", "rhubarb sauce"
        ],
        "ai_name": "rhubarb"
    },
    
    "grape": {
        "variations": [
            "grape", "grapes", "fresh grape", "fresh grapes", "frozen grape", "frozen grapes",
            "grape puree", "grape pulp", "grape juice", "concord grape", "concord grapes",
            "red grape", "red grapes", "green grape", "green grapes", "black grape", "black grapes"
        ],
        "ai_name": "grape"
    },
    
    "kiwi": {
        "variations": [
            "kiwi", "kiwis", "kiwi fruit", "kiwi fruits", "fresh kiwi", "fresh kiwis",
            "frozen kiwi", "frozen kiwis", "kiwi puree", "kiwi pulp", "golden kiwi", "golden kiwis"
        ],
        "ai_name": "kiwi"
    }
}

def get_fruit_variations():
    """
    Get all fruit variations as a flat list for easy searching.
    
    Returns:
        dict: Dictionary mapping variation -> ai_name
    """
    variation_map = {}
    for ai_name, fruit_data in FRUIT_MAP.items():
        for variation in fruit_data["variations"]:
            variation_map[variation.lower()] = ai_name
    return variation_map

def get_ai_name_for_variation(variation):
    """
    Get the standardized AI name for a fruit variation.
    
    Args:
        variation (str): The fruit variation to look up
        
    Returns:
        str: The standardized AI name, or None if not found
    """
    variation_map = get_fruit_variations()
    return variation_map.get(variation.lower())

def get_all_ai_names():
    """
    Get all standardized AI names.
    
    Returns:
        list: List of all AI names
    """
    return list(FRUIT_MAP.keys())

def extract_fruits_from_text(text):
    """
    Extract all fruits mentioned in a text string.
    
    Args:
        text (str): Text to search for fruits
        
    Returns:
        list: List of unique AI names found in the text
    """
    variation_map = get_fruit_variations()
    found_fruits = set()
    
    text_lower = text.lower()
    
    # Search for each variation
    for variation, ai_name in variation_map.items():
        if variation in text_lower:
            found_fruits.add(ai_name)
    
    return list(found_fruits)

if __name__ == "__main__":
    # Test the fruit mapping system
    print("Testing fruit mapping system...")
    
    # Test variation lookup
    test_variations = [
        "strawberries",
        "fresh blueberries", 
        "dragon fruit",
        "pitaya",
        "strawberry rhubarb",
        "not a fruit"
    ]
    
    for variation in test_variations:
        ai_name = get_ai_name_for_variation(variation)
        print(f"'{variation}' -> {ai_name}")
    
    # Test text extraction
    test_text = "This recipe uses fresh strawberries, frozen blueberries, and dragon fruit puree"
    found_fruits = extract_fruits_from_text(test_text)
    print(f"\nText: '{test_text}'")
    print(f"Found fruits: {found_fruits}")
    
    print(f"\nTotal fruits in mapping: {len(FRUIT_MAP)}")
    print(f"Total variations: {len(get_fruit_variations())}")
