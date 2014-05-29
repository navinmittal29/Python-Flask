from flask import *
from functools import wraps
import sqlite3

DATABASE = 'tickets.db'

app=Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "navin"

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])


	
def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first')
			return redirect(url_for('log'))
	return wrap

@app.route('/alltickets/')
@login_required
def alltickets():
    g.db = connect_db()
	
    cur = g.db.execute('select issue, due_date, priority, ticket_id from mytickets where status=1')
    open_tickets = [dict(issue=row[0], due_date=row[1], priority=row[2], ticket_id=row[3]) for row in cur.fetchall()]
	
    cur = g.db.execute('select issue, due_date, priority, ticket_id from mytickets where status=0')
    closed_tickets = [dict(issue=row[0], due_date=row[1], priority=row[2], ticket_id=row[3]) for row in cur.fetchall()]
	
    g.db.close()
    return render_template('alltickets.html', open_tickets=open_tickets, closed_tickets=closed_tickets)
	
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You are logged out')
	return redirect (url_for('log'))

@app.route('/', methods=['GET', 'POST'])
def log():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'navin' or request.form['password'] != 'navin':
			error = 'Invalid credentials. Please try again.'
		else:
			session['logged_in'] = True
			return redirect(url_for('alltickets'))
	return render_template('log.html', error=error)

		
@app.route('/add/', methods=['POST'])
@login_required
def new_ticket():
    g.db = connect_db()
    issue = request.form['issue']
    date = request.form['due_date']
    priority = request.form['priority']
    if not issue or not date or not priority:
        flash("All fields are required.")
        return redirect(url_for('alltickets'))
    else:
        g.db.execute('insert into mytickets (issue, due_date, priority, status) values (?, ?, ?, 1)',
         [request.form['issue'], request.form['due_date'], request.form['priority']])
        g.db.commit()
        g.db.close()
        flash('New entry was successfully raised.')
        return redirect(url_for('alltickets'))		
		
@app.route('/delete/<int:ticket_id>',)
@login_required
def delete_ticket(ticket_id):
	g.db = connect_db()
	cur = g.db.execute('delete from mytickets where ticket_id='+str(ticket_id))
	g.db.commit()
	g.db.close()
	flash('The ticket was deleted')
	return redirect(url_for('alltickets'))
	
@app.route('/complete/<int:ticket_id>',)
@login_required
def complete(ticket_id):
	g.db = connect_db()
	cur = g.db.execute('update mytickets set status=0 where ticket_id='+str(ticket_id))
	g.db.commit()
	g.db.close()
	flash('The ticket was successfully solved')
	return redirect(url_for('alltickets'))
	
	
if __name__=='__main__':
	app.run(debug=True)