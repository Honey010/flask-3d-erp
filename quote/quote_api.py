from flask import Blueprint, Response, abort, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date

from sqlalchemy import func
from database.database_models import Quote,QuoteInfo,UnitQuote, db
# from app import db
import multiprocessing
from mesh_converter import meshRun
import json
import os
import requests
import time

quote_api_blueprint = Blueprint('quote_api_blueprint', __name__)

@quote_api_blueprint.route('/file-upload', methods = ['POST'])
def upload3dFile():
    # breakpoint()
    # POST Request File
    file = request.files["file"]
    # url = "https://wordpress-311437-2997507.cloudwaysapps.com/x-file/test.stp"
    # r = requests.get(url)
    # file = r.content
    uniqueFileName = str(datetime.now().timestamp()).replace(".","")
    uTimeDate = str(uniqueFileName)
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    file.save(f"uploads/{uniqueFileName+file.filename}")
    fileServerPath = 'uploads/'+uTimeDate+file.filename
    while not os.path.exists(fileServerPath):
        print('not saved yet')
        time.sleep(1)
    if not os.path.isfile(fileServerPath):
        return "not saved anyhow"
    ret = {'success': False, "converted_file": "", "image": "", "x":"", "y":"", "z": ""}
    queue = multiprocessing.Queue()
    queue.put(ret)
    p = multiprocessing.Process(target=meshRun, args=(queue,fileServerPath,))
    p.start()
    p.join()
    queueInfo  = queue.get()
    updated_file = f"uploads/{uniqueFileName+file.filename}"
    transported_file = queueInfo['converted_file']
    return jsonify({"Success":True,"updated_file":updated_file,"transported_file":transported_file, "image": queueInfo['image'], "x":queueInfo['x'],"y":queueInfo['y'],"z":queueInfo['z']})


# POST Request


@quote_api_blueprint.route('/quote', methods = ['POST'])
def createQuote():
    # {
    #     "files":{
    #         "transported_file": "uploads/transported/1687436341754127abc.stl",
    #         "updated_file": "uploads/1687436341754127abc.stp"
    #     }
    # }

    updated_file = request.get_json().get('files')['updated_file'] 
    transported_file = request.get_json().get('files')['transported_file']
    quote = Quote(quote_date = str(datetime.now()), validity = None, shipping_cost = None, grand_total = None)
    db.session.add(quote)
    db.session.commit()
    quoteinfo = QuoteInfo(uploded_file = updated_file,transported_file = transported_file ,material_search = None,technique = None,finishing = None,x_size = None,y_size= None,z_size = None,quote_id = quote.id,image_file=None)
    db.session.add(quoteinfo)
    db.session.commit()
    unitquote = UnitQuote(unit_price = None,quantity = None,lead_time=None,quote_info_id=quoteinfo.id)
    db.session.add(unitquote)
    db.session.commit()
    return jsonify(quote.serialize())

# Endpoint belong to create quote info ...
# call to nedd 2 file in the below format...and will return unit-quote data
# Endpoint ex: /quote/19/create-quote-info/
# Request Example below 
#     {
#         "files":{
#             "transported_file": "uploads/transported/1687436341754127abc.stl",
#             "updated_file": "uploads/1687436341754127abc.stp"
#         }
#     }

@quote_api_blueprint.route('/quote/<int:quote_id>/create-quote-info/', methods = ['POST'])
def createQuoteInfo(quote_id):
    quote = Quote.query.get(quote_id)
    if quote is None:
        abort(404)
    else:
        updated_file = request.get_json().get('files')['updated_file'] 
        transported_file = request.get_json().get('files')['transported_file']
        quoteinfo = QuoteInfo(uploded_file = updated_file,transported_file = transported_file ,material_search = None,technique = None,finishing = None,x_size = None,y_size= None,z_size = None,quote_id = quote_id,image_file=None)
        db.session.add(quoteinfo)
        db.session.commit()
        unitquote = UnitQuote(unit_price = None,quantity = None,lead_time=None,quote_info_id=quoteinfo.id)
        db.session.add(unitquote)
        db.session.commit()
        return jsonify(quoteinfo.serialize())
    


# Endpoint belong to create unit quote..
# need  to create unit quote data only..
# Example : /quote-info/6/create-unit-quote
# in json form
# { "unit_price":  ....,
#  "lead_time": ........
# }

@quote_api_blueprint.route('/quote-info/<int:quote_info_id>/create-unit-quote', methods = ['POST'])
def createUnitQuote(quote_info_id):
    quoteInfo = QuoteInfo.query.get(quote_info_id)
    # quote_infoid = request.get_json().get('quote_info_id')
    if quoteInfo is None:
        abort(404)
    else:
        unitquote = UnitQuote(unit_price = None,quantity = None,lead_time=None,quote_info_id=quoteInfo.id)
        db.session.add(unitquote)
        db.session.commit()
        return jsonify(unitquote.serialize())
    

# UPDATE REQUEST...

# Endpoint belong to update unit-quote..
# need unit-quote id and to change data..
# Example-: /unit-quote/
# in json form
# {"id":1,
#   "unit_price": ....
# }


@quote_api_blueprint.route('/unit-quote/', methods = ['PATCH'])
def updateUnitQuote():
    # breakpoint()
    unit_quote = UnitQuote.query.get(request.json["id"])
   
    if unit_quote is None:
        abort(404)
    else:
        db.session.query(UnitQuote).filter_by(id=unit_quote.id).update(request.json)
        db.session.commit()
        return jsonify(unit_quote.serialize())

