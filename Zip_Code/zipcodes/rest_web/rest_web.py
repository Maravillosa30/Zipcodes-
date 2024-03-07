# Restful interface that has search and update options for navigating a Zip code database on Phpmyadmin.


# https://stackoverflow.com/questions/8211128/multiple-distinct-pages-in-one-html-file
# https://stackoverflow.com/questions/902408/how-to-use-variables-in-sql-statement-in-python
# https://stackoverflow.com/questions/1081750/python-update-multiple-columns-with-python-variables
# https://stackoverflow.com/questions/7478366/create-dynamic-urls-in-flask-with-url-for
# https://github.com/vimalloc/flask-jwt-extended/issues/175

from flask import Flask, redirect, url_for, request, render_template
import mysql.connector

app = Flask(__name__)

# Connect to database
# Connect to database
conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='zipcodes', buffered=True)
cursor = conn.cursor()


# Search zipcodes database
@app.route('/searchzip/<searchzip>')
def searchzip(searchzip):
    cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s", [searchzip])
    results = cursor.fetchall()
    if not results:
        return f"{searchzip} was not found"
    else:
        return 'Success! Here you go: %s' % results


# Update zipcodes database population for a specified zipcode
@app.route('/updatezipcodespopulation/<updateZIP>/<updatePopulation>')
def updatezipcodespopulation(updateZIP, updatePopulation):
    cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s", [updateZIP])
    test = cursor.rowcount
    if test != 1:
        return f"{updateZIP} was not found"
    else:
        cursor.execute("UPDATE `zipcodes` SET Population = %s WHERE zip= %s;", [updatePopulation, updateZIP])
        conn.commit()
        cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s and Population=%s", [updateZIP, updatePopulation])
        test1 = cursor.rowcount
        if test1 != 1:
            return f"Failed to update {updateZIP}"
        else:
            return f"Population has been updated successfully for zip: {updateZIP}"


# Update webpage
@app.route('/update', methods=['POST'])
def update():
    user = request.form['uzip']
    user2 = request.form['upopulation']
    return redirect(url_for('updatezipcodespopulation', updateZIP=user, updatePopulation=user2))


# Search page
@app.route('/search', methods=['GET'])
def search():
    user = request.args.get('zip')
    return redirect(url_for('searchzip', searchzip=user))


# Root of web server and gets to template (login.html)
@app.route('/')
def root():
    return render_template('login.html')


# Main
if __name__ == '__main__':
    app.run(debug=True)

