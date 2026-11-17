from flask import Blueprint, jsonify, render_template
from app.models import Product, Category

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "BeastEats",
        "version": "1.0.0"
    }), 200


@main.route("/api/menu")
def menu():
    products = Product.query.filter_by(is_available=True).all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": float(p.price),
            "category": p.category.name,
            "image_url": p.image_url,
            "serving_size_g": float(p.serving_size_g) if p.serving_size_g is not None else None,
            "protein_g": float(p.protein_g) if p.protein_g is not None else None,
            "carbs_g": float(p.carbs_g) if p.carbs_g is not None else None,
            "calories_kcal": float(p.calories_kcal) if p.calories_kcal is not None else None,
            "fibre_g": float(p.fibre_g) if p.fibre_g is not None else None
        }
        for p in products
    ])

@main.route("/api/categories")
def categories():
    items = Category.query.all()

    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "description": c.description
        }
        for c in items
    ])
