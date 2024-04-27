from flask import Flask, render_template, request, redirect, url_for
from database_connection import TechnologyTransferDatabase

app = Flask(__name__)
db = TechnologyTransferDatabase()
db.connect()
cursor = db.create_cursor()
tables_id = {
    'collaboration': 'collaborationID',
    'customer': 'customerID',
    'director': 'directorID',
    'intellectual_property_office': 'ipoID',
    'intellectual_property_rights': 'iprID',
    'investor': 'investorID',
    'license': 'licenseID',
    'manager': 'managerID',
    'organization_staff': 'organizationStaffID',
    'owner_organization': 'ownerOrganizationID',
    'partnership_coordinator': 'partCoordID',
    'product': 'productID',
    'receiver_organization': 'receiverOrganizationID',
    'technology': 'technologyID',
    'transfer_technology': 'transferID',
    'worker': 'workerID'
}

def get_tables():
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    return tables

@app.route('/')
def index():
    tables = get_tables()
    return render_template('index.html', tables=tables)

def get_primary_key(table):
    return tables_id.get(table, None)
    
@app.route('/select_action', methods=['POST'])
def select_action():
    table_name = request.form['table']
    action = request.form['action']
    return redirect(url_for(action, table=table_name))

@app.route('/add/<table>', methods=['GET', 'POST'])
def add_record(table):
    if request.method == 'POST':
        try:
            columns = get_columns(table)
            values = [request.form[column] for column in columns]
            placeholders = ', '.join(['%s' for _ in values])
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
            cursor.execute(query, values)
            db.connection.commit()  
            
            operation_report = f"Record added to {table} successfully.\n\nExecuted Query:\n\n{query}\n\nValues added: {values}"
            return render_template('report.html', report=operation_report)
        except Exception as e:
            error_message = f"Error adding record to {table}: {str(e)}"
            return render_template('error.html', error_message=error_message)
    else:
        columns = get_columns(table)
        return render_template('add_record.html', table=table, columns=columns)

@app.route('/find/<table>', methods=['GET', 'POST'])
def find_record(table):
    if request.method == 'POST':
        try:
            primary_key = request.form['primary_key']
            query = f"SELECT * FROM {table} WHERE {get_primary_key(table)} = %s"
            cursor.execute(query, (primary_key,))
            result = cursor.fetchone()
            
            if result:
                report = f"Record found in {table}: {result}"
            else:
                report = f"No record found in {table} with ID {primary_key}"

            return render_template('report.html', report=report + '\n' + query)
        except Exception as e:
            error_message = f"Error finding record in {table}: {str(e)}"
            return render_template('error.html', error_message=error_message)
    else:
        return render_template('find_record.html', table=table)

@app.route('/modify/<table>', methods=['GET', 'POST'])
def modify_record(table):
    if request.method == 'POST':
        try:
            primary_key = request.form[f"{table}ID"]
            columns = get_columns(table)
            set_clause = ', '.join([f"{column} = %s" for column in columns if column != f"{table}ID"])
            values = [request.form[column] for column in columns if column != f"{table}ID"]
            values.append(primary_key)
            query = f"UPDATE {table} SET {set_clause} WHERE {get_primary_key(table)} = %s"
            cursor.execute(query, values)
            db.connection.commit()
            report = f"Record modified in {table} successfully."
            return render_template('report.html', report=report + '\n' + query)
        except Exception as e:
            error_message = f"Error modifying record in {table}: {str(e)}"
            return render_template('error.html', error_message=error_message)
    else:
        columns = get_columns(table)
        return render_template('modify_record.html', table=table, columns=columns)


def get_columns(table_name):
    cursor.execute(f"DESCRIBE {table_name}")
    columns = [column[0] for column in cursor.fetchall()]
    return columns

if __name__ == '__main__':
    app.run(debug=True)
