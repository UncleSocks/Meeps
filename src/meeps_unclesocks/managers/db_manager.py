from typing import Optional, Union




class DatabaseQueries:

    def __init__(self, cursor):
        self.cursor = cursor
    
    def _fetch_all(self, query: str, 
                   param: Optional[Union[list | tuple]] = None, col: int = None):
        if param is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, param)

        if col is None:
            return self.cursor.fetchall()
        else:
            results = self.cursor.fetchall()
            return [result[col] for result in results]
    
    def _fetch_one(self, query: str, 
                   param: Optional[Union[list | tuple]] = None, col: int = None):
        if param is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, param)

        if col is None:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchone()[col]


    """--------------------SHARED QUERIES--------------------"""

    def fetch_ticket_titles(self):
        query = 'SELECT title FROM tickets'
        return self._fetch_all(query, col=0)
    
    def fetch_account_names(self):
        query = 'SELECT name FROM accounts'
        return self._fetch_all(query, col=0)
    
    def fetch_account_names_ids(self):
        query = 'SELECT id, name FROM accounts'
        return self._fetch_all(query)
    
    def fetch_threat_names(self):
        query = 'SELECT name FROM threats'
        return self._fetch_all(query, col=0)
    
    def fetch_threat_names_ids(self):
        query = 'SELECT id, name FROM threats'
        return self._fetch_all(query)
    
    def fetch_threat_details(self, threat_id):
        query = 'SELECT name, description, indicators, countermeasures, image FROM threats WHERE id=?'
        return self._fetch_one(query, param=[threat_id])
    
    def fetch_max_id(self, table: str) -> int:
        query = f'SELECT MAX(id) FROM {table}'
        return self._fetch_one(query, col=0)  
    

    """--------------------SHIFT QUERIES--------------------"""

    def fetch_ticket_ids(self):
        query = 'SELECT id FROM tickets'
        return self._fetch_all(query, col=0)
    
    def fetch_ticket_details(self, ticket_id):
        query = 'SELECT t.title, t.entry, t.threat_id, t.transcript_path, a.name, a.organization, a.email, a.contact, a.picture FROM tickets t JOIN accounts a ON t.caller_id = a.id WHERE t.id=?'
        return self._fetch_one(query, param=[ticket_id])
    

    """--------------------TICKET QUERIES--------------------"""
    
    def fetch_ticket_titles_ids(self):
        query = 'SELECT id, title FROM tickets'
        return self._fetch_all(query)
    
    def fetch_ticket_account_details(self, ticket_id):
        query = 'SELECT t.title, t.entry, a.name, a.organization, a.email, a.contact FROM tickets t JOIN accounts a ON t.caller_id = a.id WHERE t.id=?'
        return self._fetch_one(query, param=[ticket_id])
    

    """--------------------ACCOUNT QUERIES--------------------"""
    
    def fetch_account_details(self, account_id):
        query = 'SELECT name, organization, email, contact, picture FROM accounts WHERE id=?'
        return self._fetch_one(query, param=[account_id])
    
    def fetch_assigned_tickets(self, account_id):
        query = 'SELECT title FROM tickets WHERE caller_id=?'
        return self._fetch_all(query, param=[account_id], col=0)
    

class DatabaseRemovals:

    def __init__(self, cursor, connect):
        self.cursor = cursor
        self.connect = connect

    def _delete_entry(self, table: str, key: str, param: Union[list, tuple]):
        query = f'DELETE FROM {table} WHERE {key}=?'
        self.cursor.execute(query, param)
        self.connect.commit()

    def delete_ticket(self, ticket_id) -> None:
        self._delete_entry(table='tickets', key='id', param=[ticket_id])
        return

    def delete_account(self, account_id) -> None:
        self._delete_entry(table='accounts', key='id', param=[account_id])
        self._delete_entry(table='tickets', key='caller_id', param=[account_id])
        return
    
    def delete_threat(self, threat_id) -> None:
        self._delete_entry(table='tickets', key='threat_id', param=[threat_id])
        self._delete_entry(table='threats', key='id', param=[threat_id])
        return
    

class DatabaseInsertions:

    def __init__(self, cursor, connect):
        self.cursor = cursor
        self.connect = connect

    def insert_entry(self, table: str, value: tuple):
        placeholders = "?, "*(len(value)-1) + "?"
        query = f'INSERT INTO {table} VALUES ({placeholders})' 
        self.cursor.execute(query, value)
        self.connect.commit()