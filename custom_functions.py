import pandas as pd

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