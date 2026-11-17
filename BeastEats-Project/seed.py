from decimal import Decimal

from app import create_app, db
from app.models import Category, Product

app = create_app()

menu = {
    "Breakfast": [
        ("Classic Oatmeal", "Traditional oatmeal prepared with milk.", "89"),
        ("Banana Oatmeal", "Oatmeal with fresh banana.", "99"),
        ("Berries Oatmeal", "Oatmeal with mixed berries.", "119"),
        ("Chocolate Oatmeal", "Oatmeal with chocolate.", "109"),
        ("Egg Sandwich", "Fresh sandwich filled with seasoned eggs.", "99"),
        ("Protein Pancakes", "Fluffy protein pancakes.", "129"),
        ("Boiled Egg Bowl", "Boiled eggs served in a healthy bowl.", "89"),
    ],

    "Lunch": [
        ("Grilled Chicken", "Grilled chicken breast.", "199"),
        ("Chicken 65", "Spicy crispy chicken 65.", "179"),
        ("Paneer 65", "Spicy crispy paneer 65.", "159"),
        ("Chicken Rice", "Chicken served with rice.", "189"),
        ("Paneer Rice", "Paneer served with rice.", "169"),
        ("Egg Salad", "Boiled eggs with fresh salad ingredients.", "129"),
        ("Salad", "Fresh seasonal vegetable salad.", "99"),
    ],

    "Snacks": [
        ("Classic Oatmeal", "Traditional oatmeal prepared with milk.", "89"),
        ("Banana Oatmeal", "Oatmeal with fresh banana.", "99"),
        ("Berries Oatmeal", "Oatmeal with mixed berries.", "119"),
        ("Chocolate Oatmeal", "Oatmeal with chocolate.", "109"),
        ("Peanut Butter Sandwich", "Bread sandwich with peanut butter.", "79"),
    ],

    "Dinner": [
        ("Grilled Chicken", "Grilled chicken breast.", "199"),
        ("Chicken 65", "Spicy crispy chicken 65.", "179"),
        ("Paneer 65", "Spicy crispy paneer 65.", "159"),
        ("Chicken Rice", "Chicken served with rice.", "189"),
        ("Paneer Rice", "Paneer served with rice.", "169"),
        ("Egg Salad", "Boiled eggs with fresh salad ingredients.", "129"),
        ("Salad", "Fresh seasonal vegetable salad.", "99"),
    ],
}


with app.app_context():
    db.create_all()

    if Product.query.first():
        print("Existing products detected.")
        print("No changes made to avoid duplicate records.")
    else:
        for category_name, items in menu.items():
            category = Category(name=category_name)
            db.session.add(category)
            db.session.flush()

            for name, description, price in items:
                product = Product(
                    name=name,
                    description=description,
                    price=Decimal(price),
                    category_id=category.id,
                    is_available=True,
                )
                db.session.add(product)

        db.session.commit()
        print("BeastEats menu initialized successfully!")

    print("\n===== BEASTEATS MENU SUMMARY =====")

    for category_name in menu:
        category = Category.query.filter_by(name=category_name).first()
        print(f"{category_name}: {Product.query.filter_by(category_id=category.id).count()} products")

    print("Total products:", Product.query.count())
