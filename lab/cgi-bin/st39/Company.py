from .Employee import Employee
from .Supervisor import Supervisor
from .templateLoader import load_template
import pickle
import os
import sqlite3


class Company:
    FILENAME = 'cgi-bin/st39/dump.pkl'
    DB_NAME = 'cgi-bin/st39/company.db'

    def __init__(self, q, selfurl):
        self._q = q
        self._selfurl = selfurl
        self._staff = []
        self._counter = 0
        self._connection = sqlite3.connect(Company.DB_NAME)
        self._connection.row_factory = sqlite3.Row
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            'CREATE TABLE IF NOT EXISTS company (id INTEGER, name TEXT, position TEXT, salary TEXT,'
            ' liberties TEXT, responsibility TEXT)')
        self._connection.commit()

    def __del__(self):
        self._connection.close()


    def add_employee(self):
        e = Employee(self._q, self._selfurl)
        e.add()

    def add_supervisor(self):
        s = Supervisor(self._q, self._selfurl)
        s.add()

    def edit_person(self):
        id = self._q['id'].value
        e = self._get_person(id)
        e.edit()

    def _save_person(self, person):
        id = self._q['id'].value
        if id == '-1':  # add
            self._counter = self._get_cur_id()
            person.save(self._counter + 1)
            person.db_insert(self._cursor)
        else:
            person._q = self._q
            person.save(self._q['id'].value)
            person.db_update(self._cursor)

        self._connection.commit()
        self.display_staff()

    def _save_from_file(self, person):
        self._counter = self._get_cur_id()
        person._id = self._counter + 1
        person.db_insert(self._cursor)
        self._connection.commit()

    def save_employee(self):
        id = self._q['id'].value
        if id == '-1':
            e = Employee(self._q, self._selfurl)
        else:
            e = self._get_person(id)
        self._save_person(e)

    def save_supervisor(self):
        id = self._q['id'].value
        if id == '-1':
            s = Supervisor(self._q, self._selfurl)
        else:
            s = self._get_person(id)
        self._save_person(s)

    def display_staff(self):
        print('<style>'
              'th, td {'
              'padding: 15px;'
              'text-align: left;'
              '}'
              'table {'
              'border-collapse: collapse;'
              '}'
              '</style>')
        print(load_template('table_header'))
        self._cursor.execute('SELECT * FROM company')
        self._connection.commit()
        data = self._cursor.fetchall()
        for row in data:
            person = Employee(self._q, self._selfurl) if row['liberties'] is None \
                else Supervisor(self._q, self._selfurl)
            person.db_construct(row)
            person.display()
        print(load_template('menu').format(
            self._selfurl,
            self._q['student'].value))

    def clear_staff(self, need_display=True):
        self._cursor.execute('DELETE FROM company')
        self._connection.commit()
        if need_display:
            self.display_staff()

    def remove_person(self):
        id = self._q['id'].value
        self._cursor.execute('DELETE FROM company WHERE id = ?', (id,))
        self._connection.commit()
        self.display_staff()

    def read_from_file(self):
        if os.path.exists(Company.FILENAME):
            self.clear_staff(False)
            with open(Company.FILENAME, 'rb') as dump:
                staff = pickle.load(dump)
            for person in staff:
                self._save_from_file(person)

            self.display_staff()

    def _get_person(self, id):  #
        self._cursor.execute('SELECT * FROM company WHERE id = ?', (id,))
        self._connection.commit()
        data = self._cursor.fetchone()
        person = Employee(self._q, self._selfurl) if data['liberties'] is None \
            else Supervisor(self._q, self._selfurl)
        person.db_construct(data)
        return person

    def _get_cur_id(self):
        self._cursor.execute('SELECT * FROM company WHERE id = (SELECT MAX(ID) FROM company)')
        self._connection.commit()
        data = self._cursor.fetchone()
        return data['id'] if data is not None else -1