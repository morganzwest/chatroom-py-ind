import firebase_admin


class Db(object):
    def __init__(self, url: str, key_path: str):
        from firebase_admin import credentials
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred, {
            "databaseURL": url
        })

    @staticmethod
    def check_password(hashed_password: str, user_password: str):
        import hashlib
        # splits the salt so the decrypt can find the original
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

    @staticmethod
    def hash_password(password: str):
        import hashlib, uuid
        salt = uuid.uuid4().hex  # hex:bin represent
        # encode it to hashed hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

    @staticmethod
    def save(ref: str, dict_output):
        from firebase_admin import db
        _t = db.reference(ref).push(dict_output)

    @staticmethod
    def load(path="/"):
        from firebase_admin import db
        return db.reference(path)

    @staticmethod
    def update(path: str, dict_update):
        from firebase_admin import db
        ref = db.reference(path)
        ref.update(dict_update)
