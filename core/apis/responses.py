from flask import Response, jsonify, make_response


# class APIResponse(Response):
#     @classmethod
#     def respond(cls, data):
#         return make_response(jsonify(data=data))
    
class APIResponse:
    @staticmethod
    def respond(data=None, error=None, status_code=200):
        response = {
            "data": data,
            "error": error
        }
        return jsonify(response), status_code
