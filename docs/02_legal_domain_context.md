# RTI Legal Context & Ambiguity Rules

## 1. The Section 6(3) Legal Mandate
Under Section 6(3) of the RTI Act, if an application is submitted to the wrong public authority, the receiving officer must transfer it to the correct department within a strict 5-day limit. Failure triggers a penalty of Rs. 250 per day. Our system prevents this by identifying ambiguity on Day 1.

## 2. First Appeal Timelines
If an application is ignored or misrouted, a citizen has the right to file a First Appeal within 30 days of the reply due date. When our system escalates an application, it must generate a draft appeal based on these timelines.

## 3. Department Taxonomy (The 10 Labels)
The model must classify exclusively into these labels:
`PWD`, `WATER`, `EDU`, `HEALTH`, `RATION`, `POLICE`, `TRANSPORT`, `ELEC`, `MUNI`, `REV`.

## 4. Ambiguity & Escalation Logic
The backend must enforce escalation if either condition is met:
1. **Mathematical Uncertainty:** Let $P_1$ be the top probability score and $P_2$ be the second highest. Escalate if $P_1 < 0.85$ OR if the margin $(P_1 - P_2) < 0.15$.
2. **Deterministic Overlap:** If the model predicts `MUNI` and `PWD` in the top 2, escalate immediately (due to unwritten local state conventions regarding road maintenance).