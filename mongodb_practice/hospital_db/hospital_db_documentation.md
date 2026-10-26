**Lists the databases that contain stored data.**
show dbs

**Creates a new database.**
`use hospital`

**Creates a new collection.**
`db.createCollection("patients")`
`db.createCollection("doctors")`
`db.createCollection("departments")`
`db.createCollection("appointments")`

** Inserts multiple patients documents into patients collection.**

db.patients.insertMany([
  { _id: 1, name: "Anu", age: 28, city: "Chennai", blood_group: "O+" },
  { _id: 2, name: "Ravi", age: 45, city: "Bangalore", blood_group: "B+" },
  { _id: 3, name: "Priya", age: 35, city: "Chennai", blood_group: "A+" },
  { _id: 4, name: "Karthik", age: 52, city: "Coimbatore", blood_group: "O-" },
  { _id: 5, name: "Meena", age: 19, city: "Madurai", blood_group: "AB+" },
  { _id: 6, name: "Arun", age: 61, city: "Bangalore", blood_group: "B-" },
  { _id: 7, name: "Divya", age: 42, city: "Chennai", blood_group: "A-" },
  { _id: 8, name: "Vijay", age: 33, city: "Coimbatore", blood_group: "O+" }
])

**Inserts multiple doctors documents into doctors collection.**

db.doctors.insertMany([
  { _id: 101, name: "Dr. Kumar", specialization: "Cardiology", experience: 12 },
  { _id: 102, name: "Dr. Priya", specialization: "Neurology", experience: 8 },
  { _id: 103, name: "Dr. Arun", specialization: "Orthopedics", experience: 15 },
  { _id: 104, name: "Dr. Meena", specialization: "Dermatology", experience: 6 },
  { _id: 105, name: "Dr. Ravi", specialization: "General Medicine", experience: 10 }
])

**Inserts multiple documents into appointments collection.**

db.appointments.insertMany([
  { _id: 201, patient_id: 1, doctor_id: 101, date: ISODate("2026-10-20"), status: "completed" },
  { _id: 202, patient_id: 2, doctor_id: 105, date: ISODate("2026-10-21"), status: "completed" },
  { _id: 203, patient_id: 3, doctor_id: 102, date: ISODate("2026-10-22"), status: "scheduled" },
  { _id: 204, patient_id: 4, doctor_id: 103, date: ISODate("2026-10-22"), status: "completed" },
  { _id: 205, patient_id: 5, doctor_id: 104, date: ISODate("2026-10-23"), status: "scheduled" },
  { _id: 206, patient_id: 6, doctor_id: 101, date: ISODate("2026-10-23"), status: "cancelled" },
  { _id: 207, patient_id: 7, doctor_id: 105, date: ISODate("2026-10-24"), status: "scheduled" },
  { _id: 208, patient_id: 8, doctor_id: 103, date: ISODate("2026-10-24"), status: "completed" },
  { _id: 209, patient_id: 1, doctor_id: 105, date: ISODate("2026-10-25"), status: "scheduled" },
  { _id: 210, patient_id: 3, doctor_id: 101, date: ISODate("2026-10-25"), status: "scheduled" }
])

**Inserts multiple documents into departments collection.**

db.departments.insertMany([
  { _id: 301, name: "Cardiology", floor: 2, beds: 20 },
  { _id: 302, name: "Neurology", floor: 3, beds: 15 },
  { _id: 303, name: "Orthopedics", floor: 1, beds: 25 },
  { _id: 304, name: "Dermatology", floor: 1, beds: 10 },
  { _id: 305, name: "General Medicine", floor: 0, beds: 30 }
])

**Inserts multiple documents into bills collection.**

db.bills.insertMany([
  { _id: 401, patient_id: 1, appointment_id: 201, amount: 2500, payment_status: "paid" },
  { _id: 402, patient_id: 2, appointment_id: 202, amount: 1200, payment_status: "paid" },
  { _id: 403, patient_id: 3, appointment_id: 203, amount: 1800, payment_status: "pending" },
  { _id: 404, patient_id: 4, appointment_id: 204, amount: 3500, payment_status: "paid" },
  { _id: 405, patient_id: 5, appointment_id: 205, amount: 800, payment_status: "pending" },
  { _id: 406, patient_id: 6, appointment_id: 206, amount: 2200, payment_status: "cancelled" },
  { _id: 407, patient_id: 7, appointment_id: 207, amount: 1000, payment_status: "pending" },
  { _id: 408, patient_id: 8, appointment_id: 208, amount: 3000, payment_status: "paid" }
])


**Display all patients.**
db.patients.find()

**Find patients who live in Chennai.**
db.patients.find({city: 'Chennai'})

**Find patients older than 40.**
db.patients.find({age: {$gt: 40}})

**Find all doctors with more than 8 years of experience.**
db.doctors.find({experience: {$gt: 8}})

**Find appointments with status scheduled.**
db.appointments.find({status: 'scheduled'})

**Sort patients from oldest to youngest.**
db.patients.find().sort({age:1})

**Update Meena's age to 20.**
db.patients.updateOne({_id:5}, {$set: {age: 20}})

**Find bills with amounts greater than or equal to ₹2,000.**
db.bills.find({amount: {$gte: 2000}})

**Display each appointment with the patient's name.**

db.appointments.aggregate([
  {
    $lookup: {
      from: "patients",
      localField: "patient_id",
      foreignField: "_id",
      as: "patient_details"
    }
  }
])

**Display each appointment with the doctor's name and specialization.**

db.appointments.aggregate([{
| $lookup:{
| from: "doctors",
| localField: "doctor_id",
| foreignField: "_id",
| as: "doctors_details"
| }}])


**Display patient name, doctor name, appointment status, and date together.**

db.appointments.aggregate([
  {
    $lookup: {
      from: "patients",
      localField: "patient_id",
      foreignField: "_id",
      as: "patient_details"
    }
  },
  {
	$lookup: {
	from: "doctors",
	localField: "doctor_id",
	foreignField: "_id",
	as: "doctor_details"	
  }}
])