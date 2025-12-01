from flask import jsonify
import re
def markdown_to_html(text):
    text = text.strip()
    if not text:
        return jsonify({"reply": "Please enter a message."})

        # Restriction 1: Block medicine-related topics
    if is_medicine_related(text):
        return jsonify({
            "reply": (
                "I cannot provide information about medicines, drugs, treatments, "
                "or dosages. I can only help with general health and diet topics."
            )
        })

        # Restriction 2: Allow ONLY health & diet topics
    if not is_health_or_diet(text):
        return jsonify({
            "reply": (
                "This chatbot only supports general health and diet questions. "
                "Please ask something related to food, nutrition, wellness, or fitness."
            )
        })
    # Basic markdown
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)

    lines = text.split("\n")
    html_parts = []
    in_ul = False
    in_ol = False

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            if in_ol:
                html_parts.append("</ol>")
                in_ol = False
            html_parts.append("<br>")
            continue

        # Numbered list
        if re.match(r"^\d+[\.)]\s", stripped):
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            if not in_ol:
                html_parts.append("<ol>")
                in_ol = True
            content = re.sub(r"^\d+[\.\)]\s+", "", stripped)
            html_parts.append(f"<li>{content}</li>")
            continue

        # Bullet list
        if stripped.startswith(("* ", "- ", "• ")):
            if in_ol:
                html_parts.append("</ol>")
                in_ol = False
            if not in_ul:
                html_parts.append("<ul>")
                in_ul = True
            content = stripped[2:].strip()
            html_parts.append(f"<li>{content}</li>")
            continue

        # Headings
        if stripped.startswith("###"):
            html_parts.append(f"<h3>{stripped[3:].strip()}</h3>")
            continue
        if stripped.startswith("##"):
            html_parts.append(f"<h3>{stripped[2:].strip()}</h3>")
            continue

        # Normal paragraph
        html_parts.append(f"<p>{stripped}</p>")

    if in_ul:
        html_parts.append("</ul>")
    if in_ol:
        html_parts.append("</ol>")

    return "\n".join(html_parts)


# ------------------ RESTRICTION FILTERS ------------------ #

def is_medicine_related(text: str) -> bool:
    """Block all medicine or treatment related topics."""
    medicine_words = [
        "medicine", "medication", "drug", "pill", "tablet", "capsule",
        "dose", "dosage", "mg", "prescription", "antibiotic",
        "painkiller", "treatment", "cure", "remedy", "therapy",
        "insulin", "vaccine", "syrup", "ointment"
    ]
    text_lower = text.lower()
    return any(word in text_lower for word in medicine_words)


def is_health_or_diet(text: str) -> bool:
    """
    Allow ONLY general health, diet, nutrition, and fitness questions.
    Block everything else.
    """
    allowed_keywords = [
        # General health / wellness
        "health", "healthy", "wellness", "lifestyle", "self care",

        # Diet / nutrition
        "diet", "food", "nutrition", "meal", "eat", "eating",
        "calories", "protein", "carbs", "fats", "vitamins",
        "minerals", "hydration", "water intake",

        # Fitness / exercise
        "exercise", "workout", "fitness", "gym", "training",
        "running", "walking", "yoga", "stretching", "cardio",

        # Weight-related
        "weight", "fat loss", "weight gain", "muscle", "body fat",

        # Small-talk allowed
        "hi", "hello", "hey", "thank", "ok", "okay", "bye"
    ]

    text_lower = text.lower()
    return any(word in text_lower for word in allowed_keywords)


def clean_gemini_response(text: str) -> str:
    return text.strip()
