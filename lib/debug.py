#!/usr/bin/env python3

from __init__ import CONN, CURSOR
from department import Department

import ipdb

def reset_database():
    # Drop and recreate the departments table
    Department.drop_table()
    Department.create_table()

    # Seed initial data
    Department.create("Payroll", "Building A, 5th Floor")
    Department.create("Human Resources", "Building C, East Wing")
    Department.create("Accounting", "Building B, 1st Floor")


if __name__ == "__main__":
    reset_database()
    # Enter interactive debugging session
    ipdb.set_trace()
