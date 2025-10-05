import argparse

from loguru import logger


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run the CO2ral app.")
    parser.add_argument("--debug", action="store_true", help="Run the app in debug mode.")
    args = parser.parse_args()

    # Import and run the Flask app
    from app import app

    if args.debug:
        logger.info("Running App in debug mode")
        app.run(debug=True, use_reloader=False)
    else:
        logger.info("Running App in production mode")
        app.run(use_reloader=True)
