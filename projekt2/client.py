import socket  
import threading
import sys  

class ChatClient:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host 
        self.port = port 
        self.socket = None 
        self.running = False
    
    def connect(self):
        try:
            # Tworzenie socketu TCP
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Nawiązanie połączenia z serwerem
            self.socket.connect((self.host, self.port))
            self.running = True
            return True
        except Exception as e:
            print(f"Błąd połączenia: {e}")
            return False
            
    def disconnect(self):
        self.running = False 
        if self.socket:
            try:
                self.socket.close()
            except:
                pass 
    
    def receive_messages(self):
        while self.running:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if not message:
                    print("Rozłączono z serwerem")
                    self.disconnect()
                    break
                print(message)
            except ConnectionResetError:
                print("Połączenie z serwerem zostało zresetowane")
                self.disconnect()
                break
            except Exception as e:
                if self.running:
                    print(f"Błąd podczas odbierania wiadomości: {e}")
                    self.disconnect()
                break
    
    def send_message(self, message):
        try:
            self.socket.send(message.encode('utf-8'))
            return True
        except Exception as e:
            print(f"Błąd podczas wysyłania wiadomości: {e}")
            self.disconnect()
            return False
    
    def start(self):
        if not self.connect():  
            return
        
        # Uruchomienie osobnego wątku do odbierania wiadomości
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True  # Wątek zakończy się gdy główny wątek się zakończy
        receive_thread.start() 
        
        try:
            # Odebranie wiadomości powitalnej i odpowiedź nazwą użytkownika
            welcome = self.socket.recv(1024).decode('utf-8')
            print(welcome)  # Wyświetlenie wiadomości powitalnej
            
            username = input()
            self.send_message(username)  # Wysłanie nazwy użytkownika do serwera
            
            # Główna pętla wysyłania wiadomości
            while self.running:
                message = input()
                if message.lower() == '/exit':
                    break
                if not self.send_message(message):
                    break
        except KeyboardInterrupt:
            print("Wyjście z programu")
        finally:
            self.disconnect()

if __name__ == "__main__":
    client = ChatClient()
    client.start()