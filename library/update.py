import sqlite3
bd=sqlite3.connect("database.db")
cursor=bd.cursor()

def insert_client_project(client_name, client_number):
    cursor.execute("INSERT INTO clientProject (projectClientName, projectClientNumber) VALUES (?, ?)",
                   (client_name, client_number))
    bd.commit()

def update_client_name(cursor, client_id, new_name):
    cursor.execute("UPDATE clientProject SET projectClientName = ? WHERE projectClientId = ?",
                   (new_name, client_id))
    bd.commit()

def update_client_number(cursor, client_id, new_number):
    cursor.execute("UPDATE clientProject SET projectClientNumber = ? WHERE projectClientId = ?",
                   (new_number, client_id))
    bd.commit()

def insert_currency_type(cursor, currency_name):
    cursor.execute("INSERT INTO typeCurrency (currencyTypeName) VALUES (?)", (currency_name,))
    bd.commit()

def update_currency_name(cursor, currency_id, new_name):
    cursor.execute("UPDATE typeCurrency SET currencyTypeName = ? WHERE currencyTypeId = ?",
                   (new_name, currency_id))
    bd.commit()

def insert_project_charge(cursor, currency_id, installment, balance, total_payment):
    cursor.execute("INSERT INTO chargeProject (projectChargeCurrency, projectChargeInstallment, "
                   "projectChargeBalance, projectChargeTotalPayment) VALUES (?, ?, ?, ?)",
                   (currency_id, installment, balance, total_payment))
    bd.commit()

def update_project_charge(charge_id, new_installment, new_balance, new_total_payment):
    cursor.execute("UPDATE chargeProject SET projectChargeInstallment = ?, "
                   "projectChargeBalance = ?, projectChargeTotalPayment = ? WHERE projectChargeId = ?",
                   (new_installment, new_balance, new_total_payment, charge_id))
    bd.commit()

def insert_project_date(cursor, start_date, finished_date):
    cursor.execute("INSERT INTO dateProject (projectDateStart, projectDateFinished) VALUES (?, ?)",
                   (start_date, finished_date))
    bd.commit()

def update_project_date(cursor, date_id, new_start_date, new_finished_date):
    cursor.execute("UPDATE dateProject SET projectDateStart = ?, projectDateFinished = ? WHERE projectDateId = ?",
                   (new_start_date, new_finished_date, date_id))
    bd.commit()

def insert_project_type(cursor, project_type_name):
    cursor.execute("INSERT INTO typeProject (projectTypeName) VALUES (?)", (project_type_name,))
    bd.commit()

def update_project_type_name(cursor, type_id, new_type_name):
    cursor.execute("UPDATE typeProject SET projectTypeName = ? WHERE projectTypeId = ?",
                   (new_type_name, type_id))
    bd.commit()

def insert_user(cursor, user_name, user_password):
    cursor.execute("INSERT INTO users (userName, userPassword) VALUES (?, ?)", (user_name, user_password))
    bd.commit()

def update_user_password(cursor, user_id, new_password):
    cursor.execute("UPDATE users SET userPassword = ? WHERE userId = ?", (new_password, user_id))
    bd.commit()

def insert_project(cursor, project_name, project_date_id, project_charge_id, project_client_id):
    cursor.execute("INSERT INTO projects (projectName, projectDate, projectCharge, projectClient) "
                   "VALUES (?, ?, ?, ?)", (project_name, project_date_id, project_charge_id, project_client_id))
    bd.commit()

def update_project_name(cursor, project_id, new_name):
    cursor.execute("UPDATE projects SET projectName = ? WHERE projectId = ?", (new_name, project_id))
    bd.commit()

def insert_different_type_project(cursor, key_project_id, key_project_type_id):
    cursor.execute("INSERT INTO differentTypeProject (keyProjectId, keyProjectTypeId) VALUES (?, ?)",
                   (key_project_id, key_project_type_id))
    bd.commit()

def update_different_type_project(cursor, different_type_id, new_key_project_id, new_key_project_type_id):
    cursor.execute("UPDATE differentTypeProject SET keyProjectId = ?, keyProjectTypeId = ? WHERE differentTypeProjectId = ?",
                   (new_key_project_id, new_key_project_type_id))