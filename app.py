import os
from line_app.main import app

if __name__ == "__main__":
    app.run(port=int(os.environment['PORT']))