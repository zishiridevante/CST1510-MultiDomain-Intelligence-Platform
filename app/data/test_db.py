from database import DatabaseManager


db = DatabaseManager()

print("\n=== TEST 1: READ COUNTS FROM DATABASE ===")
print("Cyber incidents:", len(db.get_all_cyber_incidents()))
print("IT tickets:", len(db.get_all_it_tickets()))


print("\n=== TEST 2: CREATE + READ CYBER INCIDENT ===")
new_incident = {
    "incident_id": 9999,
    "timestamp": "2024-12-13 12:00:00",
    "severity": "High",
    "category": "Phishing",
    "status": "Open",
    "description": "Test incident created during CRUD testing"
}

db.create_cyber_incident(new_incident)
print("Created:", db.get_cyber_incident_by_id(9999))


print("\n=== TEST 3: UPDATE CYBER INCIDENT STATUS ===")
db.update_cyber_incident_status(9999, "Resolved")
print("Updated:", db.get_cyber_incident_by_id(9999))


print("\n=== TEST 4: DELETE CYBER INCIDENT ===")
db.delete_cyber_incident(9999)
print("After delete:", db.get_cyber_incident_by_id(9999))


print("\n=== TEST 5: CREATE + READ IT TICKET ===")
new_ticket = {
    "ticket_id": 8888,
    "priority": "Medium",
    "description": "Test ticket for CRUD",
    "status": "Open",
    "assigned_to": "IT_Support_X",
    "created_at": "2024-12-13 13:00:00",
    "resolution_time_hours": 10
}

db.create_it_ticket(new_ticket)
print("Created:", db.get_it_ticket_by_id(8888))


print("\n=== TEST 6: UPDATE IT TICKET ===")
db.update_it_ticket_status(8888, "Closed")
db.reassign_it_ticket(8888, "IT_Support_Y")
print("Updated:", db.get_it_ticket_by_id(8888))


print("\n=== TEST 7: DELETE IT TICKET ===")
db.delete_it_ticket(8888)
print("After delete:", db.get_it_ticket_by_id(8888))

print("\n=== ALL CRUD TESTS COMPLETED ===")
