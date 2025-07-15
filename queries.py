

def ticket_ids(cursor):
    
    cursor.execute('SELECT id FROM tickets')
    ticket_ids_results = cursor.fetchall()
    ticket_ids_list = [ticket_ids_result[0] for ticket_ids_result in ticket_ids_results]

    return ticket_ids_list


def threats(cursor):

    cursor.execute('SELECT name FROM threats')
    threat_list_results = cursor.fetchall()
    threat_list = [threat_list_result[0] for threat_list_result in threat_list_results]

    return threat_list


def accounts(cursor):

    cursor.execute('SELECT id, name FROM accounts')
    account_list_results = cursor.fetchall()
    id_list = [account_list_result[0] for account_list_result in account_list_results]
    account_list = [account_list_result[1] for account_list_result in account_list_results]

    return id_list, account_list


def tickets(cursor):

    cursor.execute('SELECT id, title FROM tickets')
    ticket_list_results = cursor.fetchall()
    id_list = [ticket_list_result[0] for ticket_list_result in ticket_list_results]
    ticket_list = [ticket_list_result[1] for ticket_list_result in ticket_list_results]

    return id_list, ticket_list



class SqliteQueries():

    def __init__(self, cursor):

        self.cursor = cursor
        

    def ticket_ids_query(self):

        self.cursor.execute('SELECT id FROM tickets')
        ticket_ids_results = self.cursor.fetchall()
        ticket_ids_list = [ticket_ids_result[0] for ticket_ids_result in ticket_ids_results]

        return ticket_ids_list


    def ticket_query(self, selected_id):

        self.cursor.execute('SELECT t.title, t.entry, t.answer, a.name, a.organization, a.email, a.contact, a.picture FROM tickets t JOIN accounts a ON t.caller_id = a.id WHERE t.id=?',
                    [selected_id])
        
        title, current_ticket, answer, caller_name, caller_org, caller_email, caller_contact, caller_picture_file = self.cursor.fetchone()

        return title, current_ticket, answer, caller_name, caller_org, caller_email, caller_contact, caller_picture_file
    

    def ticket_transcript_query(self, selected_id):

        self.cursor.execute('SELECT transcript_path FROM tickets WHERE id=?', [selected_id])
        ticket_transcript_path = self.cursor.fetchone()[0]

        return ticket_transcript_path


    def threat_list_query(self):

        self.cursor.execute('SELECT name FROM threats')
        threat_list_results = self.cursor.fetchall()
        threat_list = [threat_list_result[0] for threat_list_result in threat_list_results]

        return threat_list
    
    def threat_selection_query(self, selected_threat):

        self.cursor.execute('SELECT description, indicators, countermeasures, image FROM threats WHERE name=?', [selected_threat])
        description, indicators, countermeasures, image_file = self.cursor.fetchone()

        return description, indicators, countermeasures, image_file