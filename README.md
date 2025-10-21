# Instruções de Uso - Caixa Eletrônico (Docker Compose)

**Observação:** O sistema e o PostgreSQL rodam juntos com `docker-compose up --build`. 
Não é necessário criar/usar `venv` local quando executar via Docker.

## Variáveis de configuração
- `DATABASE_URL`: URL de conexão com PostgreSQL (padrão no compose: `postgresql://atm_user:atm_pass@db:5432/atm_db`)
- Caso queira alterar, edite `docker-compose.yml` ou exporte a variável antes de rodar.

---
## Primeira execução (máquina com Docker + Docker Compose)
1. Build e subir containers (cria imagens e inicia app + banco):
   ```bash
   docker-compose up --build
   ```
   - O serviço `app` fará a primeira tentativa de conexão com o banco e criará as tabelas básicas se necessário.
   - Aguarde as mensagens de log do container `app` informando que o menu do caixa está disponível.
2. Para abrir um terminal interativo no container do app (opcional):
   ```bash
   docker-compose exec app bash
   ```

### Observação sobre dependências
- O `requirements.txt` está presente para documentar dependências (ex.: `psycopg2-binary`). O container instala automaticamente ao buildar a imagem.

---
## Demais execuções (após o primeiro build)
1. Se os containers já foram construídos no primeiro uso, apenas execute:
   ```bash
   docker-compose up
   ```
2. Se quiser rodar em background (detached):
   ```bash
   docker-compose up -d
   ```
3. Para ver logs dos serviços em execução:
   ```bash
   docker-compose logs -f
   ```
4. Para entrar no container do app (caso precise):
   ```bash
   docker-compose exec app bash
   ```

---
## Como sair / parar e limpar
1. Para parar os containers sem removê-los:
   ```bash
   docker-compose stop
   ```
2. Para parar e remover containers, redes e volumes definidos no compose:
   ```bash
   docker-compose down
   ```
3. Se rodou em detached (-d) e quer apenas parar sem remover volumes:
   ```bash
   docker-compose stop
   ```

---
## Local onde configurar o banco (se necessário)
- A configuração padrão do banco fica no `docker-compose.yml` (serviço `db`):
  - `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`.
- A aplicação lê `DATABASE_URL` (variável de ambiente) para conectar ao banco.
- Para alterar o usuário/senha/banco, edite `docker-compose.yml` e reconstrua com `docker-compose up --build`.

---
## Notas rápidas
- Python: imagem `python:3.11` (completa) é usada no Dockerfile.
- O app cria tabelas e um dado inicial (conta demo) ao iniciar, caso não exista.
- Logs de eventos do caixa são gravados em `/app/logs/atm_events.log` dentro do container (mapeado no projeto).
