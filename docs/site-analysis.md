# Site Analysis - Jam Hot Project

## Essential Data Fields (Universal Across All Sites)

Based on analysis of Allrecipes.com, Ball Canning, and Food.com, these fields are present on all three sites and are essential for our database:

### Essential Recipe Data (Required for Database Entry):
1. **Title** - Recipe name
2. **Ingredients** - Structured list with quantities and descriptions
3. **Instructions** - Step-by-step directions
4. **Rating** - User rating system (stars or numerical)
5. **Review Count** - Number of reviews
6. **Recipe URL** - Original source URL for linking back
7. **Primary Image** - Main recipe photo/thumbnail

### Nice-to-Have Data (Optional but Valuable):
- **Servings/Yield** - Number of servings or jars
- **Time Information** - Prep time, cook time, or total time

### Recipe Ranking Strategy:
- **Primary ranking**: Use ratings and review counts to determine recipe popularity
- **Secondary ranking**: Use views/impressions if available
- **Fallback**: For obscure combinations, keep top 3 even if lower rated

## Site-Specific Variations

### Time Field Handling:
- **Allrecipes & Ball Canning**: Separate prep time and cook time
- **Food.com**: Combined "Ready In" time
- **Database approach**: Store as separate fields, normalize during scraping

### Rating Systems:
- **Allrecipes**: 4.5 stars with review count
- **Ball Canning**: No visible rating in analyzed recipe
- **Food.com**: 4.84 stars with 74 reviews
- **Database approach**: Normalize to decimal (0.0-5.0) scale

### Yield Format:
- **Allrecipes**: "Makes 4 half-pint jars"
- **Ball Canning**: "Makes about 6 (8-oz) half pints"
- **Food.com**: "7 8oz jars"
- **Database approach**: Store as text, extract numeric values for sorting

## Database Schema Implications

Our current schema handles these essential fields well:
- `title`, `ingredients`, `instructions`, `servings` - Direct mapping
- `prep_time`, `cook_time`, `total_time` - Time handling
- `rating`, `views` - For recipe ranking
- `source`, `source_url` - Track origin site

The scraper will need to:
1. Normalize time fields (combine prep+cook if only total available)
2. Convert ratings to decimal scale
3. Extract numeric values from yield text for sorting
4. Handle missing ratings gracefully

## Next Steps

1. **Refine database schema** based on these essential fields
2. **Build core scraper** for one site (Allrecipes) with these fields
3. **Test data extraction** and normalization
4. **Scale to other sites** once core functionality is proven

---
*This analysis was updated on 2025-09-21-2115 based on actual HTML data from all three target sites.*