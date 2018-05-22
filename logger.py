import sqlite3
import datetime
import httpfetcher


class Logger():
    def __init__(self, log_type):
        self.log_type = log_type
        self.conn = self.connect()
        self.url = ''
        self.scheme = ''
        self.domain_name = ''
        self.web_path = ''
        self.query = ''

    def connect(self):
        return sqlite3.connect(self.log_type + '.db')

    def _set_url(self, url):
        hf = httpfetcher.HTTPFetcher(url)
        url_parse = hf.parse_url()
        self.url = url
        self.scheme = url_parse["scheme"]
        self.domain_name = url_parse["domain_name"]
        self.web_path = url_parse["web_path"]
        self.query = url_parse["domain_name"]
        return

    def log_seen(self, url):
        self._set_url(url)
        logger_cursor = self.conn.cursor()
        execute_string_select = '''
        SELECT * FROM URL_SEEN 
        WHERE URL = "%s"
        '''
        logger_cursor.execute(execute_string_select % (self.url))
        rows = logger_cursor.fetchall()
        if rows != []:
            execute_string_update = '''
            UPDATE URL_SEEN SET STATUS_CODE = "%s", FINISHED = "%s", 
            FETCH_TIME = FETCH_TIME + 1,
            LATEST_TIMESTAMP = "%s"
            WHERE URL = "%s";
            '''
            logger_cursor.execute(execute_string_update % (
                0, 'FINISHED', str(datetime.datetime.now()), self.url))
            self.conn.commit()
            return {'FETCH_TIME': rows[0][7], 'LATEST_TIMESTAMP': rows[0][6]}
        else:
            execute_string_insert = '''
            INSERT INTO URL_SEEN (URL, WEB_SCHEME, DOMAIN_NAME, WEB_PATH,
            QUERY, STATUS_CODE, FINISHED, FETCH_TIME, LATEST_TIMESTAMP)
            VALUES ("%s", "%s", "%s", "%s", "%s", %s, "%s", 0, "%s")
            '''

            logger_cursor.execute(execute_string_insert % (self.url, self.scheme, self.domain_name,
                                                           self.web_path, self.query, 0, 'FINISHED',
                                                           str(datetime.datetime.now())))
            self.conn.commit()
            return {'FETCH_TIME': 0, 'LATEST_TIMESTAMP': 'NEW_RECORD'}

        self.conn.close()

    def fetch_all_seen(self):
        logger_cursor = self.conn.cursor()
        execute_string_select = '''SELECT * FROM URL_SEEN'''
        logger_cursor.execute(execute_string_select)
        rows = logger_cursor.fetchall()
        return rows
