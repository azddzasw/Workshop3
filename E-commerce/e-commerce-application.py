#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 18:34:31 2024

@author: azddza
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    in_stock = db.Column(db.Boolean, default=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    total_price = db.Column(db.Float)
    status = db.Column(db.String(50))

@app.route('/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    in_stock = request.args.get('inStock')
    
    query = Product.query
    if category:
        query = query.filter_by(category=category)
    if in_stock == 'true':
        query = query.filter_by(in_stock=True)
        
    products = query.all()
    result = []
    for product in products:
        result.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'category': product.category,
            'in_stock': product.in_stock
        })
    
    return jsonify(result)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    result = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'category': product.category,
        'in_stock': product.in_stock
    }
    return jsonify(result)

@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        category=data['category'],
        in_stock=data['in_stock']
    )
    db.session.add(product)
    db.session.commit()
    
    result = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'category': product.category,
        'in_stock': product.in_stock
    }
    return jsonify(result), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    data = request.json
    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = data['price']
    if 'category' in data:
        product.category = data['category']
    if 'in_stock' in data:
        product.in_stock = data['in_stock']
    
    db.session.commit()
    
    result = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'category': product.category,
        'in_stock': product.in_stock
    }
    return jsonify(result)

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'message': 'Product deleted'})

if __name__ == '__main__':
    app.run(debug=True)