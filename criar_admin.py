from models import session, Usuario
import streamlit_authenticator as stauth

# Generate the hashed password
senha_criptografada = stauth.Hasher(["05agosto13"]).generate()

# Extract the hashed password from the list
hashed_password = senha_criptografada[0]

# Create a new user with the hashed password
usuario = Usuario(nome="Luiz", senha=hashed_password, email="luizjunao@yahoo.com.br", admin=True)

# Add the user to the session and commit
session.add(usuario)
session.commit()