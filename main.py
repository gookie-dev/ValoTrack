#!/usr/bin/python3
import app as flask


if __name__ == '__main__':
    flask.app.run(host='0.0.0.0', port=80, debug=True)