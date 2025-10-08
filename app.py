from flask import Flask, jsonify, request

app = Flask(__name__)

# simple in-memory "database"
ITEMS = [
    {"id": 1, "name": "Notebook"},
    {"id": 2, "name": "Pencil"}
]

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.get("/items")
def list_items():
    return jsonify(ITEMS), 200

@app.post("/items")
def create_item():
    data = request.get_json(force=True)
    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400
    new_id = max([i["id"] for i in ITEMS] or [0]) + 1
    item = {"id": new_id, "name": data["name"]}
    ITEMS.append(item)
    return jsonify(item), 201

@app.get("/items/<int:item_id>")
def get_item(item_id):
    item = next((i for i in ITEMS if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "not found"}), 404
    return jsonify(item), 200

@app.put("/items/<int:item_id>")
def update_item(item_id):
    item = next((i for i in ITEMS if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "not found"}), 404
    data = request.get_json(force=True)
    if "name" in data:
        item["name"] = data["name"]
    return jsonify(item), 200

@app.delete("/items/<int:item_id>")
def delete_item(item_id):
    global ITEMS
    before = len(ITEMS)
    ITEMS = [i for i in ITEMS if i["id"] != item_id]
    if len(ITEMS) == before:
        return jsonify({"error": "not found"}), 404
    return jsonify({"deleted": item_id}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

