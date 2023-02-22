import mimetypes

from site_elysium import create_app, setup_app

mimetypes.add_type("application/javascript", ".js")

app = create_app()

if __name__ == "__main__":
    setup_app(app)
    app.run("0.0.0.0", 5000, debug=True)
