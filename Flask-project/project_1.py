from flask import Flask , render_template , request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, Menu

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(Menu).filter_by(restaurant_id = restaurant.id).all()
	return jsonify(Menu = [i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id,menu_id):
	item = session.query(Menu).filter_by(id = menu_id).one()
	return jsonify(Menu = item.serialize)


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id): 	
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(Menu).filter_by(restaurant_id = restaurant_id)
	return render_template('Menu_template.html', restaurant = restaurant , items = items)

#Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods = ['POST','GET'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newMItem = Menu(name = request.form['name'] ,course = request.form['course'],
			description = request.form['description'],price = request.form['price'],
			restaurant_id = restaurant_id)
		session.add(newMItem)
		session.commit()
		flash("new_menu_item_created!")
		#After creating a new menuItem t should redirect to the home page 
		return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
	else:
		return render_template('newMenuItem_template.html', restaurant_id = restaurant_id)

#Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
	menuItem = session.query(Menu).filter_by(id = menu_id).one()
	if request.method == 'POST':
		menuItem.name = request.form['newMenuItemName']
		session.add(menuItem)
		session.commit()
		flash("You have edited the item !")
		return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
	if request.method == 'GET':
		#item = session.query(Menu).filter_by(id = menu_id).one()
		return render_template('editmenuitem.html', restaurant_id = menuItem.restaurant_id , 
			menu_id = menuItem.id , item = menuItem)
	

#Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	itemToDelete = session.query(Menu).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash("You have deleted the item !")
		return redirect(url_for('restaurantMenu', restaurant_id = itemToDelete.restaurant_id))
	else:
		return render_template('deleteMenuItem.html',item = itemToDelete)

if __name__ == '__main__':
	app.secret_key = "some_secret_key"
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
