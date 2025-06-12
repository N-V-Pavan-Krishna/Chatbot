from streamlit_authenticator.utilities.hasher import Hasher

passwords = ["1234", "adminpass"]
hashed_passwords = [Hasher().hash(pw) for pw in passwords]
print(hashed_passwords)
