import json
import streamlit as st
import pandas as pd 
from mitosheet.streamlit.v1 import spreadsheet, RunnableAnalysis
import os
from custom_functions import CHECK
from file_utils import save_analysis, get_all_provider_names_from_automations, get_runnable_analysis_and_description_from_provider_name

# Set the streamlit page to wide so you can see the whole spreadsheet
st.set_page_config(layout="wide")

if not os.path.exists(os.path.join(os.getcwd(), 'automations')):
    os.mkdir(os.path.join(os.getcwd(), 'automations'))

if not os.path.exists(os.path.join(os.getcwd(), 'data')):
    os.mkdir(os.path.join(os.getcwd(), 'data'))


st.title("Book of Business Checker")
st.markdown("""Need to check a new book of business against our salesforce data? This app makes it easy.

If you've already used this app to check a book of business from the same provider, select the provider from the `Use Existing Automation` tab and click run! 

Otherwise, click the `Start new automation` button below to create a new automation.
""")

consume_tab, create_tab = st.tabs(["Use Existing Automation", "Start New Automation"])

with create_tab:

    provider_name = st.text_input("Provider Name", value="")
    description = st.text_area("Automation Description. Remind yourself which data to import in the future and the purpose of the automation.", value="")

    # Create an empty spreadsheet
    analysis: RunnableAnalysis = spreadsheet(
        import_folder='~',
        return_type='analysis',
        sheet_functions=[CHECK],
        key="recon creation spreadsheet",
        code_options={
            'as_function': True, 
            'function_name': f'create_{provider_name}_recon',
            'function_params': [],
            'call_function': False,
            'import_custom_python_code': True, 
        }
    )

    if st.button("Save automation"):
        if provider_name == '':
            st.warning("Please enter a provider name before saving")
            st.stop()

        if description == '':
            st.warning("Please enter a description before saving")
            st.stop()

        saved, error_message = save_analysis(provider_name, analysis, description)

        if not saved:
            st.error(error_message)        
        else:
            st.success(f"""
                Automation successfully saved as {provider_name} 
            """)
            with st.expander("View Generated Python Code", expanded=False):
                st.code(analysis.fully_parameterized_function)

with consume_tab:

    # Get all the provider names from the automations folder
    provider_names = get_all_provider_names_from_automations()
    provider_name = st.selectbox("Select a provider", provider_names)

    if provider_name is None:
        st.warning("Please select a provider")
        st.stop()

    # Get the analysis from the provider name
    analysis, description = get_runnable_analysis_and_description_from_provider_name(provider_name)

    st.info(f"Automation Description: {description}")

    st.markdown("### Upload the new BOB files")

    # Create an object to store the new values for the parameters
    updated_metadata = {}

    # Loop through the parameters in the analysis to display imports
    for idx, param in enumerate(analysis.get_param_metadata()):
        new_param = None

        # For imports that are exports, display a text input
        if param['subtype'] in ['file_name_export_excel', 'file_name_export_csv']:
            new_param = st.text_input(param['name'], value=param['original_value'], key=idx)
            
        # For imports that are file imports, display a file uploader
        elif param['subtype'] in ['file_name_import_excel', 'file_name_import_csv']:
            file_path = os.path.basename(param['original_value'])
            new_param = st.file_uploader(file_path, key=idx)
        
        if new_param is not None:
            updated_metadata[param['name']] = new_param

    # If all the metadata is not filled out, stop
    if len(updated_metadata) != len(analysis.get_param_metadata()):
        st.warning("Please fill out all the metadata")
        st.stop()

    result = analysis.run(**updated_metadata)

    if result is None:
        st.warning("This analysis concluded without any results. Please create this analysis again.")
    else:
        st.success("Check completed successfully. See below for results.")

    # Handle the annoying case where the result is a single dataframe
    if isinstance(result, pd.DataFrame):
        result = result, 

    spreadsheet(
        *result,
        import_folder='~',
        return_type='analysis',
        sheet_functions=[CHECK],
        key="recon consume spreadsheet"
    )