from langchain.tools import tool
from deep_translator import GoogleTranslator
import re

# Supported language codes
LANGUAGE_CODES = {
    "english": "en",
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "italian": "it",
    "swahili": "sw",
    "chinese simplified": "zh-CN",
    "chinese traditional": "zh-TW",
    "japanese": "ja",
    "korean": "ko",
    "arabic": "ar",
    "russian": "ru",
}

@tool("translate_text", return_direct=True)
def translate_text(user_input: str) -> str:
    """
    Translate text into the user-specified language.

    Handles natural requests like:
    - "Translate this to French: I love programming"
    - "Please translate 'How are you?' in Chinese Simplified"
    - "Can you translate Hello world to Swahili?"
    """

    try:
        # Normalize input
        user_input = user_input.strip()

        # Regex patterns to detect language and text
        patterns = [
            r"(?:translate|translation)\s+(?:this\s+)?(?:to|in)\s+([a-zA-Z ]+)\s*[:]?['\"]?(.*)['\"]?",  # Translate this to French: text
            r"(?:please\s+)?(?:translate|translation)\s+['\"]?(.*)['\"]?\s+(?:to|in)\s+([a-zA-Z ]+)"   # Please translate "text" to French
        ]

        target_language = None
        text_to_translate = None

        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    # Determine which group is language and which is text
                    if pattern.startswith("(?:translate"):
                        target_language, text_to_translate = match.group(1), match.group(2)
                    else:
                        text_to_translate, target_language = match.group(1), match.group(2)
                break

        if not target_language:
            # Default to Spanish if no language detected
            target_language = "spanish"
        if not text_to_translate:
            # If no text detected, remove the command words from input
            text_to_translate = re.sub(r"(translate|translation|to|in|please)", "", user_input, flags=re.IGNORECASE).strip()

        target_code = LANGUAGE_CODES.get(target_language.lower())
        if not target_code:
            return f"Sorry, I don’t support translating to '{target_language}'. Supported: {list(LANGUAGE_CODES.keys())}"

        translation = GoogleTranslator(source="auto", target=target_code).translate(text_to_translate)
        return f"Sure ma'am, the translation for '{text_to_translate}' in {target_language.title()} is: '{translation}'"

    except Exception as e:
        return f"Sorry, I couldn't translate the text due to: {str(e)}"

# if __name__=="__main__":
#     print(translate_text("please translate this to french, how are you?"))