import json
import random

categories = {
    "Electronics": {
        "items": ["Laptop", "Smartphone", "Tablet", "Smartwatch", "Headphones", "Camera", "Monitor", "Keyboard", "Mouse", "Speaker"],
        "brands": ["TechPro", "Digital", "SmartTech", "ElectroMax", "GadgetHub"],
        "tags": ["wireless", "bluetooth", "4K", "HD", "portable", "gaming", "professional", "budget", "premium", "compact"]
    },
    "Books": {
        "items": ["Novel", "Textbook", "Biography", "Cookbook", "Guide", "Manual", "Encyclopedia", "Dictionary", "Atlas", "Journal"],
        "topics": ["Science", "History", "Fiction", "Technology", "Art", "Business", "Health", "Travel", "Philosophy", "Psychology"],
        "tags": ["bestseller", "educational", "reference", "illustrated", "hardcover", "paperback", "digital", "classic", "modern", "comprehensive"]
    },
    "Clothing": {
        "items": ["Shirt", "Pants", "Jacket", "Dress", "Shoes", "Hat", "Scarf", "Sweater", "Jeans", "Coat"],
        "styles": ["Casual", "Formal", "Sport", "Vintage", "Modern", "Classic", "Trendy", "Elegant", "Comfortable", "Stylish"],
        "tags": ["cotton", "leather", "waterproof", "breathable", "stretchable", "designer", "handmade", "eco-friendly", "durable", "lightweight"]
    },
    "Food": {
        "items": ["Pasta", "Rice", "Bread", "Cheese", "Chocolate", "Coffee", "Tea", "Juice", "Snacks", "Cereal"],
        "types": ["Organic", "Gluten-Free", "Vegan", "Sugar-Free", "Whole Grain", "Natural", "Premium", "Artisan", "Fresh", "Frozen"],
        "tags": ["healthy", "nutritious", "delicious", "imported", "local", "gourmet", "instant", "homemade", "traditional", "exotic"]
    },
    "Home": {
        "items": ["Sofa", "Table", "Chair", "Lamp", "Rug", "Curtain", "Bed", "Shelf", "Mirror", "Vase"],
        "styles": ["Modern", "Rustic", "Minimalist", "Industrial", "Scandinavian", "Traditional", "Contemporary", "Vintage", "Bohemian", "Luxury"],
        "tags": ["wooden", "metal", "glass", "fabric", "handcrafted", "space-saving", "adjustable", "decorative", "functional", "elegant"]
    },
    "Sports": {
        "items": ["Ball", "Racket", "Shoes", "Bag", "Bottle", "Mat", "Weights", "Bike", "Helmet", "Gloves"],
        "activities": ["Running", "Cycling", "Swimming", "Yoga", "Tennis", "Football", "Basketball", "Hiking", "Gym", "Boxing"],
        "tags": ["professional", "beginner", "outdoor", "indoor", "waterproof", "ergonomic", "adjustable", "durable", "lightweight", "high-performance"]
    },
    "Beauty": {
        "items": ["Cream", "Serum", "Shampoo", "Conditioner", "Lipstick", "Perfume", "Lotion", "Mask", "Oil", "Spray"],
        "types": ["Anti-Aging", "Moisturizing", "Nourishing", "Brightening", "Hydrating", "Cleansing", "Soothing", "Revitalizing", "Protecting", "Repairing"],
        "tags": ["natural", "organic", "dermatologist-tested", "hypoallergenic", "fragrance-free", "paraben-free", "cruelty-free", "vegan", "luxury", "clinical"]
    },
    "Toys": {
        "items": ["Puzzle", "Doll", "Car", "Robot", "Game", "Block", "Bear", "Train", "Plane", "Ball"],
        "ages": ["Toddler", "Preschool", "Kids", "Teens", "All Ages"],
        "tags": ["educational", "interactive", "creative", "electronic", "wooden", "plush", "collectible", "outdoor", "indoor", "STEM"]
    },
    "Music": {
        "items": ["Guitar", "Piano", "Drum", "Violin", "Microphone", "Amplifier", "Synthesizer", "Flute", "Saxophone", "Ukulele"],
        "types": ["Acoustic", "Electric", "Digital", "Classical", "Professional", "Student", "Portable", "Studio", "Stage", "Practice"],
        "tags": ["beginner-friendly", "professional-grade", "compact", "full-size", "wireless", "vintage", "modern", "handcrafted", "affordable", "premium"]
    },
    "Garden": {
        "items": ["Seeds", "Tools", "Pot", "Fertilizer", "Hose", "Gloves", "Soil", "Planter", "Sprinkler", "Trimmer"],
        "types": ["Organic", "Indoor", "Outdoor", "Decorative", "Functional", "Automatic", "Manual", "Electric", "Eco-Friendly", "Professional"],
        "tags": ["durable", "rust-resistant", "ergonomic", "lightweight", "heavy-duty", "compact", "expandable", "weather-resistant", "biodegradable", "sustainable"]
    }
}

dataset = []
for i in range(200):
    cat = random.choice(list(categories.keys()))
    cat_data = categories[cat]
    
    item = random.choice(cat_data["items"])
    
    if cat == "Books":
        variant = random.choice(cat_data["topics"])
    elif cat == "Toys":
        variant = random.choice(cat_data["ages"])
    elif "brands" in cat_data:
        variant = random.choice(cat_data["brands"])
    elif "types" in cat_data:
        variant = random.choice(cat_data["types"])
    elif "styles" in cat_data:
        variant = random.choice(cat_data["styles"])
    else:
        variant = random.choice(cat_data["activities"])
    
    title = f"{variant} {item}"
    
    descriptions = [
        f"High-quality {item.lower()} perfect for everyday use",
        f"Premium {item.lower()} designed for maximum comfort and performance",
        f"Innovative {item.lower()} with advanced features",
        f"Durable {item.lower()} built to last",
        f"Stylish {item.lower()} that combines form and function",
        f"Professional-grade {item.lower()} for serious users",
        f"Affordable {item.lower()} without compromising quality",
        f"Versatile {item.lower()} suitable for multiple purposes",
        f"Compact {item.lower()} ideal for limited spaces",
        f"Elegant {item.lower()} that enhances any setting"
    ]
    
    description = random.choice(descriptions)
    tags = random.sample(cat_data["tags"], k=random.randint(3, 5))
    
    price = round(random.uniform(10, 500), 2)
    rating = round(random.uniform(3.5, 5.0), 1)
    stock = random.randint(0, 100)
    
    search_document = f"{title}. {description}. Tags: {', '.join(tags)}. Category: {cat}. Price: ${price}. Rating: {rating}/5. Stock: {stock} units."
    
    dataset.append({
        "id": i + 1,
        "title": title,
        "description": description,
        "tags": tags,
        "category": cat,
        "metadata": {
            "price": price,
            "rating": rating,
            "stock": stock
        },
        "search_document": search_document
    })

with open("dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)

print(f"✓ Generated {len(dataset)} records")
print(f"✓ Categories: {', '.join(categories.keys())}")
print(f"✓ Sample record:\n{json.dumps(dataset[0], indent=2)}")
