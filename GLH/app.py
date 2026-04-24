# app.py
from flask import Flask, app, flash, render_template, redirect, url_for, request
from flask_wtf.csrf import CSRFError
from flask_talisman import Talisman
from config import Config
from extensions import login_manager, csrf, migrate, limiter, db
from werkzeug.exceptions import HTTPException
from models import User 
import os 

# --- Create Flask app instance ---
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.from_object(Config)

# --- security headers (CSP example) ---
csp = {
    "default-src": ["'self'"],
    "img-src": ["'self'", "data:"],
    "style-src": ["'self'", "'unsafe-inline'"],
    "script-src": ["'self'"],
    "connect-src": ["'self'"]
}

#--- Apply Talisman for security headers ---
Talisman(app, content_security_policy=csp, force_https=False)  # set True in prod
# init extensions
db.init_app(app)
login_manager.init_app(app)
csrf.init_app(app)
migrate.init_app(app, db)
limiter.init_app(app)

# --- User loader for Flask-Login ---  
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"

# ---- register blueprints -----
from admin import admin_bp
from auth import auth_bp
from public import public_bp
from customer import customer_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(public_bp)
app.register_blueprint(customer_bp, url_prefix="/customer")

# debug: dump all routes at startup
@app.before_request
def _dump_routes_once():
    if not getattr(app, "_routes_dumped", False):
        print("\n=== ROUTES (endpoint -> url) ===")
        for r in app.url_map.iter_rules():
            print(f"{r.endpoint:25} -> {r.rule}")
        print("================================\n")
        app._routes_dumped = True

print("Using database file:", os.path.abspath(
    app.config['SQLALCHEMY_DATABASE_URI'].replace("sqlite:///", "")
))


# --- Error handlers ---

# CSRF errors (missing, invalid, expired, wrong referer, etc.)
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    flash(f"Form security check failed: {e.description}", "error")
    # Avoid redirect loops if referrer is same page
    referrer = request.referrer or url_for("public.home")
    return redirect(referrer), 400

# Too many requests (rate limiting)
@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template("public/error-429.html", error=e), 429

# Handle all HTTP errors (404, 405, etc.) with a generic page
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return render_template("public/error-500.html", error=e.description), e.code



#--- Run the app ---
if __name__ == "__main__":
    app.run(debug=False)