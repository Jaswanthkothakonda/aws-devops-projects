from decimal import Decimal
from app import create_app, db
from app.models import Product, Category

app = create_app()

oatmeal_values = (470, 44, 100, 1046, 16)

breakfast_values = {
    "Egg Sandwich": (250, 30, 35, 430, 4),
    "Protein Pancakes": (250, 30, 55, 450, 6),
    "Boiled Egg Bowl": (250, 30, 12, 320, 3),
}

with app.app_context():
    updated = 0

    for category_name in ["Breakfast", "Snacks"]:
        category = Category.query.filter_by(name=category_name).one()

        for product_name in [
            "Classic Oatmeal",
            "Banana Oatmeal",
            "Berries Oatmeal",
            "Chocolate Oatmeal",
        ]:
            product = Product.query.filter_by(
                name=product_name,
                category_id=category.id
            ).one()

            values = oatmeal_values

            (
                product.serving_size_g,
                product.protein_g,
                product.carbs_g,
                product.calories_kcal,
                product.fibre_g
            ) = [Decimal(str(v)) for v in values]

            updated += 1

    category = Category.query.filter_by(name="Breakfast").one()

    for product_name, values in breakfast_values.items():
        product = Product.query.filter_by(
            name=product_name,
            category_id=category.id
        ).one()

        (
            product.serving_size_g,
            product.protein_g,
            product.carbs_g,
            product.calories_kcal,
            product.fibre_g
        ) = [Decimal(str(v)) for v in values]

        updated += 1

    db.session.commit()
    print(f"Successfully updated {updated} products.")
    print("Product names and prices remain unchanged.")
