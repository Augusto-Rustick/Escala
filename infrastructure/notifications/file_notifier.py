import os
from datetime import datetime
from .notifier import Notifier

class FileNotifier(Notifier):
    def __init__(self, path='logs/atm_events.log'):
        self.path = path
        # garante diretório
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def notify(self, mensagem: str):
        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.utcnow().isoformat()}] {mensagem}\n")
