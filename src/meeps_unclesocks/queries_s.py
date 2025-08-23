class DatabaseQueries:

    def __init__(self, cursor):
        self.cursor = cursor

    def _fetch_specific_all(self, query, param=None):
        if param is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query,param)
        results = self.cursor.fetchall()
        return [result[0] for result in results]
    
    def _fetch_all(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def _fetch_one(self, query, param=None):
        if param is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, param)
        return self.cursor.fetchone()
    

    """--------------------ACCOUNT MANAGEMENT QUERIES--------------------"""

    def fetch_account_names_ids(self):
        query = 'SELECT id, name FROM accounts'
        return self._fetch_all(query)
    
    def fetch_account_names(self):
        query = 'SELECT name FROM accounts'
        return self._fetch_specific_all(query)
    
    def fetch_account_details(self, account_id):
        query = 'SELECT name, organization, email, contact, picture FROM accounts WHERE id=?'
        param = account_id
        return self._fetch_one(query, [param])
    
    def fetch_ticket_titles(self, account_id):
        query = 'SELECT title FROM tickets WHERE caller_id=?'
        param = account_id
        return self._fetch_specific_all(query, [param])