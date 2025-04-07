import socket  
import threading
import time
from message_queue import MessageQueue 

class ChatServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host  
        self.port = port  
        self.server_socket = None  # Socket serwera, inicjalizowany w metodzie start()
        self.clients = []  
        self.clients_lock = threading.Lock()  # Blokada dla bezpiecznego dostępu do listy klientów z różnych wątków
        self.message_queue = MessageQueue()  # Instancja własnej klasy do zarządzania kolejką wiadomości
        self.running = False 

    def start(self):
        # Tworzenie socketu serwera
        # AF_INET oznacza IPv4, SOCK_STREAM oznacza TCP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        # SOL_SOCKET oznacza, że chcemy ustawić opcje dla socketu, SO_REUSEADDR pozwala na ponowne użycie adresu
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bindowanie socketu do określonego adresu i portu
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10) # maks 10 oczekujących połączeń
        self.running = True
        
        print(f"Serwer czatu uruchomiony na {self.host}:{self.port}")
        
        # Uruchomienie osobnego wątku, który będzie rozsyłał wiadomości do klientów
        broadcast_thread = threading.Thread(target=self.broadcast_messages)
        broadcast_thread.daemon = True  # Daemon=True sprawia, że wątek zakończy się, gdy główny wątek się zakończy
        broadcast_thread.start() 
        
        try:
            # Główna pętla serwera - akceptowanie nowych połączeń
            while self.running:
                # Czekanie na nowe połączenie - blokująca operacja
                client_socket, address = self.server_socket.accept()
                print(f"Nowe połączenie od {address}")
                
                # Tworzenie i uruchamianie nowego wątku dla obsługi klienta
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
                client_thread.daemon = True  # Wątek zostanie zakończony gdy główny wątek się zakończy
                client_thread.start()  # Uruchomienie wątku
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            print(f"Błąd serwera: {e}")
            self.stop()

    def stop(self):
        """
        Zatrzymuje serwer i zamyka wszystkie połączenia.
        """
        self.running = False  # Oznaczenie, że serwer przestał działać
        
        # Zamknięcie wszystkich socketów klientów
        with self.clients_lock:  # Użycie blokady aby uniknąć wyścigu (race condition)
            for client in self.clients:
                try:
                    client.close()  # Zamknięcie socketu klienta
                except:
                    pass  # Ignorujemy błędy przy zamykaniu
            self.clients.clear()  # Czyszczenie listy klientów
        
        # Zamknięcie socketu serwera
        if self.server_socket:
            self.server_socket.close()
        
        print("Serwer czatu zatrzymany")

    def handle_client(self, client_socket, address):
        # Dodanie klienta do listy aktywnych klientów
        with self.clients_lock:
            self.clients.append(client_socket)
        
        client_socket.send("Witaj w czacie! Wpisz swoje imię:".encode('utf-8'))
        
        try:
            username = client_socket.recv(1024).decode('utf-8').strip()
            welcome_msg = f"*** {username} dołączył do czatu ***"
            print(welcome_msg)
            
            self.message_queue.add_message((None, welcome_msg))
            
            # Główna pętla obsługi wiadomości od klienta
            while self.running:
                try:
                    # Odbiór wiadomości od klienta - blokująca operacja
                    message = client_socket.recv(1024).decode('utf-8').strip()
                    if not message:  # Pusta wiadomość oznacza rozłączenie klienta
                        break
                    
                    print(f"Wiadomość od {username}: {message}")
                    
                    # Dodanie wiadomości do kolejki z informacją o nadawcy
                    formatted_message = f"{username}: {message}"
                    self.message_queue.add_message((client_socket, formatted_message))
                    
                except ConnectionResetError:
                    break
                except Exception as e:
                    print(f"Błąd podczas odbierania wiadomości od {username}: {e}")
                    break
                    
        except Exception as e:
            print(f"Błąd obsługi klienta {address}: {e}")
        finally:
            # Usunięcie klienta z listy aktywnych klientów
            with self.clients_lock: 
                if client_socket in self.clients:
                    self.clients.remove(client_socket)
            
            # Zamknięcie połączenia z klientem
            try:
                client_socket.close() 
                leave_msg = f"*** {username} opuścił czat ***"
                print(leave_msg)
                # Dodanie informacji o opuszczeniu czatu do kolejki (None jako nadawca - komunikat systemowy)
                self.message_queue.add_message((None, leave_msg))
            except:
                pass 

    def broadcast_messages(self):
        while self.running:
            if not self.message_queue.is_empty():
                # Pobranie wiadomości z kolejki (sender_socket to socket nadawcy lub None dla komunikatów systemowych)
                sender_socket, message = self.message_queue.get_message()
                
                # Wysłanie wiadomości do wszystkich klientów, z wyjątkiem nadawcy
                with self.clients_lock:
                    for client in self.clients:
                        if client != sender_socket:
                            try:
                                client.send(message.encode('utf-8'))
                            except:
                                pass
            else:
                # Jeśli kolejka jest pusta, czekamy chwilę przed kolejnym sprawdzeniem
                time.sleep(0.1)

if __name__ == "__main__":
    server = ChatServer()
    server.start()