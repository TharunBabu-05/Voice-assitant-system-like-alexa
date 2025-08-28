import requests
import datetime

def handle(text):
    text = text.lower()
    if "time" in text:
        now = datetime.datetime.now().strftime('%H:%M')
        return f"The time is {now}."
    if "wikipedia" in text:
        try:
            import wikipedia
            query = text.replace("wikipedia", "").strip()
            summary = wikipedia.summary(query, sentences=1)
            return summary
        except Exception:
            return "Sorry, I couldn't fetch Wikipedia info."
    if "news" in text:
        return "Sorry, news feature not implemented yet."
    return None
