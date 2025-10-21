import os
import time
from infrastructure.di_container import DIContainer

def main():
    # loop de espera para o db subir (simples retry)
    db_url = os.environ.get('DATABASE_URL')
    print('DATABASE_URL=', db_url)
    print('Iniciando container app... aguardando banco ficar disponível (tentando conectar)...')
    # DIContainer fará as tentativas de conexão quando instanciado
    container = None
    for i in range(30):
        try:
            container = DIContainer()
            break
        except Exception as e:
            print('Tentativa de conexão falhou:', e)
            time.sleep(2)
    if container is None:
        print('Não foi possível conectar ao banco. Encerrando.')
        return

    controller = container.get_caixa_controller()
    controller.iniciar()

if __name__ == '__main__':
    main()
