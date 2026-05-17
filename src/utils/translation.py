from deep_translator import GoogleTranslator

def translate_to_english(text: str, src_lang: str) -> str:
    if src_lang.lower() == "en":
        return text
    return GoogleTranslator(source=src_lang, target="en").translate(text)

def translate_from_english(text: str, target_lang: str) -> str:
    if target_lang.lower() == "en":
        return text
    return GoogleTranslator(source="en", target=target_lang).translate(text)
