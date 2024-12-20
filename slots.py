
def slots_to_list(input_data):
    # Map of categories to labels
    category_to_label = {
        'Accessibility, Location & Transportation': 'ALT',
        'Activity Level': 'AL',
        'Atmosphere, Decor & Comfort': 'ADC',
        'Availability': 'AV',
        'Consistency': 'CON',
        'Flexibility and Customization': 'FC',
        'Hygiene & Compliance': 'HC',
        'Other': 'OTH',
        'Price & Fairness': 'PF',
        'Product Quality': 'PQ',
        'Restrictions': 'RES',
        'Safety & Trust': 'ST',
        'Service Quality': 'SQ',
        'Specialization': 'SP',
        'Target Audience': 'TA',
        'Time-Specific Circumstances': 'TSC',
        'Uniqueness': 'UNI',
        'General Sentiment': 'GS',
    }

    label_to_category = {v: k for k, v in category_to_label.items()}

    output_data = []
    for slot in input_data:
        entity_label = slot["entity"]
        fact = slot["value"]
        category = label_to_category.get(entity_label, "Unknown")
        output_data.append({
            "fact": fact,
            "label": category
        })

    return output_data


def fact_postprocessing(text):
    text = text.capitalize()
    text = re.sub(r"[,:\-;]$", ".", text)
    return text


def process_review(text):
    predictions = predict_ner(text, tokenizer, model, id2label)
    slots = convert_to_slots(predictions)
    facts_with_labels = slots_to_list(slots)
    for item in facts_with_labels:
        item['fact'] = fact_postprocessing(item['fact'])

    return facts_with_labels