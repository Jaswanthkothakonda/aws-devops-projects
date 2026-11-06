from decimal import Decimal
from app import create_app, db
from app.models import Product, Category

app = create_app()

nutrition = {
    "Lunch": {
        "Grilled Chicken": (200, 40, 8, 330, 3),
        "Chicken 65": (220, 35, 18, 390, 2),
        "Paneer 65": (220, 30, 20, 430, 2),
        "Chicken Rice": (400, 38, 65, 560, 4),
        "Paneer Rice": (400, 32, 65, 620, 5),
        "Egg Salad": (300, 30, 18, 380, 5),
        "Salad": (350, 30, 35, 430, 11),
    },

    "Snacks": {
        "Classic Oatmeal": (470, 44, 100, 1046, 16),
        "Banana Oatmeal": (500, 44, 110, 1150, 17),
        "Berries Oatmeal": (500, 44, 100, 1000, 17),
        "Chocolate Oatmeal": (500, 45, 100, 1150, 16),
        "Peanut Butter Sandwich": (180, 27, 48, 430, 8),
    },

    "Dinner": {
        "Grilled Chicken": (200, 40, 8, 330, 3),
        "Chicken 65": (220, 35, 18, 390, 2),
        "Paneer 65": (220, 30, 20, 430, 2),
        "Chicken Rice": (400, 38, 65, 560, 4),
        "Paneer Rice": (400, 32, 65, 620, 5),
        "Egg Salad": (300, 30, 18, 380, 5),
        "Salad": (350, 30, 35, 430, 11),
    },
}

with app.app_context():
    updated = 0

    for category_name, products in nutrition.items():
        category = Category.query.filter_by(name=category_name).first()

        if not category:
            raise ValueError(f"Missing category: {category_name}")

        for product_name, values in products.items():
            product = Product.query.filter_by(
                name=product_name,
                category_id=category.id
            ).one_or_none()

            if not product:
                raise ValueError(
                    f"Missing product: {product_name} in {category_name}"
                )

            serving, protein, carbs, calories, fibre = values

            product.serving_size_g = Decimal(str(serving))
            product.protein_g = Decimal(str(protein))
            product.carbs_g = Decimal(str(carbs))
            product.calories_kcal = Decimal(str(calories))
            product.fibre_g = Decimal(str(fibre))

            updated += 1

    db.session.commit()

    print(f"Successfully updated {updated} products.")
    print("Prices and product names were not changed.")
