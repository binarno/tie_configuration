import streamlit as st
import urllib.parse

from streamlit.components.v1 import html


def configure_jeanie(auth_user: str, auth_password: str, sip_address: str):

    parameters = {'authUser': auth_user, 'authPassword': auth_password, 'account': sip_address}
    open_script= """
        <script type="text/javascript">
            window.open('%s');
        </script>
    """ % ('tiephoneconfig:\\open=?' + urllib.parse.urlencode(parameters))

    html(open_script)


st.title('Jeannie Softphone Configuration')


with st.form("configure_form"):
    auth_user_field = st.text_input('Auth user', placeholder='123456789')
    auth_password_field = st.text_input('Password', type='password')
    sip_address_field = st.text_input('SIP user address', placeholder='user@domain.com')
    st.form_submit_button('Configure Jeanie', on_click=configure_jeanie, args=(auth_user_field, auth_password_field, sip_address_field))
