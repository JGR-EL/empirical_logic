# Empirical Logic

A bionic-inspired framework for rule-based decision-making with vague categories.

It enables structured reasoning using empirically derived knowledge 
— without relying on probability theory or fuzzy logic.

Designed for applications where decisions must be:

* interpretable
* context-sensitive
* based on simple, composable rules

⚙️ No probability theory
⚙️ No fuzzy logic

---

Empirical Logic provides a formal approach to handling vague categories, independent 
of classical methods from probability theory or fuzzy set theory.

Instead of modeling uncertainty, it focuses on the structured treatment of vagueness 
using a bipolar validity scale ranging from -1 (invalid) to +1 (valid).

It models vagueness, variable credibility, and experience-based inference in a formally 
structured way.

A key aspect is its bionic approach: the rules imitate structural principles observed
in biological neural systems.

Due to this structural analogy, computational capacity emerges from the collective
interaction of simple elements and constitutes a form of self-organization.

For a more detailed study of the theoretical foundations of "Empirical Logic", please 
refer to the references below.

---

## 👤 Author

Dr. rer. pol. Dipl.-Ing. Jens Grotrian

ORCID: https://orcid.org/0000-0003-0619-7038
e-Mail: jens.grotrian@posteo.de

---

## 📬 Contact

For academic collaboration or industrial applications, feel free to reach out.

---

## ⚖️ License (Short Summary)

This project is licensed under the **Empirical Logic Research License (ELRL) v1.0**.

It allows use, modification, and redistribution of the software, including 
for commercial purposes. Redistribution is allowed only under the same license 
terms. Sublicensing or distributing the software under a different license 
requires explicit written permission.

See the LICENSE file for full details.

---

## 💼 Commercial Licensing

While this project is available under the Empirical Logic Research License 
(ELRL) v1.0, commercial use cases that require redistribution under different 
terms, sublicensing, or integration into proprietary products may require a 
separate commercial license.

If your organization is interested in such use, please get in touch:

Dr. rer. pol. Dipl.-Ing. Jens Grotrian (jens.grotrian@posteo.de)

---

## 🚀 Installation

```bash
pip install empirical-logic
```

---
## Example: Ordering Decision Problem

This example demonstrates how **Empirical Logic** can be used to decide
which customer order should be processed next.

### 🧠 Problem

We want to prioritize customer orders based on multiple criteria:

* **Quantity** (higher is better)
* **Customer importance**
* **Urgency**

Each criterion contributes as a *pro* or *contra indication*.

### ⚖️ Preferences

Each decision criterion is expressed by a preference category whose 
validity value lies on a bipolar scale from -1 (e_FALSE) to +1 (e_TRUE) 
and which is tied to a reference magnitude. 

In this example the preferences are represented by the parameterizable 
sigmoid function "e_THRESHOLD" (t = threshold, f = uncertainty):

* **quantity_is_high** (t = 60, f = 40)
* **customer_is_important** (t = 5.5, f = 3)
* **order_is_urgent** (t = 5.5, f = 3)

### ⚖️ Weights

Preferences are weighted to reflect their importance:

* Quantity → **0.7**
* Customer importance → **0.4**

### 🔁 Dynamic Modulation

If an order is **urgent**, the influence of customer importance is increased
using *modulation*:

```
[validity value, modulation parameter]
```

This allows the system to adapt dynamically to context.

---

## 🧩 Implementation

