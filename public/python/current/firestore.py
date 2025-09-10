import firebase_admin
from firebase_admin import firestore

# Application Default credentials are automatically created.
app = firebase_admin.initialize_app()
db = firestore.client()

# Add a document with auto-generated ID
doc_ref = db.collection('users').add({
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': 30
})
print(f"Document ID: {doc_ref[1].id}")

# Add document with specific ID
db.collection('users').document('user123').set({
    'name': 'Jane Smith',
    'email': 'jane@example.com'
})