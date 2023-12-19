from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
from model import *
api=Api()


class ProductResource(Resource):
    def get(self):
        products = Product.query.all()
        response = {}
        for product in products:
            m = {
                'name': product.name,
                'manufacture_date': product.manufacture_date,
                'expiry_date': product.expiry_date,
                'rate': product.rate_per_unit,
                'unit': product.unit,
            }
            response[product.p_id] = m
        return response, 200


    def delete(self, product_id):
        p = Product.query.get(product_id)
        if p:
            db.session.delete(p)
            db.session.commit()
            return {'message': 'Item deleted'}, 200
        else:
            return {'message': 'Item not found'}, 404

    def put(self, product_id):
        p = Product.query.get(product_id)
        if not p:
            return {'message': 'Item not found'}, 404

        data = request.json
        p.name = data.get('p_name', p.name)
        p.manufacture_date = data.get('manufacture', p.manufacture_date)
        p.expiry_date = data.get('expiry', p.expiry_date)
        p.rate_per_unit = data.get('rate', p.rate_per_unit)
        p.unit = data.get('unit', p.unit)
        c_id = data.get('c_id')
        category = Category.query.get(c_id)
        if not category:
            return {'message': 'Invalid category ID'}, 400
        p.section.append(category)

        db.session.commit()
        return {'message': 'Item updated'}, 200

    def post(self):
        data = request.json
        p_name = data.get('p_name')
        manufacture = data.get('manufacture')
        expiry = data.get('expiry')
        rate = data.get('rate')
        unit = data.get('unit')
        c_id = data.get('c_id')

        category = Category.query.get(c_id)
        if not category:
            return {'message': 'Invalid category ID'}, 400

        p = Product(name=p_name, manufacture_date=manufacture, expiry_date=expiry, rate_per_unit=rate, unit=unit)
        db.session.add(p)
        p.section.append(category)
        db.session.commit()
        return {'message': 'Item Added'}, 201


class CategoryResource(Resource):
    def get(self):
        categories = Category.query.all()
        response = {}
        for category in categories:
            m = {
                'name': category.name,
                'description':category.description,
            }
            response[category.c_id] = m
        return response, 200
    def delete(self, category_id):
        c = Category.query.get(category_id)
        if c:
            db.session.delete(c)
            db.session.commit()
            return {'message': 'Category deleted'}, 200
        else:
            return {'message': 'Category not found'}, 404


    def put(self, category_id):
        c = Category.query.get(category_id)
        if not c:
            return {'message': 'category not found'}, 404

        data = request.json
        c.name = data.get('name', c.name)
        c.description=data.get('description',c.description)
        db.session.commit()
        return {'message': 'Category updated'}, 200

    def post(self):
        data = request.json
        name=data.get('name')
        description=data.get('description')
        c= Category(name=name,description=description)
        db.session.add(c)
        db.session.commit()
        return {'message': 'Category Added'}, 201




api.add_resource(ProductResource,'/api/all_products', '/api/delete_prod/<int:product_id>', '/api/add_product', '/api/update_prod/<int:product_id>')
api.add_resource(CategoryResource,'/api/all_category','/api/delete_cate/<int:category_id>','/api/add_category','/api/update_cate/<int:category_id>')