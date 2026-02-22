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
    return If(vars["role"] == StringVal("admin"), True,
           If(And(vars["role"] == StringVal("faculty"),
                  Or(vars["action"] == StringVal("view"),
                     vars["action"] == StringVal("edit")),
                  vars["owner"]), True,
           If(And(vars["role"] == StringVal("student"),
                  Or(vars["action"] == StringVal("view"),
                     vars["action"] == StringVal("edit")),
                  vars["owner"]), True,
           False)))

def exam_rule():
    return Not(And(vars["create"], vars["grade"], vars["invigilate"]))

def lab_rule():
    return And(vars["hour"] >= 8,
               vars["hour"] <= 20,
               If(vars["system"] == StringVal("server"),
                  vars["on_campus"],
                  True))

def privacy_rule():
    return If(
        Not(vars["access_requested"]),
        True,  # no access requested → allowed
        If(
            vars["status"] != StringVal("graduated"),
            True,  # normal privacy rules don’t restrict
            If(
                Or(vars["role"] == StringVal("admin"),
                   vars["role"] == StringVal("registrar")),
                True,  # full authority
                If(
                    And(vars["role"] == StringVal("faculty"),
                        vars["action"] == StringVal("view")),
                    True,  # limited read-only access
                    False  # default deny
                )
            )
        )
    )

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

# =========================
# USER INTERACTING PARTS
# =========================

def add_policy():
    policy_type = Prompt.ask("Policy type", choices=["SIS","Exam","Lab","Privacy"])

    while True:
        policy_id = Prompt.ask("Policy ID (unique)")
        if policy_id in policies:
            console.print(Panel(f"[bold red]Policy ID '{policy_id}' already exists![/bold red]\nPlease choose a different ID.", border_style="red"))
            continue  # retry
        break

    policy = {"type": policy_type}

    if policy_type == "SIS":
        policy["role"] = Prompt.ask("Role", choices=["student","faculty","admin"])
        policy["action"] = Prompt.ask("Action", choices=["view","edit"])
        policy["owner"] = Confirm.ask("Is Owner of Record?")

    elif policy_type == "Exam":
        policy["create"] = Confirm.ask("Can Create Exam?")
        policy["grade"] = Confirm.ask("Can Grade Exam?")
        policy["invigilate"] = Confirm.ask("Can Invigilate Exam?")

    elif policy_type == "Lab":
        policy["system"] = Prompt.ask("System", choices=["lab_pc","server"])
        policy["on_campus"] = Confirm.ask("On Campus IP?")
        policy["hour"] = int(Prompt.ask("Hour (0-23)"))

    elif policy_type == "Privacy":
        policy["role"] = Prompt.ask("Role", choices=["student", "faculty", "admin", "registrar"])
        policy["status"] = Prompt.ask("Status", choices=["enrolled", "graduated"])
        policy["action"] = Prompt.ask("Action",choices=["view", "edit", "delete"])
        policy["access_requested"] = Confirm.ask("Access Requested?")


    policies[policy_id] = policy
    save_policies(policies)
    console.print(Panel(f"Policy {policy_id} added.", border_style="green"))

def delete_policy():
    if not policies:
        console.print(Panel("[bold yellow]No policies to delete.[/bold yellow]"))
        return

    display_policy_list()
    policy_id = Prompt.ask("Enter Policy ID to delete")
    if policy_id in policies:
        confirm = Confirm.ask(f"Are you sure you want to delete policy '{policy_id}'?")
        if confirm:
            del policies[policy_id]
            save_policies(policies)
            console.print(Panel(f"Policy '{policy_id}' deleted.", border_style="red"))
    else:
        console.print(Panel(f"[bold red]Policy ID '{policy_id}' not found.[/bold red]"))

def check_policy():
    display_policy_list()
    policy_id = Prompt.ask("Enter Policy ID to evaluate")
    if policy_id in policies:
        result = evaluate_policy(policies[policy_id])
        color = "green" if result else "red"
        status = "ALLOWED" if result else "DENIED"
        console.print(Panel(f"[bold]{status}[/bold]\n\n{policies[policy_id]}", border_style=color))
    else:
        console.print("[bold red]Policy ID not found[/bold red]")

# =========================
# CLI DISPLAYING PARTS
# =========================

def display_policy_list():
    table = Table(title="Policy List", box=box.ROUNDED)
    table.add_column("ID", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Details", style="white")
    for key, val in policies.items():
        table.add_row(key, val["type"], str(val))
    console.print(table)

check_policy()