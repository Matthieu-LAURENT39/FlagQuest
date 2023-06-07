import mimetypes

from flagquest import create_app

mimetypes.add_type("application/javascript", ".js")

app = create_app()

if __name__ == "__main__":
    # Serveur de développement intégré à Flask
    if app.debug:
        app.run("0.0.0.0", 5000, debug=True)
    else:
        from waitress import serve

        serve(app, host="0.0.0.0", port=5000)
