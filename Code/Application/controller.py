from flask import Flask, render_template, request, redirect
from flask import current_app as app
from Application.models import Customer, Professional, Service, Service_request, Rejected_req
from Application.database import db

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

Admin_email='admin@gmail.com'
Admin_pass='123'

from datetime import date
today=date.today()

@app.route('/', methods=["GET", "POST"])
def Login():
    if request.method=="GET":
        return render_template('login.html',error=0)
    
    Login_data=request.form

    Login_email=Login_data['email']
    Login_pass=Login_data['password']
    
    if Login_email and Login_pass:
        if Login_email==Admin_email:
            if Login_pass==Admin_pass:
                return redirect('/Admin/Home')

        Customers_emails=[i.Email for i in Customer.query.all()]
        if Login_email in Customers_emails:
            if(Login_pass==Customer.query.filter_by(Email=Login_email).first().Password):
                Customer_id=Customer.query.filter_by(Email=Login_email).first().Id
                return redirect(f'/Customer/Home/{Customer_id}')

        Professional_emails=[i.Email for i in Professional.query.all()]
        if Login_email in Professional_emails:
            if(Login_pass==Professional.query.filter_by(Email=Login_email).first().Password):
                if Professional.query.filter_by(Email=Login_email).first().Status=="Approve":
                    Professional_id=Professional.query.filter_by(Email=Login_email).first().Id
                    return redirect(f'/Professional/Home/{Professional_id}')
    return render_template('Login.html',error=1)



#Admin
@app.route('/Admin/Home', methods=["GET"])
def Admin():
    All_Services=Service.query.all()
    All_Professional=Professional.query.all()
    All_Customer=Customer.query.all()
    All_Service_requests=Service_request.query.all()
    All_request_join_1 = db.session.query(
        Service_request.Id,
        Customer.Full_name,
        Service.Service_name,
        Service_request.Service_status
        ).join(Customer, Service_request.Customer_id == Customer.Id
        ).join(Service, Service_request.Service_id == Service.Service_id
        ).filter(Service_request.Service_status == "Requested").all()
    All_request_join_2 = db.session.query(
        Service_request.Id,
        Customer.Full_name,
        Service.Service_name,
        Professional.Full_name,
        Service_request.Service_status
        ).join(Customer, Service_request.Customer_id == Customer.Id
        ).join(Professional, Service_request.Professional_id == Professional.Id
        ).join(Service, Service_request.Service_id == Service.Service_id).all()
    return render_template('Admin_home.html', S_data=All_Services,C_data=All_Customer, P_data=All_Professional, S_R_data=All_Service_requests,All1=All_request_join_1 ,All2=All_request_join_2)

@app.route('/Admin/Home/New_Service',methods=["GET","POST"])
def A_New_Service():
    if request.method=="GET":
        return render_template('Admin_new_service.html',update=0)
    New_Service_data=request.form
    New_Service=Service(Service_name=New_Service_data['name'],Price=New_Service_data['price'],Description=New_Service_data['description'],Time_required=New_Service_data['time_required'])
    db.session.add(New_Service)
    db.session.commit()
    return redirect('/Admin/Home')

@app.route('/Admin/Home/Service/<int:S_id>', methods=["GET"])
def A_S_details(S_id):
    A_S_Request_of_S_id_requested=db.session.query(
        Service_request.Id,
        Service.Service_name,
        Customer.Full_name,
        None,
        Service_request.date_of_request,
        None,
        None,
        Service_request.Service_status
        ).join(Service, Service_request.Service_id == S_id
        ).join(Customer, Customer.Id == Service_request.Customer_id
        ).filter(Service.Service_id == S_id
        ).filter(Service_request.Service_status=="Requested")
    A_S_Request_of_S_id_closed=db.session.query(
        Service_request.Id,
        Service.Service_name,
        Customer.Full_name,
        Professional.Full_name,
        Service_request.date_of_request,
        Service_request.date_of_completion,
        Service_request.Remarks,
        Service_request.Service_status
        ).join(Service, Service_request.Service_id == S_id
        ).join(Customer, Customer.Id == Service_request.Customer_id
        ).join(Professional, Professional.Id==Service_request.Professional_id
        ).filter(Service.Service_id == S_id)
    A_S_Request_of_S_id = A_S_Request_of_S_id_closed.union_all(A_S_Request_of_S_id_requested)
    return render_template("Admin_Services.html",S_id=S_id,service=A_S_Request_of_S_id.all())

