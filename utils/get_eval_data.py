from typing import List
from schemas.eval_utils import EvaluatorViolation
import streamlit as st

def show_resource_violations(resource_violations: List[EvaluatorViolation]):
    for violation in resource_violations:
            with st.expander(str(violation)):
                st.markdown(f"**{violation.short_summary}**")
                st.markdown(f"**Severity**: {violation.severity}")
                st.markdown(f"**Details**: \n\n{violation.long_summary}")
                if violation.exceptions:
                    st.markdown(f"**Exceptions**: \n\n{violation.exceptions}")