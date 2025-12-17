from waitress import serve


if __name__ == "__main__":
    # Import the app.
    from app import app

    # Serve app
    serve(app.server, host="127.0.0.1", port=8050)