@app.route('/Admin/Home/Service/Edit/<int:S_id>', methods=["GET","POST"])
def A_S_edit_details(S_id):
    A_S=Service.query.filter_by(Service_id=S_id).first()
    if request.method=="GET":
        return render_template("Admin_edit_service.html",service=A_S)
    A_S_new_data=request.form
    A_S.Service_name = A_S_new_data['name']
    A_S.Price = A_S_new_data['price']
    A_S.Description = A_S_new_data['description']
    A_S.Time_required = A_S_new_data['time_required']
    db.session.commit()
    return redirect('/Admin/Home')

@app.route('/Admin/Home/Service/Delete/<int:S_id>', methods=["GET","POST"])
def A_S_delete(S_id):
    service = Service.query.get(S_id)
    service_requests = Service_request.query.filter_by(Service_id=S_id).all()
    for service_request in service_requests:
        db.session.delete(service_request)
    Service_name=service.Service_name
    professionals = Professional.query.filter_by(Service_name=Service_name).all()
    for professional in professionals:
        db.session.delete(professional)
    db.session.delete(service)
    db.session.commit()
    return redirect('/Admin/Home')


@app.route('/Admin/Home/Professional/<int:S_id>', methods=["GET"])
def A_P_details(S_id):
    P_S=Professional.query.filter_by(Id=S_id).first()
    return render_template("Admin_professional.html",prof=P_S)

@app.route('/Admin/Professional/<int:P_id>/<string:Status>')
def A_P_Approve(P_id,Status):
    P_S=Professional.query.filter_by(Id=P_id).first()
    if Status=="Delete":
        db.session.delete(P_S)
    else:
        P_S.Status=Status
    db.session.commit()
    return redirect('/Admin/Home')

@app.route('/Admin/Customer/<int:C_id>', methods=["GET"])
def A_C_details(C_id):
    C_S=Customer.query.filter_by(Id=C_id).first()
    return render_template("Admin_Customer.html",prof=C_S)

@app.route('/Admin/Customer/<int:C_id>/Delete', methods=["GET"])
def A_C_delete(C_id):
    N_Customer=Customer.query.filter_by(Id=C_id).first()
    db.session.delete(N_Customer)
    db.session.commit()
    return redirect('/Admin/Home')


from sqlalchemy.sql import literal

@app.route('/Admin/Search', methods=["GET","POST"])
def A_Search():
    data=None
    Services=['Customer_name','Professional_name','Service_name','Status']
    if request.method=="GET":
        return render_template('Admin_Search.html',services=Services)
    All_data=request.form
    field=All_data['servicename']
    value=All_data['search_element']
    
    query_Requested = db.session.query(
    Service_request.Id,
    Customer.Full_name.label('C_name'),
    literal("N/A").label('P_name'),
    Service.Service_name.label('S_name'),
    Service_request.Service_status.label('Status')
    ).join(Customer, Service_request.Customer_id == Customer.Id
    ).join(Service, Service_request.Service_id == Service.Service_id
    ).filter(Service_request.Service_status == "Requested")
    query_closed = db.session.query(
    Service_request.Id,
    Customer.Full_name.label('C_name'),
    Professional.Full_name.label('P_name'),
    Service.Service_name.label('S_name'),
    Service_request.Service_status.label('Status')
    ).join(Customer, Service_request.Customer_id == Customer.Id
    ).join(Professional, Service_request.Professional_id == Professional.Id
    ).join(Service, Service_request.Service_id == Service.Service_id)
    
    query = query_Requested.union_all(query_closed)

    if field=='Customer_name':
        data = [i for i in query.all() if value.lower() in i.C_name.lower()]
    elif field=='Professional_name':
        data = [i for i in query.all() if value.lower() in i.P_name.lower()]
    elif field=='Service_name':
        data=[i for i in query.all() if value.lower() in i.S_name.lower()]
    elif field=='Status':
        data = [i for i in query.all() if value.lower() in i.Status.lower()]
    if data==None or data==[]:
        return render_template('Admin_Search.html',services=Services,res=2)
    return render_template('Admin_Search.html',services=Services,res=1,req_data=data)

@app.route('/Admin/Summary', methods=["GET"])
def A_Summary():
    A_R_Status=[i.Service_status for i in Service_request.query.all()]
    all_defualt_status=['Closed', 'Requested','Assigned']
    frequency = {i: 0 for i in all_defualt_status}
    for i in A_R_Status:
        frequency[i]+=1
    labels=list(frequency.keys())
    y=list(frequency.values())
    x=[i*100/sum(y) for i in y]
    plt.figure()
    plt.pie(x,labels=labels, autopct='%1.1f%%')
    plt.title("ALL Service Status")
    plt.savefig('static/Images/A_Summary_1.jpg')
    plt.close()

    services = [service[0] for service in db.session.query(Service.Service_name).distinct().all()]
    all_services=[a.Service_name for a in Service.query.all()]
    frequency1 = {i: 0 for i in services}
    for i in all_services:
        frequency1[i]+=1

    x=list(frequency1.keys())
    y=list(frequency1.values())
    plt.bar(x,y)
    plt.xlabel('Service Categories')
    plt.ylabel('Number of Requests')
    plt.title('Service Requests by Category')
    plt.savefig('static/Images/A_Summary_2.jpg')
    plt.close()
    return render_template('Admin_Summary.html')




