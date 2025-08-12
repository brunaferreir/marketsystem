from flask import Blueprint, request, jsonify
from service.items_service import ItemService

item_bp = Blueprint("item_bp", __name__)
service = ItemService()

@item_bp.route("/item", methods=["GET"])
def get_all_items():
    try:
        items = service.get_all()
        return jsonify(items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@item_bp.route("/item", methods = ["POST"])
def create_item():
    data = request.get_json()
    return service.add(data['name'])