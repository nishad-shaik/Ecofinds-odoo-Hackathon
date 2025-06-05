from app import create_app
from models import db, Product, User
from datetime import datetime

app = create_app()

with app.app_context():
    user = User.query.first()

    products = [
        Product(title="Acer Laptop", description="Used but working well", price=22000, category="Electronics",
                image="laptop.jpg", seller_id=user.id),
        Product(title="Hyundai Car", description="Second-hand but efficient", price=280000, category="Other",
                image="car.jpg", seller_id=user.id),
        Product(title="Wimpy Kid Book Set", description="Complete collection", price=1000, category="Books",
                image="books.jpg", seller_id=user.id),
        Product(title="Cricket Bat", description="Lightweight professional bat", price=1800, category="Sports",
                image="bat.jpg", seller_id=user.id),
        Product(title="Toy Train Set", description="For kids 3-6 years", price=950, category="Toys",
                image="toys.jpg", seller_id=user.id),
    ]

    db.session.bulk_save_objects(products)
    db.session.commit()
    print("Products seeded successfully.")
