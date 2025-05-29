from __init__ import CURSOR, CONN


class Department:
    # Cache of Department instances keyed by primary key
    all = {}

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        """Create the departments table if it doesn't exist"""
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the departments table if it exists"""
        sql = """
            DROP TABLE IF EXISTS departments;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Insert a new row and cache this object"""
        sql = """
            INSERT INTO departments (name, location)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, location):
        """Instantiate and save a new Department object"""
        department = cls(name, location)
        department.save()
        return department

    def update(self):
        """Update the corresponding row in the database"""
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        """Delete the corresponding row, remove from cache, and reset id"""
        sql = """
            DELETE FROM departments
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        # Remove from cache and reset
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        """Return a Department instance from a database row"""
        if row is None:
            return None
        dept_id, name, location = row
        # Check cache
        department = cls.all.get(dept_id)
        if department:
            # Update fields in case they changed
            department.name = name
            department.location = location
        else:
            department = cls(name, location, id=dept_id)
            cls.all[dept_id] = department
        return department

    @classmethod
    def get_all(cls):
        """Return all Department instances from the database"""
        sql = """
            SELECT *
            FROM departments
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return a Department instance matching the given primary key"""
        sql = """
            SELECT *
            FROM departments
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Return the first Department instance matching the given name"""
        sql = """
            SELECT *
            FROM departments
            WHERE name = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
