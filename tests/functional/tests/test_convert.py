import pytest

from app.settings import settings
from tests.functional.misc.models import QuoteModel
from tests.functional.utils.dt_utils import get_milliseconds_timestamp

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    "quote,amount",
    [
        (QuoteModel(from_currency="BTC", to_currency="ETH", rate=2), 2),
        (QuoteModel(from_currency="BTC", to_currency="USDT", rate=5), 2),
        (QuoteModel(from_currency="USDT", to_currency="XMR", rate=3), 3),
    ],
)
async def test_convert_success(app_client, redis_helper, quote: QuoteModel, amount: float) -> None:
    await redis_helper.add_quote(from_currency=quote.from_currency, to_currency=quote.to_currency, rate=quote.rate)
    result = (
        await app_client.convert(
            amount=amount, from_currency=quote.from_currency.lower(), to_currency=quote.to_currency.lower()
        )
    )["result"]
    assert result["amount"] == amount * quote.rate
    assert result["rate"] == quote.rate


async def test_convert_timestamp_success(app_client, redis_helper) -> None:
    from_currency = "BTC"
    to_currency = "ETH"
    timestamp = get_milliseconds_timestamp()
    await redis_helper.add_quote(
        from_currency=from_currency, to_currency=to_currency, rate=1, timestamp=timestamp - (60 * 1000)
    )
    await redis_helper.add_quote(
        from_currency=from_currency, to_currency=to_currency, rate=2, timestamp=timestamp - (30 * 1000)
    )
    await redis_helper.add_quote(from_currency=from_currency, to_currency=to_currency, rate=3, timestamp=timestamp)

    result = (
        await app_client.convert(
            amount=5, from_currency=from_currency, to_currency=to_currency, timestamp=timestamp - (29 * 1000)
        )
    )["result"]
    assert result["rate"] == 2
    assert result["amount"] == 10

    result = (
        await app_client.convert(
            amount=5, from_currency=from_currency, to_currency=to_currency, timestamp=timestamp - (60 * 1000)
        )
    )["result"]
    assert result["rate"] == 1
    assert result["amount"] == 5

    result = (
        await app_client.convert(amount=5, from_currency=from_currency, to_currency=to_currency, timestamp=timestamp)
    )["result"]
    assert result["rate"] == 3
    assert result["amount"] == 15


@pytest.mark.parametrize(
    "quote,amount",
    [
        (QuoteModel(from_currency="BTC", to_currency="ETH", rate=2), 2),
        (QuoteModel(from_currency="BTC", to_currency="USDT", rate=5), 2),
        (QuoteModel(from_currency="USDT", to_currency="XMR", rate=3), 3),
    ],
)
async def test_convert_reverse_success(app_client, redis_helper, quote: QuoteModel, amount: float) -> None:
    await redis_helper.add_quote(from_currency=quote.to_currency, to_currency=quote.from_currency, rate=quote.rate)
    result = (
        await app_client.convert(amount=amount, from_currency=quote.from_currency, to_currency=quote.to_currency)
    )["result"]
    reversed_rate = round(1 / quote.rate, 12)
    assert result["amount"] == (amount * reversed_rate)
    assert result["rate"] == reversed_rate


async def test_covert_amount_precision_validation(app_client) -> None:
    await app_client.convert(amount=1.2222222, from_currency="ETH", to_currency="BTC", status_code=422)


@pytest.mark.parametrize(
    "quote,amount",
    [
        (QuoteModel(from_currency="BTC", to_currency="ETH", rate=2), 2),
        (QuoteModel(from_currency="BTC", to_currency="USDT", rate=5), 2),
        (QuoteModel(from_currency="USDT", to_currency="XMR", rate=3), 3),
    ],
)
async def test_quotes_are_outdated_error(app_client, redis_helper, quote: QuoteModel, amount: float) -> None:
    await redis_helper.add_quote(
        from_currency=quote.from_currency,
        to_currency=quote.to_currency,
        rate=1,
        timestamp=get_milliseconds_timestamp() - (settings.quote.quote_outdated_secs * 1000 + 1),
    )
    result = await app_client.convert(
        amount=amount, from_currency=quote.from_currency, to_currency=quote.to_currency, status_code=400
    )
    assert result["message"] == "Quotes are outdated"


async def test_convert_quotes_not_found_error(app_client) -> None:
    response = await app_client.convert(amount=1, from_currency="ETH", to_currency="BTC", status_code=404)
    assert response["message"] == "Quotes not found"
