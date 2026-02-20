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