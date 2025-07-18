from waitress import serve


if __name__ == "__main__":
    # Import the app.
    from app import app

    # Serve app
    serve(app.server, host="131.188.75.244", port=80)
