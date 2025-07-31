import json
import pandas as pd
import re
from collections import defaultdict


with open('response_data.json', 'r') as f:
    data = json.load(f)

products = data['data']['hits']

# Process each product to extract information
processed_products = []

for product in products:
    # Extract size/volume from OptionMap if available
    size = ''
    if 'OptionMap' in product and product['OptionMap']:
        if 'Size' in product['OptionMap']:
            size = product['OptionMap']['Size']
        elif 'Style' in product['OptionMap']:
            size = product['OptionMap']['Style']
    
    # Extract ingredients from product text
    text = product['text'].lower()
    ingredients = []
    
    # Common skincare ingredients to look for
    common_ingredients = [
        'niacinamide', 'ceramides', 'hyaluronic acid', 'glycolic acid', 
        'salicylic acid', 'bha', 'aha', 'zinc oxide', 'aloe vera', 
        'coconut oil', 'vitamin c', 'alpha arbutin', 'kojic acid', 'b5'
    ]

    for ing in common_ingredients:
        if ing in text:
            ingredients.append(ing.title())
    
    # Create product dictionary
    product_dict = {
        'Product ID': product['skid'],
        'Product Line Name': product.get('rankName', ''),
        'Brand Name': product['brand'],
        'Product Name': product['text'],
        'Product Images': product['image'],
        'Price': f"${product['price']/100:.2f}" if product['price'] else '',
        'Size/Volume': size,
        'Ingredients': ', '.join(ingredients) if ingredients else '',
        'Source URL': f"https://snapklik.com/product/{product['slug']}"
    }

    processed_products.append(product_dict)

# Create DataFrame
df = pd.DataFrame(processed_products)

# Save to CSV
df.to_csv('skincare_products.csv', index=False)

print(df)

# Part 2: Group products by shared ingredients

# Create a list of tuples containing product names and their ingredient sets
product_ingredients = []
for _, row in df.iterrows():
    if row['Ingredients']:
        ingredients = {ing.strip() for ing in row['Ingredients'].split(',')}
        product_ingredients.append((row['Product Name'], ingredients))

# Find groups of products sharing at least 2 ingredients
groups = []
used_products = set()

# Sort products by number of ingredients to start with most informative ones first
product_ingredients.sort(key=lambda x: -len(x[1]))

for i, (prod1, ing_set1) in enumerate(product_ingredients):
    if prod1 in used_products:
        continue
        
    # Find all products that share at least 2 ingredients with this product
    group_products = [prod1]
    shared_ingredients = ing_set1.copy()
    
    for j, (prod2, ing_set2) in enumerate(product_ingredients[i+1:], i+1):
        if prod2 in used_products:
            continue
            
        common_ingredients = ing_set1 & ing_set2
        if len(common_ingredients) >= 2:
            group_products.append(prod2)
            shared_ingredients &= ing_set2  # Keep only ingredients shared by all
            used_products.add(prod2)
    
    if len(group_products) >= 2:
        groups.append({
            'Group': chr(65 + len(groups)),  # A, B, C, etc.
            'Shared Ingredients': ', '.join(sorted(shared_ingredients)),
            'Product Names': '; '.join(group_products)
        })

# Create DataFrame from groups
grouped_df = pd.DataFrame(groups)

# Save and display results
grouped_df.to_csv('ingredient_groups.csv', index=False)
print("\nGrouped Products by Shared Ingredients:")
print(grouped_df)