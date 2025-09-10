---
title: NoSQL - Firebase Demo
transition: fade
---

# Firebase Demo

---

# Generate key

[https://firebase.google.com/docs/admin/setup#windows](https://firebase.google.com/docs/admin/setup#windows)

<div class="w-[600px]">

![Initialize the SDK in non Google ENV](/images/nosql-demo/chrome_IfCXfWMn9d.png)
</div>

---

# Export environment variable

- Windows (Powershell)

```powershell
# run.ps1
$env:GOOGLE_APPLICATION_CREDENTIALS="D:\Backup\nodejs\astro-starlight\cos3103\public\python\current\testfirestore-5fd1d-firebase-adminsdk-fbsvc-5102bef894.json"
python firestore.py
```

```python
import firebase_admin
from firebase_admin import firestore

# Application Default credentials are automatically created.
app = firebase_admin.initialize_app()
db = firestore.client()
```