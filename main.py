import json
import time
from z3 import *    
from rich.console import Console                                            # type: ignore
from rich.prompt import Prompt, Confirm                                     # type: ignore
from rich.table import Table                                                # type: ignore
from rich.panel import Panel                                                # type: ignore
from rich import box                                                        # type: ignore

console = Console()