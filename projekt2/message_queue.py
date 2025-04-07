import threading
from collections import deque

class MessageQueue:
    def __init__(self):
        self.queue = deque()  # Kolejka przechowująca wiadomości
        self.lock = threading.Lock()  # Blokada dla bezpiecznego dostępu do kolejki
    
    def add_message(self, message):
        with self.lock:
            self.queue.append(message)
    
    def get_message(self):
        with self.lock:
            if self.queue:
                return self.queue.popleft()
            return None
    
    def is_empty(self):
        with self.lock:
            return len(self.queue) == 0
            
    def clear(self):
        with self.lock:
            self.queue.clear()