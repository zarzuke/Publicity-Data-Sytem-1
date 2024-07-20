import sqlite3


db=sqlite3.connect("database.db")
bd=sqlite3.connect("DB.db")
cursor=bd.cursor()

def insert_client_project(client_name, client_number):
    cursor.execute("INSERT INTO clientProject (projectClientName, projectClientNumber) VALUES (?, ?)",
                   (client_name, client_number))
    bd.commit()

def insert_currency_type(currency_name):
    cursor.execute("INSERT INTO typeCurrency (currencyTypeName) VALUES (?)", (currency_name,))
    bd.commit()

def insert_project_charge(currency_id, installment, balance, total_payment):
    cursor.execute("INSERT INTO chargeProject (projectChargeCurrency, projectChargeInstallment, "
                   "projectChargeBalance, projectChargeTotalPayment) VALUES (?, ?, ?, ?)",
                   (currency_id, installment, balance, total_payment))
    bd.commit()

def insert_project_date(start_date, finished_date):
    cursor.execute("INSERT INTO dateProject (projectDateStart, projectDateFinished) VALUES (?, ?)",
                   (start_date, finished_date))
    bd.commit()

def insert_project_type(project_type_name):
    cursor.execute("INSERT INTO typeProject (projectTypeName) VALUES (?)", (project_type_name,))
    bd.commit()

def insert_project(project_name, project_date_id, project_charge_id, project_client_id):
    cursor.execute("INSERT INTO projects (projectName, projectDate, projectCharge, projectClient) "
                   "VALUES (?, ?, ?, ?)", (project_name, project_date_id, project_charge_id, project_client_id))
    bd.commit()

def insert_different_type_project(key_project_id, key_project_type_id):
    cursor.execute("INSERT INTO differentTypeProject (keyProjectId, keyProjectTypeId) VALUES (?, ?)",
                   (key_project_id, key_project_type_id))
    bd.commit()
