def suggest_treatment(diagnosis):
    diagnosis = diagnosis.lower()
    if "flu" in diagnosis or "gripp" in diagnosis:
        return "Paracetamol 500mg, Rest, Hydration"
    elif "infection" in diagnosis:
        return "Antibiotics course, Hydration"
    elif "diabetes" in diagnosis:
        return "Insulin therapy, Diet control, Exercise"
    else:
        return "Consult doctor for personalized treatment"