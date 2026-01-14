# Log 004: Fixing False Positives in Inline Policies
**Date:** 2026-01-13

## 1. The Issue (Alert Fatigue)
My previous implementation of `list_inline_policies` had a major logic flaw.
* **The Logic:** It checked if a user had *any* inline policy attached.
* **The Result:** It flagged harmless policies (like simple S3 Read access) as HIDDEN RISK.
* **Impact:** In a real security operations center (SOC), this causes Alert Fatigue, leading teams to ignore the tool completely.

## 2. The Fix (Deep Inspection)
I upgraded the scanner to look go deeper and find risky inline policies, and not just scanning for names.
### Old Workflow (Flawed)
1. List Users.
2. If User has Policy, an **ALARM** goes off.

### New Workflow (Corrected)
1. List Users.
2. Get Policy Names.
3. **Fetch Policy Document:** Used `iam.get_user_policy` to retrieve the actual JSON body.
4. **Analyze:** Passed the JSON to my `analyzer.py` engine.
5. **Verdict:** Only alarm if the engine finds specific risks (for exaample: `iam:CreateUser`).

## 3. The Comparison
I tested the new logic against two custom policies I created:

| Policy Name | Content | Old Result | New Result |
| :--- | :--- | :--- | :--- |
| `Safe-List-Only` | `s3:ListBucket` | RISK | Clean |
| `Risky-Backdoor` | `iam:CreateUser` | RISK | RISK |

The tool now successfully distinguishes between **Good Users** (developers with tools) and **Bad Users** (attackers with backdoors). It has now moved from a Detection Script to an Analysis Tool.

_Screenshot:_<img width="1883" height="712" alt="5C43F64A-C9A9-4331-8196-FA5901E200D9" src="https://github.com/user-attachments/assets/7dfb3294-4341-46dd-b4f5-b2733a34017f" />
 
**Security Note:** The AWS accounts shown in screenshots are either deleted, modified. No live credentials are exposed. This was done intentionally for illustrative purposes.
