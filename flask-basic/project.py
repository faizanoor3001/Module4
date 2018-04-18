from flask import Flask
app = Flask(__name__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base , Restaurant , Menu

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/hello')
@app.route('/restaurants/<int:restaurant_id>')
def HelloWorld(restaurant_id):
	# as the first one is having no menu items , so manually hardcoding 3 and getting menu items
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	# query 1 items = session.query(Menu).filter_by(restaurant_id = 3)
	#query 2 items = session.query(Menu).all()
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
		#print(output)
	return output

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0' , port = 5000)
