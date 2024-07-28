from flask import Flask , request , render_template , jsonify 
from models import db, Cupcake

app = Flask(__name__, template_folder="templates", static_folder="static")

#Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialize database 
db.init_app(app)


@app.route('/')
def index():
    """render the main page"""
    return render_template('index.html')


@app.route('/api/cupcakes', methods = ['GET'])
def get_cupcakes():
    cupcakes = Cupcake.query.all()
    return jsonify(cupcakes = [cupcake.serialize() for cupcake in cupcakes])


@app.route('/api/cupcakes/<int:id>', methods = ['GET'])
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake = cupcake.serialize())


@app.route('/api/cupcakes', methods = ['POST'])
def new_cupcake():
    data = request.json

    new_cupcake = Cupcake(
        flavor = data['flavor'],
        size = data['size'],
        rating = data['rating'],
        image = data.get('image' or 'https://tinyurl.com/demo-cupcake')
    )

    db.session.add(new_cupcake)
    db.session.commit()

    return jsonify(cupcake = new_cupcake.serialize()), 201


@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """Update a cupcake with the given ID."""
    cupcake = Cupcake.query.get_or_404(id)
    
    # Update fields if they are in the request
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    
    db.session.commit()
    
    return jsonify(cupcake=cupcake.serialize()), 200


@app.route('/edit_cupcake/<int:id>')
def edit_cupcake_page(id):
    return render_template('edit_cupcake.html', id=id, cupcake=Cupcake.query.get_or_404(id))



@app.route('/api/cupcakes/<int:id>', methods = ['DELETE'])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify({'message' : 'deleted cupcake'}), 200 