```python
from empirical_logic.operators.validation_operators import (
    e_VALIDATE,
    e_INVALIDATE,
    e_DECIDE,
    e_WEIGHT,
)
from empirical_logic.operators.logical_operators import e_NOT
from empirical_logic.operators.validity_functions import e_THRESHOLD
from empirical_logic.core.exceptions import EmpiricalLogicError
from empirical_logic.core.constants import e_UNKNOWN


# ---------------------------
# Data model
# ---------------------------
class Order:
    def __init__(self, quantity: int, important_customer: int, urgency: int):
        self.quantity = quantity
        self.important_customer = important_customer
        self.urgency = urgency


# ---------------------------
# Validity functions
# ---------------------------
def quantity_is_high(quantity: int) -> float:
    return e_THRESHOLD(quantity, 60, 40)


def customer_is_important(importance: int) -> float:
    return e_THRESHOLD(importance, 5.5, 3)


def order_is_urgent(urgency: int) -> float:
    return e_THRESHOLD(urgency, 5.5, 3)


# ---------------------------
# Input data
# ---------------------------
orders = [
    Order(10, 7, 9),
    Order(100, 4, 4),
    Order(35, 5, 8),
    Order(50, 10, 10),
    Order(20, 3, 6),
]


# ---------------------------
# Dialog loop
# ---------------------------
while True:
    user_input = input(
        "\nOrdering Decision Problem\n"
        "Would you like to take the urgency of customer orders into account?\n"
        "Enter 1 = yes / 0 = no (or 'q' to quit): "
    ).strip().lower()

    if user_input in ("q", "quit"):
        print("Exiting program.")
        break

    if user_input not in ("0", "1"):
        print("Invalid input. Please enter 1, 0, or 'q'.")
        continue

    consider_urgency = user_input == "1"

    validated = [e_UNKNOWN for _ in orders]
    invalidated = [e_UNKNOWN for _ in orders]
    results = [e_UNKNOWN for _ in orders]

    try:
        for i, order in enumerate(orders):

            # Modulation factor (optional)
            mod = order_is_urgent(order.urgency) if consider_urgency else 0.0

            # --- PRO INDICATIONS ---
            pro_quantity = e_WEIGHT(quantity_is_high(order.quantity), 0.7)
            validated[i] = e_VALIDATE(pro_quantity, validated[i])

            pro_importance = [
                e_WEIGHT(customer_is_important(order.important_customer), 0.4),
                mod,
            ]
            validated[i] = e_VALIDATE(pro_importance, validated[i])

            # --- CONTRA INDICATIONS ---
            contra_quantity = e_WEIGHT(e_NOT(quantity_is_high(order.quantity)), 0.7)
            invalidated[i] = e_INVALIDATE(contra_quantity, invalidated[i])

            contra_importance = [
                e_WEIGHT(e_NOT(customer_is_important(order.important_customer)), 0.4),
                mod,
            ]
            invalidated[i] = e_INVALIDATE(contra_importance, invalidated[i])

            # --- FINAL DECISION ---
            results[i] = e_DECIDE(validated[i], invalidated[i])

        # Select best order
        best_index = max(range(len(results)), key=lambda i: results[i])

        # Output
        print("\nResulting order scores:")
        for i, value in enumerate(results):
            print(f"  Order {i+1}: {value:.3f}")

        print(f"\n→ Recommended next order: Order {best_index + 1}")

    except EmpiricalLogicError as e:
        print(f"Empirical Logic Error: {e}")
```

---

## ✅ Result

Although **Order 2** has the highest quantity, it is **not selected**.

👉 **Order 4 is chosen**, because:

* It has **high urgency**
* Urgency **amplifies customer importance**
* This shifts the decision despite lower quantity

---

## 💡 Key Takeaway

**Empirical Logic enables context-sensitive decisions** by combining:

* weighted preferences
* pro / contra reasoning
* dynamic modulation

This makes it more flexible than static scoring models.

---


## 📦 Features

This package provides:

### 1. Validation Operators

* `e_VALIDATE`
* `e_INVALIDATE`
* `e_DECIDE`
* `e_WEIGHT`

### 2. Logical Operators

Used to formulate premises for validation or invalidation of a hypothesis:

* `e_NOT`
* `e_AND`
* `e_OR`
* `e_XOR`
* `e_IF_POSSIBLE_ALL_OF`
* `e_SEVERAL_OF`
* `e_ONLY_ONE_OF`
* `e_NECESSARILY_ALL_OF`
* `e_AT_LEAST_ONE_OF`

### 3. Validity Functions

Describe relationships between categories and reference magnitudes:

* `e_THRESHOLD`
* `e_LIMITATION`
* `e_INTERVAL`
* `e_ESTIMATION`

Including inverse functions:

* `e_THRESHOLD_INVERSE`
* `e_LIMITATION_INVERSE`
* `e_INTERVAL_INVERSE`
* `e_ESTIMATION_INVERSE`

### 4. Modulation Function

* `e_MODULATE`

Implements dynamic "modulation" (weighting) of preferences in logical arguments.

> Note: `e_MODULATE(val, mod)` is equivalent to `[val, mod]` when used inside logical operators.

### 5. Blackboard System

Global modulation parameters:

* `e_M != 0` → general modulation of logical operator arguments
* `e_M1 != 0` → modulation of validation premises
* `e_M2 != 0` → modulation of validation hypotheses

---

## 📚 References

1. Jens Grotrian (2025)
   *Empirische Logik – Ein bionisch inspirierter Ansatz zur Entscheidungsfindung*
   https://doi.org/10.26127/BTUOpen-6974

2. Jens Grotrian (2025)
   *Thinking fast: a bionic approach to soft computing*
   https://doi.org/10.1007/s00500-025-10619-7

3. Jens Grotrian (2025)
   *Pensar Rápido – Un Planteamiento Biónico al Soft Computing*
   https://zenodo.org/doi/10.5281/zenodo.15649782

4. Jens Grotrian (2025)
   *An introduction to cluster analysis using Empirical Logic*
   https://zenodo.org/doi/10.5281/zenodo.17523740

5. Jens Grotrian (2025)
   *Designing Control Systems with Empirical Logic*
   https://zenodo.org/doi/10.5281/zenodo.17524902

6. Jens Grotrian (2025)
   *Empirical Logic (Maple programs)*
   https://zenodo.org/doi/10.5281/zenodo.14962362

---

## 📖 Summary

Empirical Logic combines:

* approximate reasoning
* empirical knowledge
* weighting and dynamic modulating of preferences

to support robust decision-making in complex systems.

---