# Endpoint belong to update quote-info..
# need quote-info id and to change data..
# Example-: /quote-info/
# in json form
#{"id": 4
#  "uploded_file": ....
# }


@quote_api_blueprint.route('/quote-info/', methods = ['PATCH'])
def updateQuoteInfo():
    quote_info = QuoteInfo.query.get(request.json["id"])
    if quote_info is None:
        abort(404)
    else:
        db.session.query(QuoteInfo).filter_by(id=quote_info.id).update(request.json)
        db.session.commit()
        return jsonify(quote_info.serialize())


# Endpoint belong to update quote..
# need quote id and to change data..
# Example-: /quote/
# in json form
#{"id": 4,
# "shipping_cost" : .....,
# }
#
#

@quote_api_blueprint.route('/quote/', methods = ['PATCH'])
def updateQuote():
    quote = Quote.query.get(request.json["id"])
    if quote is None:
        abort(404)
    else:
        db.session.query(Quote).filter_by(id=quote.id).update(request.json)
        db.session.commit()
        # breakpoint()
        return jsonify(quote.serialize())

#DELETE REQUEST


# Endpoint belong to update unit-quote..
# need unit-quote id and to delete data..
# ex- /unit-quote/
# in json form
#{
# "id":5,
# }

@quote_api_blueprint.route("/unit-quote/", methods = ["DELETE"])
def deleteUnitQuote():
    if UnitQuote.query.filter_by(id=request.json["id"]).delete():
        db.session.commit()
        return jsonify({"success":True, "response": "Unit Quote deleted","id":request.json["id"]})
    return jsonify({"success":False, "response": "Unit Quote ID: "+ str(request.json["id"]) +" Not Found"})


# Endpoint belong to update quote-info..
# need quote-info id and to delete data..
# ex- /quote-info/
# in json form
#{
# "id":6
# }

@quote_api_blueprint.route("/quote-info/", methods = ["DELETE"])
def deleteQuoteInfo():
    if QuoteInfo.query.filter_by(id=request.json["id"]).delete():
        db.session.commit()
        return jsonify({"success":True, "response": "Quote Info deleted","id":request.json["id"]})
    return jsonify({"success":False, "response": "Quote Info ID: "+ str(request.json["id"]) +" Not Found"})


# Endpoint belong to update quote..
# need quote id and to delete data..
# ex- /quote/
# in json form
#{
# "id":9
# }
@quote_api_blueprint.route("/quote/", methods = ["DELETE"])
def deleteQuote():
    if Quote.query.filter_by(id=request.json["id"]).delete():
        db.session.commit()
        return jsonify({"success":True, "response": "Quote deleted","id":request.json["id"]})
    return jsonify({"success":False, "response": "Quote ID: "+ str(request.json["id"]) +" Not Found"})

#GET REQUEST


# Endpoint belong to Get unit-quote..
# need unit-quote id to get quote in url..


@quote_api_blueprint.route('/unit-quote/<int:unit_quote_id>', methods = ['GET'])
def getUnitQuote(unit_quote_id):
    unit_quote = UnitQuote.query.get(unit_quote_id)
    return jsonify(unit_quote.serialize())

# Endpoint belong to Get quote-info..
# need quote-info id to get quote in url..

@quote_api_blueprint.route('/quote-info/<int:quote_info_id>', methods = ['GET'])
def getQuoteInfo(quote_info_id):
    quote_info = QuoteInfo.query.get(quote_info_id)
    return jsonify(quote_info.serialize())


# Endpoint belong to Get quote..
# need quote id to get quote in url.. ex: /quote/19
@quote_api_blueprint.route('/quote/<int:quote_id>', methods = ['GET'])
def getQuote(quote_id):
    quote = Quote.query.get(quote_id)
    return jsonify(quote.serialize())


# Endpoint belong to Get all quote

@quote_api_blueprint.route('/quotes/', methods = ['GET'])
def getAllQuotes():
    quotes = Quote.query.all()
    result = [quote.serialize() for quote in quotes]
    return jsonify(result)

@quote_api_blueprint.route('/unit-quotes/', methods = ['GET'])
def getAllUnitQuote():
    unit_quotes = UnitQuote.query.all()
    result = [unit_quotes.serialize() for unit_quotes in unit_quotes]
    return jsonify(result)


@quote_api_blueprint.route('/quote-infos/', methods = ['GET'])
def getAllQuoteInfo():
    quote_infos = QuoteInfo.query.all()
    result = [quote_infos.serialize() for quote_infos in quote_infos]
    return jsonify(result)

# Endpoint
# query to get quote by date..
# Quote by date(single day) by get parameters ex. /quotes-by-date/?date=2023-06-22
@quote_api_blueprint.route('/quotes-by-date/', methods = ['GET'])
def getAllQuoteByDate():
    quotes = Quote.query.filter(func.date(Quote.quote_date)==request.args.get('date') ).all()
    result = [quote.serialize() for quote in quotes]
    return jsonify(result)



@quote_api_blueprint.route('/quotes-b/w-date/', methods = ['GET'])
def getAllQuoteBetweenDate():
    # breakpoint()
    quotes = Quote.query.filter(func.date(Quote.quote_date).between(request.args.get('date'),request.args.get('end'))).all()
    result = [quote.serialize() for quote in quotes]
    return jsonify(result)