import json
import time
from z3 import *    
from rich.console import Console                                            # type: ignore
from rich.prompt import Prompt, Confirm                                     # type: ignore
from rich.table import Table                                                # type: ignore
from rich.panel import Panel                                                # type: ignore
from rich import box                                                        # type: ignore

console = Console()
POLICY_FILE = "policies.json"

Z3_TYPE_MAP = {
    "String": String,
    "Bool": Bool,
    "Int": Int
}

# =========================
# LOAD / SAVE POLICIES
# =========================

def load_policy_schemas(filepath="policy_schemas.json"):
    with open(filepath, "r") as f:
        return json.load(f)
    
def load_policies():
    try:
        with open(POLICY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
def save_policies(policies):
    with open(POLICY_FILE, "w") as f:
        json.dump(policies, f, indent=2)

policies = load_policies()
policy_schemas = load_policy_schemas()

# =========================
# Z3 EVALUATION PARTS
# =========================

def sis_rule():
    pass

def exam_rule():
    pass

def lab_rule():
    pass

def privacy_rule():
    pass

RULE_MAP = {
    "SIS": sis_rule,
    "Exam": exam_rule,
    "Lab": lab_rule,
    "Privacy": privacy_rule,
}

def evaluate_policy(policy):
    """
    Evaluates a single policy rule and returns True if allowed, False if denied.
    """
    s = Solver()

    schema = policy_schemas[policy["type"]]
    z3_vars = {}

    for name, type_name in schema["vars"].items():
        constructor = Z3_TYPE_MAP[type_name]
        z3_vars[name] = constructor(f"{name}_{policy['type']}")

    # Bind values from policy to Z3 variables
    for name, var in z3_vars.items():

        value = policy.get(name)

        if isinstance(var, SeqRef):  # String
            s.add(var == StringVal(value))
        else:
            s.add(var == value)


    # Apply rule
    allowed = Bool(f"allowed_{policy['type']}")
    rule_function = RULE_MAP[policy["type"]]

    s.add(allowed == rule_function(z3_vars))

    # Solve
    if s.check() == sat:
        model = s.model()
        return bool(model[allowed])
    return False

