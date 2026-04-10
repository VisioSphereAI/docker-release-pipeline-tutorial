from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "bad_request", "message": str(error)}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "not_found", "message": "The requested resource was not found."}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "method_not_allowed", "message": str(error)}), 405

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "internal_server_error", "message": "An unexpected error occurred."}), 500
