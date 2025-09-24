# Fruit Profile Creation Specification

## Overview
This specification defines the framework for creating accurate, factual fruit profiles for the Jam Hot application. All data must be scientifically verified and sourced from reliable sources.

## Data Sources

### Primary Sources (Required)
1. **USDA FoodData Central** - Nutritional data
   - URL: https://fdc.nal.usda.gov/
   - Use for: Sugar content, fiber, water content, vitamins, minerals

2. **Scientific Literature** - Pectin and acidity data
   - Search terms: "[fruit name] pectin content", "[fruit name] pH acidity"
   - Use for: Pectin content (mg/100g), pH levels

3. **Botanical References** - Plant information
   - Sources: Britannica, USDA Plants Database, scientific papers
   - Use for: Scientific names, descriptions, plant family

### Secondary Sources (Supporting)
1. **Extension Services** - Practical information
   - University extension websites (.edu domains)
   - Use for: Storage tips, preparation methods, season information

2. **Unsplash** - Images
   - URL: https://unsplash.com/
   - Search: "[fruit name] fruit"
   - License: Unsplash License (free to use)

## Profile Structure

### Required Fields
```json
{
  "fruit_id": 1,
  "scientific_name": "Fragaria × ananassa",
  "description": "Factual botanical description",
  "country_of_origin": "Country or region of origin",
  "flavor_profile": {
    "sweet": 8,
    "tart": 6,
    "acidic": 4,
    "floral": 3,
    "earthy": 2,
    "notes": "Factual flavor characteristics"
  },
  "season": "Accurate seasonal information",
  "storage_tips": "Scientifically-based storage advice",
  "preparation": "Practical preparation methods",
  "jam_properties": {
    "sugar_content": 4.9,
    "pectin_content": 30,
    "acidity": 3.25,
    "water_content": 91,
    "fiber": 2.0
  },
  "image_url": "https://images.unsplash.com/photo-...",
  "created_date": "2025-09-24T09:29:00Z"
}
```

## Data Collection Process

### Step 1: Nutritional Data (USDA FoodData Central)
1. Search for the fruit in USDA FoodData Central
2. Use "Raw" or "Fresh" entries only
3. Extract per 100g values:
   - Sugar content (g)
   - Fiber (g)
   - Water content (%)
   - Vitamins (mg/μg)
   - Minerals (mg)

### Step 2: Jam-Making Properties
1. **Pectin Content**: Search scientific literature for "[fruit name] pectin content mg/100g"
2. **Acidity (pH)**: Search for "[fruit name] pH acidity level"
3. **Sugar Content**: Use USDA data
4. **Water Content**: Use USDA data
5. **Fiber**: Use USDA data

### Step 3: Botanical Information
1. **Scientific Name**: Verify from USDA Plants Database or botanical references
2. **Description**: Write factual botanical description based on scientific sources
3. **Country of Origin**: Research the native region or country where the fruit originated
4. **Plant Family**: Include if relevant

### Step 4: Practical Information
1. **Season**: Research actual growing/harvest seasons
2. **Storage Tips**: Use extension service recommendations
3. **Preparation**: Use established food safety guidelines

### Step 5: Flavor Profile
1. **Subjective Ratings**: Use 1-10 scale based on known characteristics
2. **Notes**: Use factual flavor descriptions from scientific sources

### Step 6: Image
1. Search Unsplash for "[fruit name] fruit"
2. Choose high-quality, clear image
3. Verify image is actually of the correct fruit
4. Use direct Unsplash image URL

## Quality Assurance Checklist

### Factual Accuracy
- [ ] All nutritional data sourced from USDA FoodData Central
- [ ] Pectin content verified from scientific literature
- [ ] pH/acidity data from scientific sources
- [ ] Scientific name verified from botanical database
- [ ] Description based on botanical facts
- [ ] Season information accurate for the fruit
- [ ] Storage tips from reliable sources
- [ ] Preparation methods follow food safety guidelines