@app.route('/Customer/Register', methods=["GET","POST"])
def create_customer():
    if request.method=="GET":
        return render_template('Customer_register.html')
    Customer_data=request.form
    New_Customer=Customer(Full_name=Customer_data['fullname'],Email=Customer_data['email'],Password=Customer_data['password'], Address=Customer_data['address'],Pincode=Customer_data['pin'],Phone_number=Customer_data['phone_number'])
    ALL_Customer=[i.Email for i in Customer.query.all()]
    if New_Customer.Email not in ALL_Customer:
        db.session.add(New_Customer)
        db.session.commit()
        return render_template('login.html',error=0)
    else:
        return render_template('Customer_register.html',error=1)

@app.route('/Customer/Home/<int:ID>', methods=["GET"])
def C_home(ID):
    All_Services = db.session.query(Service.Service_name).distinct().all()
    service_histor_requested=db.session.query(
        Service.Service_name,
        Service_request.Service_status
    ).join(Service, Service_request.Service_id==Service.Service_id
    ).filter(Service_request.Customer_id == ID
    ).filter(Service_request.Service_status=="Requested").all()
    service_history_accepted = db.session.query(
        Service_request.Id,
        Service.Service_name,
        Professional.Full_name,
        Professional.Phone_number,
        Service_request.Service_status,
        Service_request.date_of_completion
    ).join(Professional, Service_request.Professional_id == Professional.Id
    ).join(Service, Service_request.Service_id==Service.Service_id
    ).filter(Service_request.Customer_id == ID).all()
    return render_template('Customer_home.html',ID=ID,services=All_Services,Service_history_1=service_histor_requested,Service_history_2=service_history_accepted)

@app.route('/Customer/<int:ID>')
def C_details(ID):
    cust=Customer.query.filter_by(Id=ID).first()
    return render_template("Customer_details.html",ID=ID,cust=cust)

@app.route('/Customer/Edit/<int:ID>', methods=["GET","POST"])
def C_edit_details(ID):
    cust=Customer.query.filter_by(Id=ID).first()
    if request.method=="GET":
        return render_template("Customer_edit_details.html",ID=ID,cust=cust)
    cust_new_data = request.form
    cust.Full_name = cust_new_data['full_name']
    cust.Password = cust_new_data['password']
    cust.Email = cust_new_data['email']
    cust.Phone_number = cust_new_data['phone_number']
    cust.Address = cust_new_data['address']
    cust.Pincode = cust_new_data['pincode']
    db.session.commit()
    return redirect(f'/Customer/{ID}')

@app.route('/Customer/Service/<int:ID>/<string:service_name>', methods=["GET"])
def C_Service(ID,service_name):
    all_services=Service.query.filter_by(Service_name=service_name).all()
    return render_template('Customer_Service.html',ID=ID,all_services=all_services,name=service_name)

@app.route('/Customer/<int:C_id>/Book/<int:service_id>')
def book(C_id,service_id):
    New_service_request=Service_request(Service_id=service_id,Customer_id=C_id,date_of_request=today,Service_status='Requested')
    db.session.add(New_service_request)
    db.session.commit()
    return redirect(f'/Customer/Home/{C_id}')

@app.route('/Customer/Home/<int:Id>/Close/<int:service_req_id>', methods=["GET","POST"])
def Closing(Id,service_req_id):
    service_request=Service_request.query.filter_by(Id=service_req_id).first()
    if request.method=="GET":
        ALL_data=db.session.query(
            Service_request.Id,
            Service.Service_name,
            Service.Description,
            Professional.Id,
            Professional.Full_name,
            Professional.Phone_number
        ).join(Service,Service_request.Service_id==Service.Service_id
        ).join(Professional,Service_request.Professional_id==Professional.Id
        ).filter(Service_request.Id==service_req_id).first()
        return render_template('Customer_req_close.html',ID=Id,a=service_req_id,abc=ALL_data,date=str(today))
    remarks=request.form.get('remarks')
    service_request.Remarks=remarks
    service_request.Service_status="Closed"
    service_request.date_of_completion=today
    db.session.commit()
    return redirect(f'/Customer/Home/{Id}')

