""" Start Application """ 
from app import app

if __name__ == '__main__':
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.01'
    PORT = int(os.environ.get('PORT', 5000)) 
    app.run(host=HOST, port=PORT, debug=True)