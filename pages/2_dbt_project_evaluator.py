from typing import Dict, List
from eval.modeling_rules import ModelingRuleSet
from eval.performance_rules import PerformanceRuleSet
from eval.tests_and_docs_rules import TestingAndDocumentationRuleSet
from query.query_eval import get_all_unique_ids, query_single_resource
from schemas.eval_model_and_source import EvalDiscoResponse
from schemas.eval_utils import EvaluatorViolation
import plotly.express as px
import pandas as pd
import streamlit as st
from utils.set_variables import check_variables

check_variables()

unique_ids = get_all_unique_ids()

st.header("`dbt_project_evaluator`")

def get_all_resources(unique_ids: Dict[str, EvalDiscoResponse]):
    all_resources = {}
    for unique_id in unique_ids:
        selected_resource_type = unique_id.split(".")[0]
        resp = query_single_resource(resource_type = selected_resource_type, unique_id=unique_id)
        all_resources[unique_id] = resp
    return all_resources

def get_all_violations(_resource_responses):
    all_violations = []
    for unique_id, resp in _resource_responses.items():
        resource_defintion = resp.environment.definition
        selected_resource_type = unique_id.split(".")[0]
        resource = getattr(resource_defintion, selected_resource_type + "s").edges[0].node
        for rulesets in [ModelingRuleSet, TestingAndDocumentationRuleSet, PerformanceRuleSet]:
            all_violations.extend(rulesets().process(resource))
    return all_violations

all_resources = get_all_resources(unique_ids)
all_violations = get_all_violations(all_resources)
st.subheader(f"Total Violations: {len(all_violations)}")

def get_violations_by_severity(violations: List[EvaluatorViolation]):
    violation_map = {}
    for violation in violations:
        if violation.severity not in violation_map.keys():
            violation_map[violation.severity.value] = 1
        else:
            violation_map[violation.severity.value] += 1
    df = pd.DataFrame.from_dict(violation_map, orient="index").reset_index()
    df.columns = ["Severity", "Total Count"]
    return df

def get_violations_by_rule_set(violations: List[EvaluatorViolation]):
    violation_map = {}
    for violation in violations:
        if violation.rule_set not in violation_map.keys():
            violation_map[violation.rule_set] = 1
        else:
            violation_map[violation.rule_set] += 1
    df = pd.DataFrame.from_dict(violation_map, orient="index").reset_index()
    df.columns = ["Rule Category", "Total Count"]
    return df

def get_violations_by_model(violations: List[EvaluatorViolation]):
    violation_map = {}
    for violation in violations:
        if violation.model not in violation_map.keys():
            violation_map[violation.model] = 1
        else:
            violation_map[violation.model] += 1
    df = pd.DataFrame.from_dict(violation_map, orient="index").reset_index()
    df.columns = ["Model Name", "Total Count"]
    return df

severity_map = get_violations_by_severity(all_violations)
rule_category_map = get_violations_by_rule_set(all_violations)
model_map = get_violations_by_model(all_violations)
severity_plot = px.bar(severity_map, y="Severity", x="Total Count", orientation='h', color="Severity")
rule_set_plot = px.bar(rule_category_map, y="Rule Category", x="Total Count", orientation='h', color="Rule Category")
model_plot = px.bar(model_map, y="Model Name", x="Total Count", orientation='h', color="Model Name")
grouper = st.selectbox(
        "View Violations by",
        ("Severity", "Rule Category", "Model Name")
    )
if grouper == "Severity":
    st.subheader("Violations by Severity")
    st.plotly_chart(severity_plot)
elif grouper == "Model Name":
    st.subheader("Violations by Model Name")
    st.plotly_chart(model_plot)
elif grouper == "Rule Category":
    st.subheader("Violations by Rule Category")
    st.plotly_chart(rule_set_plot)

## This is the section to look at a single resource and evaluate it
st.subheader("Violations by Resource")
violating_resources = set([violation.unique_id for violation in all_violations])
unique_id = st.selectbox("Select a resource with a violation", violating_resources)

resource_violations = [violation for violation in all_violations if violation.unique_id == unique_id]

for violation in resource_violations:
    with st.expander(str(violation)):
        st.markdown(f"**{violation.short_summary}**")
        st.markdown(f"**Severity**: {violation.severity}")
        st.markdown(f"**Details**: \n\n{violation.long_summary}")
        if violation.exceptions:
            st.markdown(f"**Exceptions**: \n\n{violation.exceptions}")