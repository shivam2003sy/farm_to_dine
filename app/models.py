from app import db
from flask_login import UserMixin
import jwt
import time

class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(64),unique = True)
    email = db.Column(db.String(120),unique = True)
    password = db.Column(db.String(500))
    isfarmer = db.Column(db.Boolean , default = False)
    isowner = db.Column(db.Boolean , default = False)
    latitude = db.Column(db.Numeric())
    longitude = db.Column(db.Numeric())
    def get_by_id(self,id):
        return User.query.filter_by(id=id).first()
    def get_by_username(self,username):
        return User.query.filter_by(user=username).first()
    def get_all(self):
        return User.query.all()
    def __repr__(self):
        return str(self.id) + ' - ' + str(self.user)
    def save(self):
        # inject self into db session    
        db.session.add( self )
        # commit change and save the object
        db.session.commit()
        return self 
    def to_json(self):
        json_user = {
            'id': self.id,
        'user': self.user,
            'email': self.email,
            'isfarmer' : self.isfarmer,
            'isowner' : self.isowner
        }
        return json_user
    def from_json(self, json_user):
        self.user = json_user.get('user')
        self.email = json_user.get('email')
        self.password = json_user.get('password')
        self.isfarmer = json_user.get('isfarmer')
        self.isowner = json_user.get('isowner')
        return self
    def verify_password(self, password):
        return self.password == password
    
    def login(self, username, password):
        user = User.query.filter_by(user=username).first()
        if user and user.verify_password(password):
            return user.to_json()
        return None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
#  modal for farmerclass 

    
#  modal to list services for agriculture
class Service(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    service_name = db.Column(db.String(64))
    description = db.Column(db.String(64))
    price = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    latitude = db.Column(db.Numeric())
    longitude = db.Column(db.Numeric())
    def get_by_id(self,id):
        return Service.query.filter_by(id=id).first()
    def get_by_name(self,name):
        return Service.query.filter_by(name=name).first()
    def get_all(self):
        return Service.query.all()
    def __repr__(self):
        return str(self.id) + ' - ' + str(self.name)
    def save(self):
        # inject self into db session    
        db.session.add( self )
        # commit change and save the object
        db.session.commit()
        return self 
    def to_json(self):
        json_service = {
            'id': self.id,
            'name': self.name,
            'service_name': self.service_name,
            'description': self.description,
            'price': self.price,
            'phone': self.phone,
            'latitude': self.latitude,
            'longitude': self.longitude

        }
        return json_service
    def from_json(self, json_service):
        self.name = json_service.get('name')
        self.service_name = json_service.get('service_name')
        self.description = json_service.get('description')
        self.price = json_service.get('price')
        self.phone = json_service.get('phone')
        self.latitude = json_service.get('latitude')
        self.longitude = json_service.get('longitude')
        return self
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self



#  modal for crop add by farmer
class Crop(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    Area = db.Column(db.String(64))
    price = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    latitude = db.Column(db.Numeric())
    longitude = db.Column(db.Numeric())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def get_by_id(self,id):
        return Crop.query.filter_by(id=id).first()
    def get_by_name(self,name):
        return Crop.query.filter_by(name=name).first()
    def get_all(self):
        return Crop.query.all()
    def __repr__(self):
        return str(self.id) + ' - ' + str(self.name)
    def save(self):
        # inject self into db session    
        db.session.add( self )
        # commit change and save the object
        db.session.commit()
        return self 
    def to_json(self):
        json_crop = {
            'id': self.id,
            'name': self.name,
            'area': self.Area,
            'price': self.price,
            'phone': self.phone,
            'latitude': self.latitude,
            'longitude': self.longitude

        }
        return json_crop
    def from_json(self, json_crop):
        self.name = json_crop.get('name')
        self.quantity = json_crop.get('quantity')
        self.price = json_crop.get('price')
        self.phone = json_crop.get('phone')
        self.latitude = json_crop.get('latitude')
        self.longitude = json_crop.get('longitude')
        return self
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self



#  farm contract by user
class Contract(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    area = db.Column(db.String(64))
    price = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def get_by_id(self,id):
        return Contract.query.filter_by(id=id).first()
    def get_by_name(self,name):
        return Contract.query.filter_by(name=name).first()
    def get_all(self):
        return Contract.query.all()
    def __repr__(self):
        return str(self.id) + ' - ' + str(self.name)
    def save(self):
        # inject self into db session    
        db.session.add( self )
        # commit change and save the object
        db.session.commit()
        return self
    def to_json(self):
        json_contract = {
            'id': self.id,
            'name': self.name,
            'area': self.area,
            'price': self.price,
            'user_id': self.user_id
        }
        return json_contract
    def from_json(self, json_contract):
        self.name = json_contract.get('name')
        self.area = json_contract.get('area')
        self.price = json_contract.get('price')
        self.user_id = json_contract.get('user_id')
        return self
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self


# clauses for contract using id 
class Clause(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    clause = db.Column(db.String(64))
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'))
    def get_by_id(self,id):
        return Clause.query.filter_by(id=id).first()
    def get_by_name(self,name):
        return Clause.query.filter_by(name=name).first()
    def get_all(self):
        return Clause.query.all()
    def __repr__(self):
        return str(self.id) + ' - ' + str(self.name)
    def save(self):
        # inject self into db session    
        db.session.add( self )
        # commit change and save the object
        db.session.commit()
        return self
    def to_json(self):
        json_clause = {
            'id': self.id,
            'name': self.name,
            'clause': self.clause,
            'contract_id': self.contract_id
        }
        return json_clause
    def from_json(self, json_clause):
        self.name = json_clause.get('name')
        self.clause = json_clause.get('clause')
        self.contract_id = json_clause.get('contract_id')
        return self
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self




