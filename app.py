from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, Ad
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists!"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200


@app.route('/ads', methods=['POST'])
@jwt_required()
def create_ad():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title or not description:
        return jsonify({"message": "Title and description are required"}), 400

    user_id = get_jwt_identity()
    new_ad = Ad(title=title, description=description, owner_id=user_id)
    db.session.add(new_ad)
    db.session.commit()

    return jsonify({"message": "Ad created successfully!"}), 201


@app.route('/ads/<int:ad_id>', methods=['GET'])
def get_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    return jsonify({
        'id': ad.id,
        'title': ad.title,
        'description': ad.description,
        'created_at': ad.created_at,
        'owner_id': ad.owner_id
    })

@app.route('/ads/<int:ad_id>', methods=['PUT'])
@jwt_required()
def update_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    user_id = get_jwt_identity()

    if ad.owner_id != user_id:
        return jsonify({"message": "You are not authorized to update this ad"}), 403

    data = request.get_json()
    ad.title = data.get('title', ad.title)
    ad.description = data.get('description', ad.description)

    db.session.commit()

    return jsonify({"message": "Ad updated successfully!"}), 200

@app.route('/ads/<int:ad_id>', methods=['DELETE'])
@jwt_required()
def delete_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    user_id = get_jwt_identity()

    if ad.owner_id != user_id:
        return jsonify({"message": "You are not authorized to delete this ad"}), 403

    db.session.delete(ad)
    db.session.commit()

    return jsonify({"message": "Ad deleted successfully!"}), 200


if __name__ == '__main__':
    db.create_all(app=app)
    app.run(debug=True)
