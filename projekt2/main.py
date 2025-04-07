import argparse
from server import ChatServer

def main():
    parser = argparse.ArgumentParser(description='Wielowątkowy serwer czatu')
    parser.add_argument('--host', default='127.0.0.1', help='Adres hosta serwera')
    parser.add_argument('--port', type=int, default=8888, help='Port serwera')
    args = parser.parse_args()
    
    # Uruchom serwer z podanymi parametrami
    server = ChatServer(host=args.host, port=args.port)
    try:
        server.start()
    except KeyboardInterrupt:
        print("Zatrzymywanie serwera...")
    finally:
        server.stop()

if __name__ == "__main__":
    main()