import pdfplumber, requests, re
from io import BytesIO


class Parser:

    def __init__(self, url):
        try:
            file_ = requests.get(url).content
            self.file = BytesIO(file_)
        except:
            raise ParserError("Can not load file.")

    def get_text(self):
        try:
            text = []
            string = ""
            with pdfplumber.open(self.file) as pdf:
                for page in pdf.pages:
                    string += " " + page.extract_text(x_tolerance=3, y_tolerance=3)
                    if len(string) > 7500:
                        string = re.sub(r"\(cid:\d*\)", '', string) # remove tables
                        string = re.sub(r'(?<=[a-zäöü])(?=[A-ZÄÖÜ][a-zäöü])', ' ', string) # split camel cased words
                        text.append(string)
                        string = ""

            string = re.sub(r"\(cid:\d*\)", '', string)
            string = re.sub(r'(?<=[a-zäöü])(?=[A-ZÄÖÜ][a-zäöü])', ' ', string)
            text.append(string)
        except Exception as e:
            raise ParserError(f"Failure on parsing: {e}")
        return text

    def get_size(self):
        return self.file.getbuffer().nbytes

    def get_pages(self):
        with pdfplumber.open(self.file) as pdf:
            pages = len(pdf.pages)

        return pages


class ParserError(Exception):
    pass

