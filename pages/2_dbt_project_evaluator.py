from typing import List
from eval.modeling_rules import ModelingRuleSet
from eval.performance_rules import PerformanceRuleSet
from eval.tests_and_docs_rules import TestingAndDocumentationRuleSet
from query.query_eval import get_all_models, get_all_sources 
from schemas.eval_utils import EvaluatorViolation
import plotly.express as px
import pandas as pd
import streamlit as st
from utils.get_eval_data import show_resource_violations
from utils.set_variables import check_variables

check_variables()

model_data = get_all_models()
source_data = get_all_sources()
models = [node.node for node in model_data.environment.definition.models.edges]
sources = [node.node for node in source_data.environment.definition.sources.edges]
all_resources = models + sources

st.header("`dbt_project_evaluator`")

def get_all_violations(_resource_responses):
    all_violations = []
    for resource in _resource_responses:
        for rulesets in [ModelingRuleSet, TestingAndDocumentationRuleSet, PerformanceRuleSet]:
            all_violations.extend(rulesets().process(resource))
    return all_violations

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

def get_violations_by_resource(violations: List[EvaluatorViolation]):
    violation_map = {}
    for violation in violations:
        if violation.model not in violation_map.keys():
            violation_map[violation.model] = 1
        else:
            violation_map[violation.model] += 1
    df = pd.DataFrame.from_dict(violation_map, orient="index").reset_index()
    df.columns = ["Resource", "Total Count"]
    return df

severity_map = get_violations_by_severity(all_violations)
rule_category_map = get_violations_by_rule_set(all_violations)
resource_map = get_violations_by_resource(all_violations)
severity_plot = px.bar(severity_map, y="Severity", x="Total Count", orientation='h', color="Severity")
rule_set_plot = px.bar(rule_category_map, y="Rule Category", x="Total Count", orientation='h', color="Rule Category")
resource_plot = px.bar(resource_map, y="Resource", x="Total Count", orientation='h', color="Resource")
grouper = st.selectbox(
        "View Violations by",
        ("Severity", "Rule Category", "Resource")
    )
if grouper == "Severity":
    st.subheader("Total Violations by Severity")
    st.plotly_chart(severity_plot)
    st.subheader("View Violations by Severity")
    severity_levels = set([violation.severity.value for violation in all_violations])
    severity = st.selectbox("Select a resource with a violation", severity_levels)
    resource_violations = [violation for violation in all_violations if violation.severity == severity]
    show_resource_violations(resource_violations)
elif grouper == "Resource":
    st.subheader("Total Violations by Resource")
    st.plotly_chart(resource_plot)
    st.subheader("View Violations by Resource")
    violating_resources = set([violation.model for violation in all_violations])
    model = st.selectbox("Select a resource with a violation", violating_resources)
    resource_violations = [violation for violation in all_violations if violation.model == model]
    show_resource_violations(resource_violations)

elif grouper == "Rule Category":
    st.subheader("Total Violations by Rule Category")
    st.plotly_chart(rule_set_plot)
    st.subheader("View Violations by Rule Category")
    rule_sets = set([violation.rule_set for violation in all_violations])
    rule_set = st.selectbox("Select a resource with a violation", rule_sets)
    resource_violations = [violation for violation in all_violations if violation.rule_set == rule_set]
    show_resource_violations(resource_violations)

# st.write(severity_map)
## This is the section to look at a single resource and evaluate it