### Data Completeness
- [ ] All required fields present
- [ ] Country of origin is specified
- [ ] All jam_properties fields have values
- [ ] Image URL is valid and accessible
- [ ] Flavor profile has all required ratings
- [ ] Created date is accurate

### Source Verification
- [ ] USDA data properly cited
- [ ] Scientific literature sources noted
- [ ] Extension service sources verified
- [ ] Image source is Unsplash with proper license

## Flavor Profile Guidelines

### Rating Scale (1-10)
- **Sweet**: Based on sugar content and taste perception
- **Tart**: Based on acidity and taste perception
- **Acidic**: Based on pH levels and taste perception
- **Floral**: Based on aromatic compounds
- **Earthy**: Based on soil-influenced flavors

### Rating Guidelines
- Use scientific data as baseline
- Consider taste perception studies
- Be consistent across fruits
- Use whole numbers only
- Avoid extreme values (1 or 10) unless scientifically justified

## Common Fruits Priority List

### High Priority (Jam-Making Common)
1. Strawberry ✅ (Complete)
2. Blueberry
3. Apple
4. Peach
5. Cherry
6. Raspberry
7. Blackberry
8. Plum
9. Apricot
10. Orange

### Medium Priority
11. Lemon
12. Lime
13. Grape
14. Pear
15. Fig

### Low Priority
16. Kiwi
17. Mango
18. Pineapple
19. Cranberry
20. Rhubarb

## Error Prevention

### Common Mistakes to Avoid
1. **Don't estimate nutritional values** - Always use USDA data
2. **Don't guess pectin content** - Must be from scientific sources
3. **Don't make up pH levels** - Must be from scientific literature
4. **Don't use generic descriptions** - Must be specific to the fruit
5. **Don't use copyrighted images** - Only use Unsplash or public domain
6. **Don't assume seasonal information** - Research actual growing seasons
7. **Don't create flavor profiles without basis** - Use scientific taste data

### Validation Steps
1. Cross-reference all data with multiple sources
2. Verify scientific names with botanical databases
3. Check image URLs are accessible
4. Ensure all values are within reasonable ranges
5. Validate that descriptions are factual, not marketing copy

## Template for New Fruit Profiles

```json
{
  "fruit_id": [NEXT_ID],
  "scientific_name": "[VERIFIED_BOTANICAL_NAME]",
  "description": "[FACTUAL_BOTANICAL_DESCRIPTION]",
  "country_of_origin": "[NATIVE_COUNTRY_OR_REGION]",
  "flavor_profile": {
    "sweet": [1-10_BASED_ON_SUGAR_CONTENT],
    "tart": [1-10_BASED_ON_ACIDITY],
    "acidic": [1-10_BASED_ON_PH],
    "floral": [1-10_BASED_ON_AROMATIC_COMPOUNDS],
    "earthy": [1-10_BASED_ON_SOIL_INFLUENCE],
    "notes": "[FACTUAL_FLAVOR_CHARACTERISTICS]"
  },
  "season": "[ACCURATE_SEASONAL_INFORMATION]",
  "storage_tips": "[SCIENTIFICALLY_BASED_STORAGE_ADVICE]",
  "preparation": "[PRACTICAL_PREPARATION_METHODS]",
  "jam_properties": {
    "sugar_content": [USDA_DATA_G_PER_100G],
    "pectin_content": [SCIENTIFIC_LITERATURE_MG_PER_100G],
    "acidity": [SCIENTIFIC_LITERATURE_PH],
    "water_content": [USDA_DATA_PERCENTAGE],
    "fiber": [USDA_DATA_G_PER_100G]
  },
  "image_url": "https://images.unsplash.com/photo-[UNSPLASH_ID]",
  "created_date": "[CURRENT_TIMESTAMP]"
}
```

## Success Criteria

A fruit profile is complete when:
1. All data is scientifically verified
2. All sources are documented
3. All required fields are present
4. Image is accessible and properly licensed
5. Data is consistent with known fruit characteristics
6. Profile follows the established framework
7. Quality assurance checklist is completed

---

*This specification was created on 2025-09-24-0929 to ensure consistent, factual fruit profiles for the Jam Hot application.*
