"""Entry point of the delivery service."""
import os

from storage import DBClient, DeliveryStatusQuery, OrderNotFoundError
from web import NotFound, View, app, register_route

LISTEN_PORT = os.getenv("LISTEN_PORT", 5000)


class DeliveryView(View):
    async def _get(self, request, delivery_id: int):
        dsq = DeliveryStatusQuery(int(delivery_id), await DBClient())
        try:
            result = await dsq.get()
        except OrderNotFoundError as e:
            raise NotFound(str(e)) from e

        return result.message()


register_route(DeliveryView, "/status/<delivery_id:int>")


def main():
    app.run(host="0.0.0.0", port=LISTEN_PORT)


if __name__ == "__main__":
    main()
