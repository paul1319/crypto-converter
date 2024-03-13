import argparse

import uvicorn
import uvloop

from app.infrastructure.logging import setup_logging
from app.quote_consumer_app import QuoteConsumerApp
from app.settings import settings

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="API for converting crypro currencies")
    parser.add_argument("mode", choices=("api", "quote-consumer"))
    args = parser.parse_args()

    setup_logging(settings=settings.logging)

    if args.mode == "api":
        uvicorn.run(
            "app.api_app:build_api_app",
            reload=settings.server.reload,
            host=settings.server.host,
            port=settings.server.port,
        )
    elif args.mode == "quote-consumer":
        app = QuoteConsumerApp()
        uvloop.run(app.run())
    else:
        raise ValueError("Invalid mode to run")
