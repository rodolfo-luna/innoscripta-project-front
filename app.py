import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import base64
import requests
import json
from PIL import Image

def main():
    hide_menu()
    hide_forehead()
    set_sidebar_background()
    set_background()
    authenticator.logout('Logout', 'main')
    set_page_title("Innoscripta Global Data Competition")
    company_data = None
    with st.form('Main form'):
        with st.sidebar:
            st.sidebar.markdown(format_body_text("Type the company name:"),unsafe_allow_html=True)
            company_name = st.sidebar.text_input("", key="company")   
            st.sidebar.markdown(format_body_text("Type the country:"),unsafe_allow_html=True)
            country = st.sidebar.text_input("", key="country")
            st.sidebar.markdown(format_body_text("Type the website (Optional):"),unsafe_allow_html=True)
            website = st.sidebar.text_input("", key="website")

        
            submitted = st.form_submit_button('Submit')
            if submitted:
                if company_name !='' and country != '':
                    with st.spinner('Please wait.'):
                        company_data = get_data_from_api(company_name, country, website)
                else:
                    st.error('Company name and country is mandatory.')
    if company_data is not None:
            output_list = ['Company name: {}'.format(company_data['Company Name']),
                          'Country: {}'.format(company_data['Country']),
                          'Website: {}'.format(company_data['Website']),
                          'Products or Services: {}'.format(company_data['Products/Services']),
                          'Keywords: {}'.format(company_data['keywords']),
                          'Other info: {}'.format(company_data['Other Info']),
                          'NAICS: {}'.format(company_data['NAICS']),
                          'SIC: {}'.format(company_data['SIC'])
                          ]
            output = "\n".join(output_list)
            st.text_area(label="Results:", value=output, height=220)

            if len(company_data['Products/Services Images']) > 0:
                st.markdown(format_body_text("Company products/services images: "),unsafe_allow_html=True)
                st.image(company_data['Products/Services Images'][0])  
                st.image(company_data['Products/Services Images'][1])    

def set_page_title(title):
    '''
    Set the title of the page with font and font-size formatted.
    '''
    st.markdown(f'<p style="font-family:Roboto, sans-serif;color:#FFFFFF;;font-size:38px;border-radius:2%;">{title}</p>', 
                unsafe_allow_html=True)
    
def format_body_text(text):
    '''
    Format the text inside the body of the page.
    '''

    formatted_text = f'<p style="font-family:Roboto, sans-serif;color:#FFFFFF;font-size:20px;border-radius:2%;">{text}</p>'
    return formatted_text

def set_background():
    '''
    Set background color and color gradient of the page.
    '''
    st.markdown("""
                <style>
                    .stApp {
                    background: #2596be; 
                    background: -webkit-linear-gradient(to right, #2596be, #50a49c); 
                    background: linear-gradient(to right, #2596be, #50a49c); 
                    }
                </style>""", 
                unsafe_allow_html=True)
    
def set_sidebar_background():
    '''
    Set background color and color gradient in sidebar of the page.
    '''
    st.markdown("""
                <style>
                    [data-testid=stSidebar] {
                    background: -webkit-linear-gradient(to right, #2596be, #50a49c);
                    background: linear-gradient(to right, #2596be, #50a49c);
                    }
                </style>
                """,
                unsafe_allow_html=True,
        )
    
def get_data_from_api(company_name, country, website):
    '''
    request companies data from the api.
    '''
    base_url = 'https://companiesdata.sytes.net/company'
    headers = {"Authorization": "Bearer InnoREK2I8vlUtMHqBE6ko916ZvdHqdMT5rT2x"}
    url_complement = ("?company_name={}&country={}&website={}".format(company_name, country, website))
    full_url = base_url + url_complement
    response = requests.get(full_url, headers=headers)

    return json.loads(response.content)

def hide_forehead():
    '''
    Hide header of the page.
    '''
    hide_streamlit_style = """
        <style>
            #MainMenu, header, footer {visibility: hidden;}
        </style>"""
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def hide_menu():
    '''
    Hide Streamlit top-right menu.
    '''
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

# Open the yaml file with allowed users.
with open('users.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Create the authenticator object with users credentials.
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Execute the authentication process.
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    main()
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
    