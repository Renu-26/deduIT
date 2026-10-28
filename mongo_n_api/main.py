from fastapi import FastAPI, HTTPException
from pymongo import MongoClient, ReturnDocument
from pydantic import BaseModel
from typing import Optional

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "hospital"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

app = FastAPI()


# What the client sends when creating a patient (no id: the server makes it)
class PatientIn(BaseModel):
    name: str
    age: int
    gender: Optional[str] = None
    city: Optional[str] = None
    blood_group: Optional[str] = None

# For PATCH: every field is optional, send only what you want to change
class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    city: Optional[str] = None
    blood_group: Optional[str] = None


# Gives the next number: 9, 10, 11, ...
def next_patient_id():
    counter = db["counters"].find_one_and_update(
        {"_id": "patients"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return str(counter["seq"])

def find_patient(patient_id: str):
    query_values = [patient_id]
    if patient_id.isdigit():
        query_values.append(int(patient_id))
    return db["patients"].find_one({"_id": {"$in": query_values}})


# Prints the database and lists its collections
@app.get("/")
def list_collections():
    return {"database": DB_NAME, "collections": db.list_collection_names()}


# List all patients (shows _id as "id")
@app.get("/patients")
def get_patients():
    patients = []
    for doc in db["patients"].find():
        doc["id"] = str(doc.pop("_id"))
        patients.append(doc)
    return {"collection": "patients", "total": len(patients), "data": patients}


# Get one patient by id
@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    # try the id as text, and also as a number if it looks like one
    query_values = [patient_id]
    if patient_id.isdigit():
        query_values.append(int(patient_id))

    doc = db["patients"].find_one({"_id": {"$in": query_values}})
    if doc is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    doc["id"] = str(doc.pop("_id"))
    return doc


# Any collection
@app.get("/data/{collection_name}")
def get_collection(collection_name: str):
    docs = []
    for doc in db[collection_name].find():
        doc["_id"] = str(doc["_id"])
        docs.append(doc)
    return {"collection": collection_name, "total": len(docs), "data": docs}


# Create a patient with an auto-incremented id
@app.post("/patients", status_code=201)
def create_patient(patient: PatientIn):
    data = patient.model_dump()
    data["_id"] = next_patient_id()      # "9", "10", ...
    db["patients"].insert_one(data)
    data["id"] = data.pop("_id")         # show it as id
    return data


@app.put("/patients/{patient_id}")
def replace_patient(patient_id: str, patient: PatientIn):
    existing = find_patient(patient_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    new_data = patient.model_dump(exclude_none=True)
    db["patients"].replace_one({"_id": existing["_id"]}, new_data)

    return {"id": str(existing["_id"]), **new_data}


@app.patch("/patients/{patient_id}")
def update_patient(patient_id: str, changes: PatientUpdate):
    existing = find_patient(patient_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    updates = changes.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    db["patients"].update_one({"_id": existing["_id"]}, {"$set": updates})

    doc = db["patients"].find_one({"_id": existing["_id"]})
    return {"id": str(doc.pop("_id")), **doc}


@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    existing = find_patient(patient_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    db["patients"].delete_one({"_id": existing["_id"]})
    return {"message": f"Patient {patient_id} deleted", "name": existing.get("name")}