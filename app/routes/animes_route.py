from flask import Blueprint
from app.controllers import animes_controller


bp = Blueprint("animes", __name__, url_prefix="/animes")

bp.get("")(animes_controller.get_animes)
bp.get("/<anime_id>")(animes_controller.get_anime_by_id)
bp.post("")(animes_controller.add_anime)
bp.patch("/<anime_id>")(animes_controller.update_anime)
bp.delete("/<anime_id>")(animes_controller.remove_anime)
