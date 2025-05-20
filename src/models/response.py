from flask import jsonify


class ResponseInfo:

    @classmethod
    def to_response(cls, tuple_response: tuple[any, str, int]):
        return (
            jsonify({"response": tuple_response[0], "message": tuple_response[1]}),
            tuple_response[2],
        )
