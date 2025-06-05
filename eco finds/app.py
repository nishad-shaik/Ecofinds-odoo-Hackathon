from flask import Flask
from config import Config
from extensions import db, login_manager, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    migrate.init_app(app, db)

    # Register blueprints (delayed to avoid circular imports)
    from auth_routes import auth_bp
    from product_routes import product_bp
    from auction_routes import auction_bp
    from chat_routes import chat_bp
    from admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(auction_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(admin_bp)

    return app

# Main runner
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        from models import *  # ✅ Import models after app is ready
        db.create_all()
    app.run(debug=True)
