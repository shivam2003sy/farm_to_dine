from logging import Logger
from app import app , api  ,db
from app.models import User , Service ,Crop ,Contract ,Clause
from flask import request, jsonify
import jwt
from datetime import datetime 
from app.util import  token_required
from flask_restful import Resource
from werkzeug.utils import secure_filename
from app.util import allowed_file
from app.models import User 
import os
# function to calculate distance between two points using latitude and longitude
from math import cos, asin, sqrt


#  new user created  sucess
@app.route("/api/users/create", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or not data["username"] or not data["email"] or not data["password"]:
        return {
            "message": "Please provide username, email and password!",
            "data": None,
            "error": "Bad Request"
        }, 400
    if User().get_by_username(data["username"]):
        return {
            "message": "User already exists!",
            "data": None,
            "error": "Bad Request"
        }, 400
    if (data['isfarmer']):
        new_user = User(
            user=data["username"],
            email=data["email"],
            password=data["password"],
            isfarmer=data["isfarmer"],
            isowner = data["isowner"],
        )
    else:
         new_user = User(
            user=data["username"],
            email=data["email"],
            password=data["password"])
    new_user.save()
    return {
        "message": "User created successfully! name  :" + str(new_user.user)+"id :"+str(new_user.id)+"email :  "+str(new_user.email),
        "data": new_user.to_json(),
        "error": None
    }, 201 
# login user  sucess
@app.route("/api/users/login", methods=["POST"])
def login_api():
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        user = User().login(
            data["username"],
            data["password"]
        )
        if user:
            try:
                # token should expire after 24 hrs
                user["id"] = jwt.encode(
                    {"id": user["id"]},
                    app.config["SECRET_KEY"],
                    algorithm="HS256"
                )
                return {
                    "message": "Successfully fetched auth token",
                    "data": user
                }
            except Exception as e:
                return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500
        return {
            "message": "Error fetching auth token!, invalid email or password",
            "data": None,
            "error": "Unauthorized"
        }, 404
    except Exception as e:
        return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": None
        }, 500




# get farmer profile
@app.route("/api/users/farmer", methods=["GET"] ,endpoint="get_farmer" )
@token_required
def get_farmer(current_user):
    try:
        user = User().get_by_id(current_user.id)
        if user:
            return {
                "message": "User fetched successfully!",
                "data": user.to_json(),
                "error": None
            }, 200
        return {
            "message": "User not found!",
            "data": None,
            "error": "Not Found"
        }, 404
    except Exception as e:
        return {
            "message": "Something went wrong!",
            "error": str(e),
            "data": None
        }, 500
# set latitude and longitude
@app.route("/api/users/farmer/location", methods=["POST"] , endpoint="set_location")
@token_required
def set_location(current_user):
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        user = User().get_by_id(current_user.id)
        if user:
            user.latitude = data["latitude"]
            user.longitude = data["longitude"]
            user.save()
            return {
                "message": "User location updated successfully!",
                "data": user.to_json(),
                "error": None
            }, 200
        return {
            "message": "User not found!",
            "data": None,
            "error": "Not Found"
        }, 404
    except Exception as e:
        return {
            "message": "Something went wrong!",
            "error": str(e),
            "data": None
        }, 500
    
# create listing
@app.route("/api/listing", methods=["POST"] , endpoint="create_listing")
def create_listing():
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        new_listing = Service(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            phone=data["phone"],
            service_name = data["service_name"]
        )
        new_listing.save()
        return {
            "message": "Listing created successfully! name  :" + str(new_listing.name)+"id :"+str(new_listing.id)+"price :  "+str(new_listing.price),
            "data": new_listing.to_json(),
            "error": None
        }, 201
    except Exception as e:
        return {
            "message": "Something went wrong!",
            "error": str(e),
            "data": None
        }, 500

import geopy.distance
def distance(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2,lon2)
    dis =  geopy.distance.geodesic(coords_1, coords_2).km
    app.logger.info(dis)
    return dis

