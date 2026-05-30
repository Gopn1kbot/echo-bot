def analyze_memory(text: str):
    text_low = text.lower()

    # --- NAME ---
    if "меня зовут" in text_low:
        return {
            "key": "name",
            "value": text.split("зовут")[-1].strip(),
            "importance": 5
        }

    # --- CITY ---
    if "я из" in text_low:
        return {
            "key": "city",
            "value": text_low.split("я из")[-1].strip(),
            "importance": 4
        }

    # --- JOB ---
    if "я работаю" in text_low or "работаю" in text_low:
        return {
            "key": "job",
            "value": text_low.split("работаю")[-1].strip(),
            "importance": 4
        }

    # --- LIKES ---
    if "я люблю" in text_low:
        return {
            "key": "likes",
            "value": text_low.split("я люблю")[-1].strip(),
            "importance": 3
        }

    return None
