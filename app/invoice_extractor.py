from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from PIL import Image
import re
# Function to perform OCR on an image using Doctr
def perform_ocr(image_path):

    # Load the OCR model
    model = ocr_predictor(pretrained=True)

    # Load the document (assuming it's an image file, not a PDF)
    doc = DocumentFile.from_images([image_path])

    # Analyze the document with the OCR model
    result = model(doc)
    words = ""
    for page in result.pages:
        for block in page.blocks:
            for line in block.lines:
                for word in line.words:
                    words+=" "+word.value
    return words
def get_data_regex(text):
   
      nom_vendeur_search = re.search(r".* \d+:\d+:\d+ (.*?)(?: \d{5}| \d+/\d+/\d+ \d+:\d+:\d+|$)", text)
      nom_vendeur = nom_vendeur_search.group(1) if nom_vendeur_search else "not found"
        
      date_search = re.search(r"(\d+/\d+/\d+)", text)
      date = date_search.group(1) if date_search else "not found"
        
      heure_search = re.search(r"(\d+:\d+:\d+)", text)
      heure = heure_search.group(1) if heure_search else "not found"
        
      montant_search = re.search(r"(\d+,\d+) EUR", text)
      montant = montant_search.group(1) if montant_search else "not found"
      return {"vendor_name":nom_vendeur,"Date":date,"Time":heure,"Amount":montant}
