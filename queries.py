

class SqliteQueries():

    def __init__(self, cursor):

        self.cursor = cursor
        

    def ticket_ids_query(self):

        self.cursor.execute('SELECT id FROM tickets')
        ticket_ids_results = self.cursor.fetchall()
        ticket_ids_list = [ticket_ids_result[0] for ticket_ids_result in ticket_ids_results]

        return ticket_ids_list
    
    def max_ticket_id_query(self):
        self.cursor.execute('SELECT MAX(id) FROM tickets')
        last_ticket_id = self.cursor.fetchone()[0]
        return last_ticket_id
    

    def ticket_titles_query(self):
        self.cursor.execute('SELECT title FROM tickets')
        ticket_title_result = self.cursor.fetchall()
        ticket_title_list = [ticket[0] for ticket in ticket_title_result]
        return ticket_title_list
    
    def ticket_id_title_list(self):
        self.cursor.execute('SELECT id, title FROM tickets')
        ticket_id_title_list = self.cursor.fetchall()
        return ticket_id_title_list


    def ticket_query(self, selected_id):

        self.cursor.execute('SELECT t.title, t.entry, t.threat_id, a.name, a.organization, a.email, a.contact, a.picture FROM tickets t JOIN accounts a ON t.caller_id = a.id WHERE t.id=?',
                    [selected_id])
        
        title, current_ticket, threat_id, caller_name, caller_org, caller_email, caller_contact, caller_picture_file = self.cursor.fetchone()

        return title, current_ticket, threat_id, caller_name, caller_org, caller_email, caller_contact, caller_picture_file
    

    def ticket_account_query(self, selected_ticket_id):

        self.cursor.execute('SELECT t.title, t.entry, a.name, a.organization, a.email, a.contact FROM tickets t JOIN accounts a ON t.caller_id = a.id WHERE t.id=?', [selected_ticket_id])
        ticket_title, ticket_entry, account_name, account_organization, account_email, account_contact = self.cursor.fetchone()
        
        return ticket_title, ticket_entry, account_name, account_organization, account_email, account_contact
    

    def ticket_transcript_query(self, selected_id):

        self.cursor.execute('SELECT transcript_path FROM tickets WHERE id=?', [selected_id])
        ticket_transcript_path = self.cursor.fetchone()[0]

        return ticket_transcript_path
    
    def ticket_threat_selection_query(self, selected_threat_id):

        self.cursor.execute('SELECT name, description, indicators, countermeasures, image FROM threats WHERE name=?', [selected_threat_id])
        name, description, indicators, countermeasures, image_file = self.cursor.fetchone()

        return name, description, indicators, countermeasures, image_file
    
    def max_threat_id_query(self):
        self.cursor.execute('SELECT MAX(id) FROM threats')
        last_threat_id = self.cursor.fetchone()[0]
        return last_threat_id

    def threat_ids_query(self):
        self.cursor.execute('SELECT id FROM threats')
        threat_ids_results = self.cursor.fetchall()
        threat_id_list = [threat_ids_result[0] for threat_ids_result in threat_ids_results]
        return threat_id_list
    
    def threat_id_name_query(self):
        self.cursor.execute('SELECT id, name FROM threats')
        threat_id_name_list = self.cursor.fetchall()
        return threat_id_name_list


    def threat_list_query(self):

        self.cursor.execute('SELECT name FROM threats')
        threat_list_results = self.cursor.fetchall()
        threat_list = [threat_list_result[0] for threat_list_result in threat_list_results]

        return threat_list
    
    def threat_selection_query(self, selected_threat):

        self.cursor.execute('SELECT description, indicators, countermeasures, image FROM threats WHERE name=?', [selected_threat])
        description, indicators, countermeasures, image_file = self.cursor.fetchone()

        return description, indicators, countermeasures, image_file
    

    def threat_ticket_selection_query(self, selected_threat_id):

        self.cursor.execute('SELECT name, description, indicators, countermeasures FROM threats WHERE id=?', [selected_threat_id])
        name, description, indicators, countermeasures = self.cursor.fetchone()

        return name, description, indicators, countermeasures
    
    def ticket_caller_id_query(self, selected_caller):

        self.cursor.execute('SELECT id FROM accounts WHERE name=?', [selected_caller])
        selected_caller_id = int(self.cursor.fetchone()[0])

        return selected_caller_id
    
    def ticket_title_caller_id_query(self, selected_account_id):

        self.cursor.execute('SELECT title FROM tickets WHERE caller_id=?', [selected_account_id])
        assigned_tickets_result = self.cursor.fetchall()

        assigned_ticket_list = [assigned_ticket_title[0] for assigned_ticket_title in assigned_tickets_result]
        
        return assigned_ticket_list
    
    
    def account_name_list_query(self):

        self.cursor.execute('SELECT name FROM accounts')
        account_name_list_results = self.cursor.fetchall()

        account_name_list = [account_name_list_result[0] for account_name_list_result in account_name_list_results]

        return account_name_list
    

    def account_id_query(self):

        self.cursor.execute('SELECT id FROM accounts')
        account_id_list_results = self.cursor.fetchall()

        account_id_list = [account_id_list_result[0] for account_id_list_result in account_id_list_results]

        return account_id_list
    
    def account_id_name_list(self):
        self.cursor.execute('SELECT id, name FROM accounts')
        account_id_name_list = self.cursor.fetchall()
        return account_id_name_list
    
    def max_account_id_query(self):
        self.cursor.execute('SELECT MAX(id) FROM accounts')
        last_account_id = self.cursor.fetchone()[0]
        return last_account_id
    
    def account_details_query(self, selected_account_id):

        self.cursor.execute('SELECT name, organization, email, contact, picture FROM accounts WHERE id=?', [selected_account_id])
        account_name, account_organization, account_email, account_contact, account_picture_path = self.cursor.fetchone()

        return account_name, account_organization, account_email, account_contact, account_picture_path