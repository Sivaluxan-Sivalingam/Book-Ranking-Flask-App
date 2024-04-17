from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
db = mysql.connector.connect(
    host="dataprogramming-project.c1ge4vi7lkbt.us-east-2.rds.amazonaws.com",
    user="admin",
    password="Sivaluxan",
    database="TEST_DB"
)

# Route to display the dropdown form
@app.route('/')
def dropdown_form():
    # Fetch values from SQL table
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT list_name FROM list_table")
    values = cursor.fetchall()
    cursor.close()
    return render_template('bestseller_form.html', values=values)
    # return render_template('dropdown_form.html')

# Route to handle form submission and execute SQL query
@app.route('/result', methods=['POST'])
def query_result():
    selected_value = request.form['selected_value']
    print(selected_value)
    cursor = db.cursor()
    query = "SELECT title,book_rank, author, rank_last_week, weeks_on_list FROM book_table where list_id=(SELECT list_id FROM list_table WHERE list_name=%s)"
    cursor.execute(query, (selected_value,))
    result = cursor.fetchall()
    print(result)
    cursor.close()
    return render_template('table_visualization.html', data=result)


# # Route to fetch data and render the template
# @app.route('/')
# def display_table():
#     cursor = db.cursor()
#     cursor.execute("SELECT list_id,title,book_rank FROM book_table")
#     data = cursor.fetchall()
#     cursor.close()
#     return render_template('table_visualization.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, port=7843)
