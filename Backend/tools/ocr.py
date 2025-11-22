from langchain.tools import tool
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import os

# Optional: for cleaning OCR text into readable sentences
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

@tool("ocr_image_reader", return_direct=True)
def ocr_read(image_path: str, use_llm: bool = True) -> str:
    """
    Reads text from ANY image, cleans it, and optionally converts it into readable sentences using an LLM.

    Args:
    - image_path (str): Path to the image.
    - use_llm (bool): If True, post-process OCR text into readable sentences via LLM.

    Returns:
    - str: Extracted and cleaned text.
    """

    # Expand ~ to full path
    image_path = os.path.expanduser(image_path)

    if not os.path.exists(image_path):
        return f"Image not found at: {image_path}"

    try:
        # --- Image preprocessing ---
        img = Image.open(image_path).convert('L')  # grayscale
        img = img.filter(ImageFilter.MedianFilter())  # reduce noise
        img = ImageEnhance.Contrast(img).enhance(2)  # increase contrast

        # --- OCR extraction ---
        text = pytesseract.image_to_string(img)

        if not text.strip():
            return "No readable text found in the image."

        # --- Clean common OCR errors ---
        text = (
            text.replace('|', 'I')
                .replace('0', 'O')
                .replace('1', 'I')
                .replace('\n', ' ')
        )

        # --- Optional: convert to natural sentences using LLM ---
        if use_llm:
            llm = ChatOpenAI(temperature=0)
            prompt = ChatPromptTemplate.from_template(
                "Turn the following OCR text into readable, natural sentences:\n{text}"
            )
            text = llm(prompt.format(text=text))

        return text.strip()

    except Exception as e:
        return f"Failed to extract text: {str(e)}"


# Standalone test
# if __name__=="__main__":
#     test_path = "/home/neemah/Pictures/js.jpeg"  # replace with your image
#     print(ocr_read(test_path))
