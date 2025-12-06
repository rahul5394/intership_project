import re

# ----------------------------------------------------------
#                STRICT TOPIC FILTER SETTINGS
# ----------------------------------------------------------

ALLOWED_TOPICS = [
    "health", "fitness", "diet", "nutrition", "food",
    "exercise", "workout", "daily routine", "routine",
    "water", "sleep", "lifestyle","diet","hii"
]

BLOCKED_KEYWORDS = [
    "medicine", "pill", "tablet", "dose", "dosage", "mg",
    "prescription", "drug", "treatment", "therapy",
    "disease", "symptom", "injury", "diagnose", "antibiotic",
    "injection"
]

SIMPLE_ALLOWED = ["hi","hii", "hello", "hey", "ok", "okay", "bye", "thanks", "thank you"]


def topic_filter(text: str) -> bool:
    """Strict filter: Only health, diet, fitness, daily routine."""
    text_l = text.lower().strip()

    # Allowed simple messages
    if text_l in SIMPLE_ALLOWED:
        return True

    # Block strong medical topics
    for bad in BLOCKED_KEYWORDS:
        if bad in text_l:
            return False

    # Allow only messages containing allowed topics
    for good in ALLOWED_TOPICS:
        if good in text_l:
            return True

    # Everything else is blocked
    return False


# ----------------------------------------------------------
#                MARKDOWN TABLE SUPPORT
# ----------------------------------------------------------

def convert_markdown_table(lines):
    """Convert |col|col| style markdown table to HTML."""
    table_lines = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if "|" in line:
            table_lines.append(line)
            i += 1
        else:
            break

    if len(table_lines) < 2:
        return None, 0

    # Build Table
    html = ["<table>", "<thead>"]

    header = table_lines[0].split("|")[1:-1]
    html.append("<tr>" + "".join(f"<th>{h.strip()}</th>" for h in header) + "</tr>")
    html.append("</thead><tbody>")

    for row in table_lines[2:]:
        cols = row.split("|")[1:-1]
        html.append("<tr>" + "".join(f"<td>{c.strip()}</td>" for c in cols) + "</tr>")

    html.append("</tbody></table>")

    return "\n".join(html), i


# ----------------------------------------------------------
#                MAIN MARKDOWN → HTML FUNCTION
# ----------------------------------------------------------

def markdown_to_html(text):
    text = text.strip()

    if not text:
        return "<p>Please enter a message.</p>"

    # STRICT TOPIC CHECK
    if not topic_filter(text):
        return """
        <div style='padding:12px;border-left:4px solid red;background:#ffecec;'>
            <strong>Not Allowed:</strong> I only accept topics about general health, 
            diet, fitness, and daily routine.
        </div>
        """

    # Basic Markdown Styles
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)

    lines = text.split("\n")
    html_parts = []

    in_ul = False
    in_ol = False

    i = 0
    while i < len(lines):
        stripped = lines[i].strip()

        # ---------------- TABLE SUPPORT ----------------
        table_html, consumed = convert_markdown_table(lines[i:])
        if consumed > 0:
            html_parts.append(table_html)
            i += consumed
            continue

        # Empty Line
        if not stripped:
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            if in_ol:
                html_parts.append("</ol>")
                in_ol = False
            html_parts.append("<br>")
            i += 1
            continue

        # Ordered List
        if re.match(r"^\d+[\.)]\s", stripped):
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            if not in_ol:
                html_parts.append("<ol>")
                in_ol = True

            content = re.sub(r"^\d+[\.\)]\s+", "", stripped)
            html_parts.append(f"<li>{content}</li>")
            i += 1
            continue

        # Bullet List
        if stripped.startswith(("* ", "- ", "• ")):
            if in_ol:
                html_parts.append("</ol>")
                in_ol = False
            if not in_ul:
                html_parts.append("<ul>")
                in_ul = True

            html_parts.append(f"<li>{stripped[2:].strip()}</li>")
            i += 1
            continue

        # Close lists before text
        if in_ul:
            html_parts.append("</ul>")
            in_ul = False
        if in_ol:
            html_parts.append("</ol>")
            in_ol = False

        # Headings
        if stripped.startswith("###"):
            html_parts.append(f"<h3>{stripped[3:].strip()}</h3>")
            i += 1
            continue

        if stripped.startswith("##"):
            html_parts.append(f"<h2>{stripped[2:].strip()}</h2>")
            i += 1
            continue

        if stripped.startswith("#"):
            html_parts.append(f"<h1>{stripped[1:].strip()}</h1>")
            i += 1
            continue

        # Paragraph
        html_parts.append(f"<p>{stripped}</p>")
        i += 1

    # Close remaining lists
    if in_ul:
        html_parts.append("</ul>")
    if in_ol:
        html_parts.append("</ol>")

    return "\n".join(html_parts)


# ----------------------------------------------------------
#                 CLEAN RESPONSE FUNCTION
# ----------------------------------------------------------

def clean_gemini_response(text: str) -> str:
    return text.strip()