# get listing by distance using latitude and longitude
@app.route("/api/listing", methods=["GET"] , endpoint="get_listing")
@token_required
def get_listing(current_user):
    lat  = current_user.latitude
    lon = current_user.longitude
    service = Service.query.all()
    output = []
    for i in service:
        if distance(lat,lon,i.latitude,i.longitude) < 10:
            output.append(i.to_json())
    app.logger.info(output)
    return {
        "message": "Listing fetched successfully!",
        "data": output,
        "error": None
    }, 200



# create crop by farmer
@app.route("/api/crop", methods=["POST"] , endpoint="create_crop")
@token_required
def create_crop(current_user):
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        new_crop = Crop(
            name=data["name"],
            price=data["price"],
            Area=data["area"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            phone = data["phone"],
            user_id = current_user.id
        )
        new_crop.save()
        return {
            "message": "Crop created successfully! name  :" + str(new_crop.name)+"id :"+str(new_crop.id)+"price :  "+str(new_crop.price),
            "data": new_crop.to_json(),
            "error": None
        }, 201
    except Exception as e:
        return {
            "message": "Something went wrong!",
            "error": str(e),
            "data": None
        }, 500

# get crop listed by farmer
@app.route("/api/crop", methods=["GET"] , endpoint="get_crop")
@token_required
def get_crop(current_user):
    try:
        crops = Crop.query.filter_by(user_id=current_user.id).all()
        output = []
        for crop in crops:
            output.append(crop.to_json())
        return {
            "message": "Crops fetched successfully!",
            "data": output,
            "error": None
        }, 200
    except Exception as e:
        return {
            "message": "Something went wrong!",
            "error": str(e),
            "data": None
        }, 500


# POST THE CONTRACT DETAILS
@app.route("/api/contract", methods=["POST"] , endpoint="create_contract")
@token_required
def create_contract(current_user):
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        new_contract = Contract(
            price=data["price"],
            area=data["area"],
            name = data["name"],
            user_id = current_user.id,
            
        )
        new_contract.save()
        return {
            "message": "Contract created successfully! name  :" + str(new_contract.name)+"id :"+str(new_contract.id)+"price :  "+str(new_contract.price),
            "data": new_contract.to_json(),
            "error": None
        }, 201
    except Exception as e:
        return {
            "message": "Something went wrong!",
            "error": str(e),
            "data": None
        }, 500
# get all contracts active 
@app.route("/api/contract", methods=["GET"] , endpoint="get_contract")
@token_required
def get_contract(current_user):
    try:
        contracts = Contract.query.filter_by(user_id=current_user.id).all()
        output = []
        for contract in contracts:
            output.append(contract.to_json())
        return {
            "message": "Contracts fetched successfully!",
            "data": output,
            "error": None
        }, 200
    except Exception as e:
        return {
            "message": "Something went wrong!",
            "error": str(e),
            "data": None
        }, 500
    

#  post clauses for contract using contract id
@app.route("/api/clause", methods=["POST"] , endpoint="create_clause")
@token_required
def create_clause(current_user):
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        new_clause = Clause(
            clause=data["clause"],
            contract_id = data["contract_id"]
        )
        new_clause.save()
        return {
            "message": "Clause created successfully! name  :" + str(new_clause.clause)+"id :"+str(new_clause.id),
            "data": new_clause.to_json(),
            "error": None
        }, 201
    except Exception as e:
        return {
            "message": "Something went wrong!",
            "error": str(e),
            "data": None
        }, 500
    

# get all clauses for a contract using contract id
@app.route("/api/clause", methods=["GET"] , endpoint="get_clause")
@token_required
def get_clause(current_user):
    try:
        clauses = Clause.query.filter_by(contract_id=current_user.id).all()
        output = []
        for clause in clauses:
            output.append(clause.to_json())
        return {
            "message": "Clauses fetched successfully!",
            "data": output,
            "error": None
        }, 200
    except Exception as e:
        return {
            "message": "Something went wrong!",
            "error": str(e),
            "data": None
        }, 500
    

