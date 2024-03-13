# Crypto Converter

## Introduction

Crypto Converter is a service designed to calculate cryptocurrency conversions using live exchange rates. It focuses on providing accurate, real-time conversion
calculations between different cryptocurrencies.

## Architecture

The project consists of two primary parts:

1. **Currency Conversion API**: API that offers a conversion service, accepting requests with parameters for the
amount and currencies to convert between. It responds with the converted amount and the exchange rate used.
2. **Quote Consumer**: A service that fetches real-time cryptocurrency data from Binance.


## Prerequisites

* Docker and Docker Compose 

## Installation & Running

1. Clone the repository
2. Configure Environment Variables
The .env file is in the project `/app` directory with necessary configurations.

3. Start the Project
    ```shell
    docker-compose up
    ```
   This will start the Currency Conversion API and Quote Consumer.

## Usage
* To convert cryptocurrency, send a GET request to the Currency Conversion API with the desired amount and currencies.
Example:
   ```
   http://<API_HOST>:<API_PORT>/api/v1/convert?amount=1.0&from=BTC&to=ETH
   ```
Development & Testing

* Run tests with:
   ```shell
   make tests
   ```
Make sure you are in the root folder.