@app.route('/Customer/<int:ID>/Search', methods=["GET","POST"])
def C_Search_(ID):
    data=None
    Services=['Service_name','Price','Time_required','Description']
    if request.method=="GET":
        return render_template('Customer_Search.html',ID=ID,services=Services)
    All_data=request.form
    field=All_data['servicename']
    value=All_data['search_element']
    if field=='Service_name':
        data = [i for i in Service.query.all() if value.lower() in i.Service_name.lower()]
        Service.query.filter(Service.Service_name.ilike(value)).all()
    elif field=='Price':
        data=Service.query.filter(Service.Price<=value).all()
    elif field=='Time_required':
        data=Service.query.filter(Service.Time_required<=value).all()
    elif field=='Description':
        data=[i for i in Service.query.all() if value.lower() in i.Description.lower()]
    if data==None or data==[]:
        return render_template('Customer_Search.html',ID=ID,services=Services,res=2)
    return render_template('Customer_Search.html',ID=ID,services=Services,res=1,req_data=data)

@app.route('/Customer/<int:ID>/Summary', methods=["GET"])
def C_Summary(ID):
    all_status=[i.Service_status for i in Service_request.query.filter_by(Customer_id=ID)]
    all_defualt_status=['Closed', 'Requested','Assigned']
    frequency = {i: 0 for i in all_defualt_status}
    for i in all_status:
        frequency[i]+=1
    x=list(frequency.keys())
    y=list(frequency.values())
    plt.figure()
    plt.bar(x,y)
    plt.title("Service Status")
    plt.savefig('static/Images/C_Summary_1.jpg')
    plt.close()
    return render_template('Customer_Summary.html',ID=ID)


@app.route('/Professional/Register', methods=["GET", "POST"])
def create_professional():
    All_services=db.session.query(Service.Service_name).distinct().all()
    if request.method=="GET":
        return render_template('Professional_register.html',services=All_services)
    Professional_data=request.form
    New_Professional=Professional(Full_name=Professional_data['fullname'],Email=Professional_data['email'],Password=Professional_data['password'], Address=Professional_data['address'],Pincode=Professional_data['pin'],Experience=Professional_data['experience'], Service_name=Professional_data['servicename'],Phone_number=Professional_data['phone_number'])
    ALL_professional=[i.Email for i in Professional.query.all()]
    if New_Professional.Email not in ALL_professional:
        db.session.add(New_Professional)
        db.session.commit()
        return render_template('login.html',error=0)
    return render_template('Professional_register.html',services=All_services,error=1)



@app.route('/Professional/Home/<int:ID>', methods=["GET"])
def P_home(ID):
    P_Service_name=Professional.query.filter_by(Id=ID).first().Service_name
    Service_id_with_given_service=[i.Service_id for i in Service.query.all() if i.Service_name==P_Service_name]
    
    rejected_request_ids = [req.service_req_id for req in Rejected_req.query.filter_by(professional_id=ID).all()]
    
    All_today_services_with_P_service_name = db.session.query(
        Service_request.Id,
        Customer.Full_name,
        Customer.Phone_number,
        Customer.Address,
        Customer.Pincode
    ).join(Service_request, Service_request.Customer_id == Customer.Id
    ).filter(
        Service_request.date_of_request == str(today),
        Service_request.Service_id.in_(Service_id_with_given_service),
        Service_request.Professional_id==None,
        ~Service_request.Id.in_(rejected_request_ids)
        ).all()


    closed_services = db.session.query(
        Service_request.Id,
        Customer.Full_name,
        Customer.Phone_number,
        Customer.Address,
        Customer.Pincode,
        Service_request.date_of_completion,
        Service_request.Remarks
    ).join(Customer, Service_request.Customer_id == Customer.Id
    ).filter(Service_request.Professional_id == ID, 
             Service_request.Service_status=="Closed").all()

    return render_template('Professional_home.html',ID=ID,Today_services=All_today_services_with_P_service_name,Closed_services=closed_services)

@app.route('/Professional/<int:ID>')
def P_details(ID):
    prof=Professional.query.filter_by(Id=ID).first()
    return render_template("Professional_details.html",ID=ID,prof=prof)

