from pymongo import MongoClient

class Database:
    def __init__(self, url, name):
        self.client = MongoClient(url)
        self.db = self.client.get_database(name)
        self.records = self.db.user_records
        self.emails = self.db.paypal_accounts
    
    def new_user(self, user):
        self.records.insert_one(user.__dict__)
        print(f"successfully inserted new user {user.phone}")
    
    def get_user(self, phone):
        return self.records.find_one({"phone": phone})

    def update_balance(self, phone, amt):
        self.records.update_one({"phone": phone}, {'$inc': {"balance": amt}})

    def get_balance(self, phone):
        return int(self.get_user(phone)['balance'])

    def update_user(self, filter, update_value):
        self.records.update_one(filter, {'$set': update_value})

    def find_unused_email(self):
        return self.emails.find_one({"is_used": False})

    def mark_email_as_used(self, email):
        self.emails.update_one({"email": email}, {'$set': {"is_used" : True}})

    def lookup_paypalauth(self, phone):
        email = self.get_user(phone)['paypal_email']
        return self.emails.find_one({"email": email})['paypal_auth']
        

class User:
    def __init__(self, email, phone, balance=0):
        self.name = "placeholder_name"
        self.phone = phone
        self.paypal_email = email
        self.voice_identity = ""
        self.onboarding_status = 0
        self.balance = balance

db = Database('LINK', 'database1')