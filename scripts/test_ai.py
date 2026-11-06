import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.ai.classifier import classify
from app.ai.decide import decide

test_email = "Which paddle board should I get? I weigh 90 kg."
if len(sys.argv) > 1:
    test_email = sys.argv[1]

print(f"Testing with input:\n{test_email}\n")

print("1. Running classify()...")
classification = classify(test_email)
print("Classification result:")
print(f"  section: {classification.section}")
print(f"  needs_human: {classification.needs_human}")
print(f"  reason: {classification.reason}")
print(f"  acknowledgement: {classification.acknowledgement}")

print("\n2. Running decide()...")
decision = decide(test_email)
print("Decision result:")
print(f"  action: {decision.action}")
print(f"  section: {decision.section}")
print(f"  reply:\n{decision.reply}")

