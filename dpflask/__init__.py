from flask import Flask, request, jsonify

from dpflask import db

app = Flask(__name__)
connection = db.connect_db()


@app.route('/get_voters_where', methods=['GET'])
def get_voters():
    args = request.args
    result = db.get_voters_where(args, connection)
    return result


def main():
    app.run()


if __name__ == '__main__':
    main()


