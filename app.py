import json
import streamlit as st
import pandas as pd 
from mitosheet.streamlit.v1 import spreadsheet, RunnableAnalysis
import os
from file_utils import save_analysis, get_all_provider_names_from_automations, get_runnable_analysis_from_provider_name

# Set the streamlit page to wide so you can see the whole spreadsheet
st.set_page_config(layout="wide")

if not os.path.exists(os.path.join(os.getcwd(), 'automations')):
    os.mkdir(os.path.join(os.getcwd(), 'automations'))

if not os.path.exists(os.path.join(os.getcwd(), 'data')):
    os.mkdir(os.path.join(os.getcwd(), 'data'))

def CHECK(val1, val2, mismatch_label=False):

    # For each cell in val 1 and val2 perform the following check

    def _check_if_value_is_none(val):
        if val is None or pd.isna(val):
            return True
        else:
            return False
    
    def _check(val1, val2, mismatch_label):

        if _check_if_value_is_none(val1) and _check_if_value_is_none(val2):
            return True if not mismatch_label else ''
        elif val1 == val2:
            return True if not mismatch_label else ''
        else:
            return mismatch_label

    # Use the _check on series val1 and val2
    if isinstance(val1, pd.Series) and isinstance(val2, pd.Series):
        return pd.Series([_check(v1, v2, mismatch_label) for v1, v2 in zip(val1, val2)])


st.title("Book of Business Checker")
st.markdown("""Need to check a new book of business against our salesforce data? This app makes it easy.

If you've already used this app to check a book of business from the same provider, select the provider from the `Use Existing Automation` tab and click run! 

Otherwise, click the `Start new automation` button below to create a new automation.
""")

consume_tab, create_tab = st.tabs(["Use Existing Automation", "Start New Automation"])

with create_tab:

    provider_name = st.text_input("Provider Name", value="")

    # Create an empty spreadsheet
    analysis: RunnableAnalysis = spreadsheet(
        import_folder='~',
        return_type='analysis',
        sheet_functions=[CHECK]
    )

    if st.button("Save automation"):
        if provider_name == '':
            st.warning("Please enter a provider name before saving")
            st.stop()

        saved, error_message = save_analysis(provider_name, analysis)

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
    analysis = get_runnable_analysis_from_provider_name(provider_name)

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

    # Show a button to trigger re-running the analysis with the updated_metadata
    run = st.button('Run')
    if run:
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
            sheet_functions=[CHECK]
        )