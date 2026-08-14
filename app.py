import os
import socket
from flask import Flask, render_template
from config import Config
from models import db
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.admin_routes import admin_bp
from routes.quiz_routes import quiz_bp

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(quiz_bp)

    # Global context processors for template convenience
    @app.context_processor
    def inject_now():
        from datetime import datetime
        return {'current_year': datetime.utcnow().year}

    # Custom Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', error_code=404, error_message="Page Not Found - The page you requested does not exist."), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error.html', error_code=500, error_message="Internal Server Error - Something went wrong on our end."), 500

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    local_ip = get_local_ip()
    print("\n" + "=" * 65)
    print(" === QuizMaster Application Server Started ===")
    print(" Universal Live Link (Cloudflare Tunnel - All Devices):")
    print(" https://vpn-fuji-robert-normally.trycloudflare.com")
    print("=" * 65 + "\n")

    app.run(host='0.0.0.0', port=5500, debug=True)
