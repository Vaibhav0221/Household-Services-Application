from .database import db

class Customer(db.Model):
    Id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True, nullable=False)
    Full_name =db.Column(db.String, nullable=False)
    Email =db.Column(db.String, unique=True, nullable=False)
    Phone_number=db.Column(db.Integer, nullable=False)
    Password =db.Column(db.String, nullable=False)
    Address =db.Column(db.String, nullable=False)
    Pincode =db.Column(db.Integer, nullable=False)
    service_requests = db.relationship('Service_request', backref='customer', lazy=True)

class Professional(db.Model):
    Id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True, nullable=False)
    Full_name =db.Column(db.String, nullable=False)
    Email =db.Column(db.String, unique=True, nullable=False)
    Password =db.Column(db.String, nullable=False)
    Phone_number=db.Column(db.Integer, nullable=False)
    Service_name =db.Column(db.String)
    Address =db.Column(db.String, nullable=False)
    Pincode =db.Column(db.Integer, nullable=False)
    Experience =db.Column(db.Integer)
    Status = db.Column(db.String)
    service_requests = db.relationship('Service_request', backref='professional', lazy=True)
    
class Service(db.Model):
    Service_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True, nullable=False)
    Service_name =db.Column(db.String, nullable=False)
    Price =db.Column(db.Integer, nullable=False)
    Time_required =db.Column(db.Integer, nullable=False)
    Description =db.Column(db.String, nullable=False)
    service_requests = db.relationship('Service_request', backref='service', lazy=True)

class Service_request(db.Model):
    Id = db.Column(db.Integer, primary_key=True, nullable=False)
    Service_id = db.Column(db.Integer, db.ForeignKey('service.Service_id'), nullable=False)
    Customer_id = db.Column(db.Integer, db.ForeignKey('customer.Id'), nullable=False)
    Professional_id = db.Column(db.Integer, db.ForeignKey('professional.Id'))
    date_of_request = db.Column(db.Date, nullable=False)
    date_of_completion = db.Column(db.Date)
    Service_status = db.Column(db.String, nullable=False)
    Remarks=db.Column(db.String)

class Rejected_req(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_req_id = db.Column(db.Integer, db.ForeignKey('service_request.Id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.Id'), nullable=False)