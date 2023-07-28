from typing import List, Union
from schemas.eval_utils import EvaluatorViolation
from schemas.eval_model_and_source import DiscoModelNode, DiscoSourceNode


class PerformanceRuleSet:
    def __init__(self):
        self.violations: List[EvaluatorViolation, None] = []
        self.rule_map = {
            DiscoModelNode: [self.exposure_parent_materializations],
            DiscoSourceNode: []
        }

    def exposure_parent_materializations(self, model: DiscoModelNode):
        if any([child.uniqueId.startswith("exposure") for child in model.children]) and model.materializedType in ["view", "ephemeral"]:
            self.violations.append(
                EvaluatorViolation.parse_obj({
                    "short_summary":f"{model.name} is a view that is exposed to downstream consumers.",
                    "long_summary":f"""{model.name} is a view that is exposed to downstream consumers. models that are referenced by an exposure are likely to be used heavily in downstream systems, and therefore need to be performant when queried.""",
                    "model":model.name,
                    "unique_id":model.uniqueId,
                    "severity":"medium",
                    "rule_set":"Performance",
                    "rule_name":"Exposure Parent Materialization Types",
                    "exceptions": ""
                })
            )


    def process(self, resource: Union[DiscoModelNode, DiscoSourceNode]):
        rules = self.rule_map[type(resource)]
        for rule in rules:
            rule(resource)
        return self.violations
