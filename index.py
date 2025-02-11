from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/") 
db = client["sampleDB"]
collection = db["sample"]

@app.route("/conversations", methods=["GET"])
def get_all_data():
    try:
        data = list(collection.find({}, {"_id": 0}))
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@app.route('/conversations/<string:conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    try:

        result = collection.delete_one({"conversation_id": conversation_id})

        if result.deleted_count == 0:
            return jsonify({"error": "Conversation not found"}), 404

        return jsonify({"message": "Conversation deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
