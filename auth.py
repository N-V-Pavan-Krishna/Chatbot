# auth.py (final fixed version for streamlit-authenticator >= 0.3.0)
import streamlit_authenticator as stauth
import streamlit as st

# Pre-hashed passwords
users = {
    "pavan": {
        "name": "Pavan Krishna",
        "password": "$2b$12$QZVn/vrHOu07U2sf/G1SmOm5mR/5DF9s/kePDn42AzsmJYulNVCWq",
        "role": "user"
    },
    "admin": {
        "name": "Admin",
        "password": "$2b$12$dk4txZSx5KH6N4yT0p7psuiHpCwPyrminFo4W6pRGZX0eUEOig7hO",
        "role": "admin"
    },
}

def login():
    credentials = {
        "usernames": {
            uname: {
                "name": udata["name"],
                "password": udata["password"]
            } for uname, udata in users.items()
        }
    }

    authenticator = stauth.Authenticate(credentials, "chatbot_app", "abcdef", cookie_expiry_days=1)
    authenticator.login(location="sidebar")

    name = st.session_state.get("name")
    auth_status = st.session_state.get("authentication_status")
    username = st.session_state.get("username")
    role = users.get(username, {}).get("role", "user")
    return authenticator, name, auth_status, username, role

def is_authenticated():
    return "user" in st.session_state
