from __future__ import annotations

from flask_smorest import Blueprint
from flask.views import MethodView

from communication_api.schemas import HealthResponseSchema

blp = Blueprint("health", __name__, description="Health endpoints")


@blp.route("/health")
class HealthResource(MethodView):
    @blp.response(200, HealthResponseSchema)
    def get(self) -> dict[str, str]:
        return {"status": "ok", "service": "communication-api"}

