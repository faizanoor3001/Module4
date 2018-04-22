from flask import Flask , render_template
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, Menu

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

newMenuItemForm = '''
				<!doctype html>
				<title>Create a new menu item</title>
				<form method = 'POST' action = >
				<h2>Create a new menu item, and enter the following details below</h2>
				<table>
				<tr>
				<td><label for='name'>Name</label></td>
				<td><input  name ='name' id ='name' type = 'text'></td>
				</tr>
				<tr>
				<td><label for='course'>Course</label></td>
				<td><input  name ='course' id ='course' type = 'text'></td>
				</tr>
				<tr>
				<td><label for='description'>Description</label></td>
				<td><input  name ='description' id ='description' type = 'text'></td>
				</tr>
				<tr>
				<td><label for='price'>Price</label></td>
				<td><input  name ='price' id ='price' type = 'text'></td>
				</tr>
				<tr>
				<td><label for='restaurant_id'>Restaurant_id</label></td>
				<td><input  name ='restaurant_id' id ='restaurant_id' type = 'text'></td>
				</tr>
				<tr>
				<td></td>
				<td><input name ='create' id ='submit' type = 'submit'></td>
				</tr>
				</table>
				</form>
				</html>
				'''

@app.route('/')
def DefaultRestaurantMenu():
	restaurant = session.query(Restaurant).first()
	items = session.query(Menu).filter_by(restaurant_id = restaurant.id)
	output = ''
	for i in items:
		output += i.name
		output += '</br>'
		output += i.price
		output += '</br>'
		output += i.description
		output += '</br>'
		output += '</br>'
		
	return output
	
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(Menu).filter_by(restaurant_id = restaurant_id)
	return render_template('Menu_template.html', restaurant = restaurant , items = items)

#Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):

	return newMenuItemForm

#Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
	return "page to edit a new menu item. Task 2 complete!"

#Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
			return "page to delete a new menu item. Task 3 complete!"

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
