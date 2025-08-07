import streamlit as st
import urllib.parse
import Crypto.Signature
import Crypto.PublicKey.RSA
import Crypto.Signature.pkcs1_15
import Crypto.Hash.SHA256
import base64
import os

if 'configuring' not in st.session_state:
    st.session_state.configuring = False

if 'error' not in st.session_state:
    st.session_state.error = ''


def change_state():
    st.session_state.auth_user = auth_user_field
    st.session_state.auth_password = auth_password_field
    st.session_state.sip_address = sip_address_field
    st.session_state.audio_recording_folder = audio_recording_folder_field

    valid = (st.session_state.auth_user != '' and
             st.session_state.auth_password != ''
             and st.session_state.sip_address.find('@') > 0)

    if valid:
        st.session_state.configuring = True
        st.session_state.error = ''
    else:
        st.session_state.configuring = False
        st.session_state.error = '### One or more entries are not correct'


if not st.session_state.configuring:
    st.title('Jeannie Softphone Configuration')
    auth_user_field = st.text_input('Auth user', placeholder='123456789')
    auth_password_field = st.text_input('Password', type='password')
    sip_address_field = st.text_input('SIP user address', placeholder='user@domain.com')
    audio_recording_folder_field = st.text_input('Audio recording folder', placeholder='c:\\somefolder')

    if st.session_state.error != '':
        st.markdown(st.session_state.error)

    st.button('Configure Jeanie', on_click=change_state)

else:
    st.title('Almost there!')
    st.markdown("""
    Click the button below to finish configuring your Jeanie app.
    
    Before you click:
    
    - Make sure you installed Jeanie
    - After you click the button, allow your browser to launch Jeanie
    """)

    parameters = {'authUser': st.session_state.auth_user, 'authPassword': st.session_state.auth_password, 'account': st.session_state.sip_address, 'recordingFolder': st.session_state.audio_recording_folder}
    encoded_parameters = urllib.parse.urlencode(parameters)

    url = 'tiephoneconfig://open/?' + encoded_parameters

    encoded_url_for_signature = url.encode('UTF-8')

    hash = Crypto.Hash.SHA256.SHA256Hash(encoded_url_for_signature)
    hash16 = hash.hexdigest()

    with open("configuration.key") as signature_file:
        signarure_key_content = signature_file.read()
    password = os.getenv("SIGNATURE_PASSWORD")
    key = Crypto.PublicKey.RSA.import_key(signarure_key_content, password)
    signature_object = Crypto.Signature.pkcs1_15.new(key)
    signature = signature_object.sign(hash)
    signature_base64 = base64.b64encode(signature).decode('UTF-8')

    url = url + "&signature=" + signature_base64
    st.link_button('Almost there! Click here to configure Jeanie', url)
    st.markdown(f"""
    Configuration URL: [{url}]({url})
    """)



