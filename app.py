# Standard Library Imports
import os

# Third-Party Library Imports
from flask import Flask, render_template

# Local Appliation Imports
from extensions import postgres_db, init_mongo
from routes import employee_bp, chat_bp, rag_bp

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQL_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    postgres_db.init_app(app)
    init_mongo()
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
        postgres_db.create_all()
        print("Tables created...")
    
    # Run the flask app
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()