from fastapi import FastAPI, Path, HTTPException, Query 
import json

app=FastAPI()

def load_data(): 
    with open("patients.json",'r') as f:
        data=json.load(f)

    return data


@app.get("/")
def hello():
    return {"message":"Hello, Patient Management System!"}


@app.get("/about")
def about():
    return {"message":"This is a Patient Management System API built with FastAPI."}

@app.get("/view")
def view():
    data=load_data()
    return data



@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description = "ID of the patient to retrieve", example="P001")):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404, detail="Patient not found")



@app.get("/sort")
def sort_patients(sort_by : str = Query(..., description=" Sort on the basis of height, weight, or bmi"), order : str = Query("asc", description="Sort in ascending or descending order")):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields :
        raise HTTPException (status_code = 400, detail = f"Invalid field Select from {valid_fields}")
    
    valid_orders=['asc','desc']

    if order not in valid_orders:
        raise HTTPException (status_code=400, detail= f'Invalid Orders select from {valid_orders}')
    
    data= load_data()
    sort_order= True if order == 'desc' else False

    sorted_data = sorted ( data.values(), key= lambda x : x.get(sort_by, 0), reverse=sort_order)

    return sorted_data
