import json
import streamlit as st
import pandas as pd 
from mitosheet.streamlit.v1 import spreadsheet, RunnableAnalysis
import os

# Set the streamlit page to wide so you can see the whole spreadsheet
st.set_page_config(layout="wide")

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
st.markdown("""Need to check a new book of business against our salesforce data? This app makes it easy

If you've already used this app to check a book of business from the same provider, select that provider from below and click run! 

Otherwise, click the `Start new automation` button below to create a new automation.
""")

create_tab, consume_tab = st.tabs(["Start New Automation", "Use Existing Automation"])

with create_tab:

    provider_name = st.text_input("Provider Name", value="")

    # Create an empty spreadsheet
    analysis: RunnableAnalysis = spreadsheet(
        import_folder='./',
        return_type='analysis',
        sheet_functions=[CHECK]
    )

    if st.button("Save automation"):
        # When the user clicks the button, save the generated_code returned by the spreadsheet 
        # component to a .py file in the /scripts directory.
        file_path = os.path.join(os.getcwd(), 'scripts', provider_name + '.py')
        with open(file_path, 'w') as f:
            f.write(analysis.to_json())
            st.success(f"""
                Automation successfully saved as {provider_name} 
            """)
            with st.expander("View Generated Python Code", expanded=False):
                st.code(analysis.fully_parameterized_function)


with consume_tab:

    # Read the file names from the scripts folder
    file_names = os.listdir(os.path.join(os.getcwd(), 'scripts'))

    # Remove the .py from the end
    file_names = [file_name.split('.')[0] for file_name in file_names]

    # Create a dropdown to select the file name
    file_name = st.selectbox("Select a provider", file_names)

    if file_name is None:
        st.stop()

    path = os.path.join(os.getcwd(), 'scripts', file_name + '.py')
    # Read the contents of the path
    with open(path, 'r') as f:
        json_string = f.read()

    analysis = RunnableAnalysis.from_json(json_string)

    st.markdown("### Upload the new BOB files")

    # Create an object to store the new values for the parameters
    updated_metadata = {}

    # Loop through the parameters in the analysis to display imports
    for param in analysis.get_param_metadata():
        new_param = None

        # For imports that are exports, display a text input
        if param['subtype'] in ['file_name_export_excel', 'file_name_export_csv']:
            new_param = st.text_input(param['name'], value=param['initial_value'])
            
        # For imports that are file imports, display a file uploader
        elif param['subtype'] in ['file_name_import_excel', 'file_name_import_csv']:
            new_param = st.file_uploader(param['name'])
        
        if new_param is not None:
            updated_metadata[param['name']] = new_param

    # Show a button to trigger re-running the analysis with the updated_metadata
    run = st.button('Run')
    if run:
        result = analysis.run(**updated_metadata)
        spreadsheet(
            *result,
            import_folder='./',
            return_type='analysis',
            sheet_functions=[CHECK]
        )

    

