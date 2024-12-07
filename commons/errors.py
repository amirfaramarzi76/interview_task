class ErrorMessages:
    @staticmethod
    def invalid_json_format():
        return {"status": "error", "message": "Invalid JSON format in the file."}

    @staticmethod
    def zmq_error(message):
        return {"status": "error", "message": f"ZMQ error occurred: {message}"}

    @staticmethod
    def unexpected_error(message):
        return {"status": "error", "message": f"An unexpected error occurred: {message}"}
