from flask import Flask
from config import Config
from flask_login import LoginManager
from models import db, User  # ✅ db & User from models



# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
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

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

# Entry point
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
