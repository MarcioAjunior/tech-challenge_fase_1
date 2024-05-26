import streamlit as st
import requests

st.title('/register')

username = st.text_input('Username')
email = st.text_input('Email')
password = st.text_input('Password', type='password')

if st.button('Register'):
    if username and email and password:
        user_data = {
            "username": username,
            "email": email,
            "password": password
        }
        response = requests.post('http://localhost:8000/register', json=user_data)
        if response.status_code == 201:
            st.success('Usuario cadastrado com sucesso !')
        else:
            st.error(response.json().get('detail', 'Cadastro falhou'))
    else:
        st.error('Preencha todos os campos')
