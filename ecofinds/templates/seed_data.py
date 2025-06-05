from app import create_app
from models import db, User, Product
from werkzeug.security import generate_password_hash
from datetime import datetime

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create a sample seller
    test_user = User(
        username='seller1',
        email='seller1@example.com',
        password=generate_password_hash('password', method='pbkdf2:sha256'),
        phone='9876543210',
        verified=True
    )
    db.session.add(test_user)
    db.session.commit()

    # Sample products
    sample_products = [
        {"title": "Second-Hand Laptop", "description": "Acer laptop, 8GB RAM, SSD.", "price": 22000, "category": "Electronics", "image": "laptop.jpg"},
        {"title": "HP Pavilion Laptop", "description": "Good condition, 16GB RAM, i5 processor.", "price": 30000, "category": "Electronics", "image": "laptop2.jpg"},
        {"title": "Dell Inspiron Laptop", "description": "Reliable second-hand Dell Inspiron.", "price": 25000, "category": "Electronics", "image": "laptop3.jpg"},
        {"title": "Book Set - Wimpy Kid", "description": "Set of 10 Wimpy Kid books.", "price": 1000, "category": "Books", "image": "books.jpg"},
        {"title": "Harry Potter Book Set", "description": "Complete 7 book series.", "price": 1200, "category": "Books", "image": "harrypotter.jpg"},
        {"title": "Oxford Dictionary", "description": "Used English Oxford Dictionary.", "price": 200, "category": "Books", "image": "dictionary.jpg"},
        {"title": "Men's Denim Jacket", "description": "Stylish blue denim jacket.", "price": 1500, "category": "Fashion", "image": "jacket.jpg"},
        {"title": "Traditional Saree", "description": "Ethnic Indian saree with blouse.", "price": 1200, "category": "Fashion", "image": "saree.jpg"},
        {"title": "Kids T-shirt Pack", "description": "Pack of 3 cotton T-shirts.", "price": 600, "category": "Fashion", "image": "tshirt.jpg"},
        {"title": "Cricket Bat", "description": "Full-size Kashmir willow bat.", "price": 2000, "category": "Sports", "image": "cricketbat.jpg"},
        {"title": "Mini Cricket Bat for Kids", "description": "Plastic bat for children.", "price": 300, "category": "Sports", "image": "kidsbat.jpg"},
        {"title": "Soft Toy Teddy Bear", "description": "Brown teddy bear, 2 feet.", "price": 500, "category": "Toys", "image": "teddy.jpg"},
        {"title": "Lego Building Set", "description": "Colorful building blocks for kids.", "price": 800, "category": "Toys", "image": "lego.jpg"},
        {"title": "Toy Car", "description": "Battery operated remote car.", "price": 1000, "category": "Toys", "image": "car.jpg"}
    ]

    for product in sample_products:
        p = Product(
            title=product['title'],
            description=product['description'],
            price=product['price'],
            category=product['category'],
            image=product['image'],
            created_at=datetime.utcnow(),
            seller_id=test_user.id
        )
        db.session.add(p)

    db.session.commit()

    print("✅ Database seeded with 1 user and 14 products.")
