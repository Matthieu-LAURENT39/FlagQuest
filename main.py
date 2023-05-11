import mimetypes

from flagquest import create_app

mimetypes.add_type("application/javascript", ".js")

app = create_app()

if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)
