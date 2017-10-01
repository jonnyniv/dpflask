from flask import Flask, request, jsonify
from dpflask import db

app = Flask(__name__)


@app.route('/')
def test():
    return 'Flask test'


@app.route('/get_voters_where', methods=['GET'])
def get_voters():
    args = request.args
    result = db.get_voters_where(county=args.get('county'),
                                 month=args.get('month'),
                                 party=args.get('party'),
                                 status=args.get('status'),
                                 limit=args.get('limit'))
    return jsonify(result)


if __name__ == '__main__':
    app.run()