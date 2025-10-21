import psycopg2
import psycopg2.extras
from core.dominio.entidades.inventario_cedulas import InventarioCedulas

class PostgresInventoryRepository:
    def __init__(self, database_url):
        self.database_url = database_url
        self._ensure_tables()

    def _connect(self):
        return psycopg2.connect(self.database_url)

    def _ensure_tables(self):
        sql = """
        CREATE TABLE IF NOT EXISTS inventory (
            denomination INTEGER PRIMARY KEY,
            quantity INTEGER NOT NULL
        );
        -- seed common denominations if table empty
        INSERT INTO inventory(denomination, quantity)
        SELECT 100, 10
        WHERE NOT EXISTS (SELECT 1 FROM inventory);
        """
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
        finally:
            conn.close()

    def getInventory(self):
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute('SELECT denomination, quantity FROM inventory')
            rows = cur.fetchall()
            mapa = {}
            for row in rows:
                mapa[row[0]] = row[1]
            return InventarioCedulas(mapa)
        finally:
            conn.close()

    def updateInventory(self, inventario):
        conn = self._connect()
        try:
            cur = conn.cursor()
            for denom, qtd in inventario.getMapaDisponivel().items():
                cur.execute('INSERT INTO inventory(denomination, quantity) VALUES(%s,%s) ON CONFLICT (denomination) DO UPDATE SET quantity = EXCLUDED.quantity', (denom, qtd))
            conn.commit()
        finally:
            conn.close()
