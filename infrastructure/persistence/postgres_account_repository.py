import psycopg2
import psycopg2.extras
from decimal import Decimal
from core.dominio.entidades.conta import Conta

class PostgresAccountRepository:
    def __init__(self, database_url):
        self.database_url = database_url
        self._ensure_tables()

    def _connect(self):
        return psycopg2.connect(self.database_url)

    def _ensure_tables(self):
        sql = """
        CREATE TABLE IF NOT EXISTS accounts (
            id TEXT PRIMARY KEY,
            balance NUMERIC NOT NULL
        );
        INSERT INTO accounts(id, balance)
        SELECT 'demo'::text, 1000.00::numeric
        WHERE NOT EXISTS (SELECT 1 FROM accounts WHERE id='demo');
        """
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
        finally:
            conn.close()

    def getById(self, contaId: str):
        conn = self._connect()
        try:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute('SELECT id, balance FROM accounts WHERE id=%s', (contaId,))
            row = cur.fetchone()
            if not row:
                return None
            return Conta(row['id'], Decimal(row['balance']))
        finally:
            conn.close()

    def update(self, conta: Conta):
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute('UPDATE accounts SET balance=%s WHERE id=%s', (str(conta.saldo), conta.id))
            conn.commit()
        finally:
            conn.close()
