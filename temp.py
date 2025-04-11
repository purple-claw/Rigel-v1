import csv
import random
from faker import Faker
from datetime import datetime
from tqdm import tqdm

fake = Faker()

risk_levels = {
    "high" : (0.85,1.0),
    "medium" : (0.45, 0.84),
    "low" : (0.0, 0.44)
}

categories = [
    "privacy_data_usage", "payment_terms", "late_fees", "interest_rates",
    "termination_rights", "third_party_sharing", "user_obligations",
    "consent_clarity", "penalty_clauses", "data_retention"
]

TEMPLATES = {
    "high": [
        "We may modify the terms without prior notice to the user.",
        "Late payment will incur a recurring penalty of 25% per month.",
        "Interest rates can reach up to 42% annually.",
        "Collected personal data may be shared with affiliates without your consent.",
        "The company has the right to terminate services at its sole discretion."
    ],
    "medium": [
        "Failure to comply may result in service suspension upon review.",
        "Interest rates vary based on credit score and are updated quarterly.",
        "User data might be shared for analytics under anonymized conditions.",
        "Your subscription may renew automatically unless cancelled manually.",
        "We may charge a reactivation fee after 30 days of inactivity."
    ],
    "low": [
        "Personal data will only be used to provide requested services.",
        "Users will be notified of any major changes to the agreement.",
        "Standard interest rate is fixed at 7.5% annually with full transparency.",
        "Data sharing with third parties occurs only after explicit consent.",
        "You may terminate your agreement at any time with a 7-day notice."
    ]
}

SOURCES = ["synthetic_template", "semi_random_generated"]

def generate_clause(risk_level: str, category: str) -> dict:
    base_template = random.choice(TEMPLATES[risk_level])
    clause = fake.paragraph(nb_sentences=random.randint(1, 2)) + " " + base_template

    risk_range = risk_levels[risk_level]
    risk_prob = round(random.uniform(risk_range[0], risk_range[1]), 2)
    label = 1 if risk_level == "high" else 0

    return {
        "clause_text": clause,
        "risk_index": risk_level,
        "label": label,
        "probability_of_risk": risk_prob,
        "category": category,
        "source": random.choice(SOURCES)
    }

def generate_dataset(num_entries: int = 5000, output_file: str = "fraud_clauses_dataset.csv"):
    data = []
    for _ in tqdm(range(num_entries), desc="Generating clauses"):
        risk = random.choices(["high", "medium", "low"], weights=[0.3, 0.4, 0.3])[0]
        category = random.choice(categories)
        clause = generate_clause(risk, category)
        data.append(clause)

def generate_dataset(num_entries: int = 5000, output_file: str = "fraud_clauses_dataset.csv"):
    data = []
    for _ in tqdm(range(num_entries), desc="Generating clauses"):
        risk = random.choices(["high", "medium", "low"], weights=[0.3, 0.4, 0.3])[0]
        category = random.choice(categories)
        clause = generate_clause(risk, category)
        data.append(clause)

    # Save to CSV
    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"\n✅ Dataset successfully saved to '{output_file}' with {num_entries} entries.")

if __name__ == "__main__":
    start = datetime.now()
    generate_dataset()
    print("Time taken:", datetime.now() - start)