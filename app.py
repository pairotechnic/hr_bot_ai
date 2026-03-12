from flask import Flask, render_template
from extensions import db
from routes import employee_bp, chat_bp, rag_bp
import os

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQL_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.register_blueprint(employee_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(rag_bp)

    @app.route("/")
    def index():
        return render_template("index.html")
    
    return app


def main():
    app = create_app()

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        print("Tables created...")
    
    # Run the flask app
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()