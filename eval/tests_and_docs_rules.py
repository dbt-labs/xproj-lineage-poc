from typing import List, Union
from schemas.eval_utils import EvaluatorViolation
from schemas.eval_model_and_source import DiscoModelNode, DiscoSourceNode


class TestingAndDocumentationRuleSet:
    def __init__(self):
        self.rule_map = {
            DiscoModelNode:[self.missing_primary_key_tests, self.undocumented_model],
            DiscoSourceNode: []
        }
        self.violations: List[EvaluatorViolation, None] = []

    def missing_primary_key_tests(self, model: DiscoModelNode):
        column_summary = {}
        for test in model.tests:
            if test.columnName in column_summary.keys():
                column_summary[test.columnName].append(test.name)
            else:
                column_summary[test.columnName] = [test.name]
        primary_key = False
        for col, tests in column_summary.items():
            contains_unique = any(item.startswith('unique') for item in tests)
            contains_not_null = any(item.startswith('not_null') for item in tests)
            if contains_unique and contains_not_null:
                primary_key = True

        if not primary_key:
            self.violations.append(
                EvaluatorViolation.parse_obj({
                    "short_summary":f"{model.name} is missing a primary key tests",
                    "long_summary":f"""{model.name} is missing a primary key test. This test is important to ensure that the model is not generating duplicate records. Models without proper tests on their grain are a risk to the reliability and scalability of your project.""",
                    "model":model.name,
                    "unique_id":model.uniqueId,
                    "severity":"high",
                    "rule_set":"Testing",
                    "rule_name":"Missing Primary Key Tests",
                    "exceptions": ""
                })
            )

    def undocumented_model(self, model: DiscoModelNode):

        if not model.description or model.description == "":
            self.violations.append(
                EvaluatorViolation.parse_obj({
                    "short_summary":f"{model.name} is missing a description",
                    "long_summary":f"""{model.name} is missing a description. Good documentation for your dbt models will help downstream consumers discover and understand the datasets which you curate for them. The documentation for your project includes model code, a DAG of your project, any tests you've added to a column, and more.""",
                    "model":model.name,
                    "unique_id":model.uniqueId,
                    "severity":"medium",
                    "rule_set":"Documentation",
                    "rule_name":"Undocumented Model",
                    "exceptions": ""
                })
            )

    def process(self, resource: Union[DiscoModelNode, DiscoSourceNode]):
        rules = self.rule_map[type(resource)]
        for rule in rules:
            rule(resource)
        return self.violations
