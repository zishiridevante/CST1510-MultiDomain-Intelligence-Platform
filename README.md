# Week 7: Secure Authentication System
**Student Name:** Devante Zishiri  
**Student ID:** M01040790  
**Course:** CST1510 – Multi-Domain Intelligence Platform  

## Overview  
This week implements a command-line authentication system using secure password hashing.  
The goal is to demonstrate understanding of security fundamentals before moving on to database integration and full web application development in later weeks.

## Features  
- Secure password hashing using bcrypt with automatic salt generation  
- User registration with validation  
- Duplicate username prevention  
- Login system using bcrypt verification  
- File-based storage (`users.txt`)  
- Simple menu-driven interface  
- Clear success/error messages  

## Technical Details  
- **Hashing Algorithm:** bcrypt (salted hashes)
- **Storage:** Plain-text file using CSV-style entries (`username,hashed_password`)
- **Validation Rules:**  
  - Username: 3–20 characters, alphanumeric  
  - Password: minimum 6 characters  

## Files  
- `auth.py` – main program  
- `users.txt` – user data store  

## How to Run

```bash
python3 auth.py


## Requirements  
bcrypt==4.2.0


