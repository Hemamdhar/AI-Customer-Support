import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
load_dotenv()

from app.ai.decide import decide
from evals.golden_emails import GOLDEN_EMAILS

failing_cases = ["pump-missing-no-order", "return-other-product", "replacement-shipping-time"]

for case in GOLDEN_EMAILS:
    if case["name"] in failing_cases:
        print(f"\n==========================================")
        print(f"Case: {case['name']}")
        print(f"Expected: section={case['section']}, action={case['action']}")
        d = decide(case["email"])
        print(f"Actual:   section={d.section}, action={d.action}")
        print(f"Reason:   {d.reason}")
        print(f"Reply:    {d.reply[:120]}...")
        time.sleep(4)

