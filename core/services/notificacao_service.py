class NotificacaoService:
    def __init__(self):
        self.notificadores = []

    def registrarNotifier(self, notifier):
        self.notificadores.append(notifier)

    def notify(self, mensagem: str):
        for n in self.notificadores:
            try:
                n.notify(mensagem)
            except Exception as e:
                print('Falha ao notificar:', e)
