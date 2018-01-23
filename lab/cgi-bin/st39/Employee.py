from .templateLoader import load_template


class Employee:
    def __init__(self, q, selfurl):
        self._q = q
        self._selfurl = selfurl
        self._id = None
        self._name = None
        self._position = None
        self._salary = None

    def db_construct(self, data):
        self._id = data['id']
        self._name = data['name']
        self._position = data['position']
        self._salary = data['salary']

    def edit(self):
        print(load_template('employee_form').format(
            self._selfurl,
            self._q['student'].value,
            self._id,
            self._name,
            self._position,
            self._salary
        ))

    def display(self):
        print(load_template('display_employee').format(
            self._q['student'].value,
            self._id,
            self._name,
            self._position,
            self._salary))

    def add(self):
        print(load_template('employee_form').format(
            self._selfurl,
            self._q['student'].value,
            -1,
            '', '', ''
        ))

    def save(self, id):
        self._id = id
        self._name = self._q.getvalue('name', '')
        self._position = self._q.getvalue('position', '')
        self._salary = self._q.getvalue('salary', '')

    def db_insert(self, cursor):
        cursor.execute('INSERT INTO company (id, name, position, salary) VALUES (?, ?, ?, ?)',
                       (self._id, self._name, self._position, self._salary))

    def db_update(self, cursor):
        cursor.execute('UPDATE company SET name = ?, position = ?, salary = ? WHERE id = ?',
                       (self._name, self._position, self._salary, self._id))

