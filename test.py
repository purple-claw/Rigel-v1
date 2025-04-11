from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

model = AutoModelForSequenceClassification.from_pretrained("nitinsri/RigelClauseNet")
tokenizer = AutoTokenizer.from_pretrained("nitinsri/RigelClauseNet")

def predict_clause_risk(text):
    device = next(model.parameters()).device
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Run inference
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=1).squeeze().tolist()

    # Interpret result
    label = int(torch.argmax(logits, dim=1).item())
    label_name = "RISKY" if label == 1 else "SAFE"
    confidence = round(probs[label] * 100, 2)

    return {
        "text": text,
        "predicted_label": label,
        "label_meaning": label_name,
        "confidence": f"{confidence}%",
        "probabilities": {
            "SAFE (0)": round(probs[0], 4),
            "RISKY (1)": round(probs[1], 4)
        }
    }

test_clauses = [
    "Late payments will incur a 20% recurring monthly penalty.",
    "We reserve the right to terminate your access at any time without notice.",
    "Personal data is stored securely and will only be used for service delivery.",
    "Interest rates are capped at 7.5% per annum as per RBI norms.",
    "This agreement is binding upon signature, and you forfeit all refund rights.",
    "User activity may be shared with unknown third parties.",
    "You may cancel anytime without penalty.",
]

for clause in test_clauses:
    result = predict_clause_risk(clause)
    print("\n---")
    for k, v in result.items():
        print(f"{k}: {v}")
