import sys
sys.path.insert(0, '/var/www/trade_app/app')
from site import application

if __name__ == "__main__":
    application.run()
