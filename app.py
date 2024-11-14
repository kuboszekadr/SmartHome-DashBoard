import os

from src import app
from src.index import *

# Run the app
if __name__ == '__main__':
    app.run_server(
        host='0.0.0.0',
        port=os.getenv('app_port', 8050),
        debug=True,
    )