@app.route('/Professional/Edit/<int:ID>', methods=["GET","POST"])
def P_edit_details(ID):
    prof=Professional.query.filter_by(Id=ID).first()
    if request.method=="GET":
        return render_template("Professional_edit_details.html",ID=ID,prof=prof)
    prof_new_data = request.form
    prof.Full_name = prof_new_data['full_name']
    prof.Password = prof_new_data['password']
    prof.Email = prof_new_data['email']
    prof.Phone_number = prof_new_data['phone_number']
    prof.Service_name = prof_new_data['service_name']
    prof.Address = prof_new_data['address']
    prof.Pincode = prof_new_data['pincode']
    prof.Experience = prof_new_data['experience']
    db.session.commit()
    return redirect(f'/Professional/{ID}')

@app.route('/Professional/Home/<int:ID>/Booked/<int:service_req_id>', methods=["GET"])   
def booked(ID,service_req_id):
    Service_req=Service_request.query.filter_by(Id=service_req_id).first()
    Service_req.Professional_id=ID
    Service_req.Service_status='Assigned'
    db.session.commit()
    return redirect(f'/Professional/Home/{ID}')

@app.route('/Professional//Home/<int:ID>/Rejected/<int:service_req_id>', methods=["GET"])   
def rejected(ID,service_req_id):
    New_Rejected=Rejected_req(service_req_id=service_req_id,professional_id=ID)
    db.session.add(New_Rejected)
    db.session.commit()
    return redirect(f'/Professional/Home/{ID}')

@app.route('/Professional/<int:ID>/Search', methods=["GET","POST"])
def P_Search(ID):
    data=None
    Services=['Customer_name','Customer_number','Pincode','Location','Date_of_request','Date_of_completion','Price']
    if request.method=="GET":
        return render_template('Professional_Search.html',ID=ID,services=Services)
    All_data=request.form
    field=All_data['servicename']
    value=All_data['search_element']
    query = db.session.query(
        Customer.Full_name.label('Customer_name'),
        Customer.Phone_number.label('Customer_number'),
        Customer.Pincode.label('Pincode'),
        Customer.Address.label('Location'),
        Service_request.date_of_request.label('Date_of_request'),
        Service_request.date_of_completion.label('Date_of_completion'),
        Service.Price.label('Price')
        ).join(Service_request, Customer.Id == Service_request.Customer_id
        ).join(Service, Service_request.Service_id == Service.Service_id
        ).join(Professional, Service_request.Professional_id==Professional.Id
        ).filter(Service_request.Professional_id==ID)
    if field=='Customer_name':
        data = [i for i in query.all() if value.lower() in i.Customer_name.lower()]
    elif field=='Customer_number':
        data = [i for i in query.all() if int(value)==i.Customer_number]
    elif field=='Pincode':
        data = [i for i in query.all() if int(value)==i.Pincode]
    elif field=='Location':
        data=[i for i in query.all() if value.lower() in i.Location.lower()]
    elif field=='Price':
        data = [i for i in query.all() if int(value)==i.Price]
    elif field=='Date_of_request':
        data = [i for i in query.all() if value==i.Date_of_request.strftime("%Y-%m-%d")]
    elif field=='Date_of_completion':
        data = [i for i in query.all() if value==i.Date_of_completion.strftime("%Y-%m-%d")]
    if data==None or data==[]:
        return render_template('Professional_Search.html',ID=ID,services=Services,res=2)
    return render_template('Professional_Search.html',ID=ID,services=Services,res=1,req_data=data)

@app.route('/Professional/<int:ID>/Summary', methods=["GET"])
def P_Summary(ID):
    all_ratings=[int(i.Remarks) for i in Service_request.query.filter_by(Professional_id=ID) if i.Service_status=="Closed"]
    frequency = {i: 0 for i in range(1, 6)}
    for i in all_ratings:
        frequency[i]+=1
    x=list(frequency.keys())
    y=list(frequency.values())
    plt.figure()
    plt.bar(x,y)
    plt.xlabel('Ratings')
    plt.ylabel('No. of Customers')
    plt.ylim(0, max(y) + 1) 
    plt.title("Ratings Review")
    plt.savefig('static/Images/P_Summary_1.jpg')
    plt.close()

    Total_req_id=[i.Customer_id for i in Service_request.query.filter_by(Professional_id=ID).all()]
    Total_req_name=[]
    for i in Total_req_id:
        Total_req_name.append(Customer.query.filter_by(Id=i).first().Full_name)
    frequency1 = {i: 0 for i in Total_req_name}
    for i in Total_req_name:
        frequency1[i]+=1

    labels=list(frequency1.keys())
    y=list(frequency1.values())
    x=[i*100/sum(y) for i in y]
    plt.figure()
    plt.pie(x,labels=labels , autopct='%1.1f%%')
    plt.title("Customer Distribution")
    plt.savefig('static/Images/P_Summary_2.jpg')
    plt.close()
    return render_template('Professional_Summary.html',ID=ID)