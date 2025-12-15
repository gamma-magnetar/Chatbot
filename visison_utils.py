import fitz
import base64
from openai import OpenAI

client = OpenAI()

def extract_vision_descriptions(pdf_path):
    doc = fitz.open(pdf_path)
    descriptions = ""

    for page_num, page in enumerate(doc): # type: ignore
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")
        img_base64 = base64.b64encode(img_bytes).decode()

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Describe the slide in detail. "
                                "If there are charts, explain trends, comparisons, "
                                "and key insights. Do NOT hallucinate numbers."
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_base64}"
                            },
                        },
                    ],
                }
            ],
            temperature=0,
        )

        descriptions += f"\n--- Slide {page_num + 1} (Vision Summary) ---\n"
        if response.choices[0].message.content:
            descriptions += response.choices[0].message.content

    return descriptions
