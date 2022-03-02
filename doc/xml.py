from __future__ import annotations
from io import TextIOWrapper
from typing import *
from collections.abc import Iterable
from user.cheatsheet.doc.abc import *
import os


def xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "\n<br />\n")
    )


def attr_class(kwargs) -> str:
    css_classes = kwargs.get("css_classes", [])
    if isinstance(css_classes, str):
        css_classes = [css_classes]
    elif isinstance(css_classes, Iterable):
        css_classes = list(css_classes)
    if "cols" in kwargs:
        css_classes.append(f"columns-{kwargs['cols']}")
    if css_classes:
        css_classes = " ".join(css_classes)
        css_classes = f' class="{css_classes}"'
        return css_classes
    else:
        return ""


def attr_colspan(kwargs) -> str:
    if "cols" in kwargs:
        return f" colspan=\"{kwargs['cols']}\""
    else:
        return ""


class XmlItem(Row):
    def __init__(self, file: TextIOWrapper, **kwargs):
        self.file = file
        self.kwargs = kwargs

    def __enter__(self) -> XmlItem:
        self.file.write(f"<item>\n")
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.file.write(f"</item>\n")

    def cell(self, contents: str, type:str, **kwargs):
        self.file.write(f"<{xml_escape(type)}>{xml_escape(contents)}</{xml_escape(type)}>\n")


class XmlList(Table):
    def __init__(self, file: TextIOWrapper, **kwargs):
        self.file = file
        self.kwargs = kwargs

    def __enter__(self) -> XmlList:
        self.file.write(f"<item>\n")

        if "title" in self.kwargs:
            self.file.write(
                f"<Title>{xml_escape(self.kwargs['title'])}</Title>\n"
            )

        self.file.write(f"<list>\n")
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.file.write(f"</list>")
        self.file.write(f"</item>")
        # self.file.write(f"</div>")

    def row(self, **kwargs) -> XmlItem:
        return XmlItem(self.file, **kwargs)


class XmlSection(Section):
    def __init__(self, file: TextIOWrapper, **kwargs):
        self.file = file
        self.kwargs = kwargs

    def __enter__(self) -> XmlSection:
        if "title" in self.kwargs:
            self.file.write(f"<h1>{xml_escape(self.kwargs['title'])}</h1>\n")
        self.file.write(f"<section{attr_class(self.kwargs)}>\n")
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.file.write(f"</section>\n")

    def table(self, **kwargs) -> XmlList:
        return XmlList(self.file, **kwargs)


class XmlDoc(Doc):
    # class XmlDoc(Doc):   
    def __init__(self, file_path: str, **kwargs):
        self.file = open(file_path, "w")
        self.kwargs = kwargs

    def __enter__(self) -> XmlDoc:
        # self.file.write(f"<!doctype xml>\n")
        # self.file.write(f'<xml lang="en">\n')
        # self.file.write(f"<head>\n")
        # self.file.write(f'<meta charset="utf-8">\n')

        # Use **title as the document title:
        # if "title" in self.kwargs:
        #     self.file.write(f"<title>{xml_escape(self.kwargs['title'])}</title>\n")

    
        # self.file.write(f"</head>\n")
        # self.file.write(f"<body>\n")
        # self.file.write(f"<main>\n")
        self.file.write(f"<list>\n")
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        # self.file.write(f"</main>\n")
        # self.file.write(f"</body>\n")
        # self.file.write(f"</xml>\n")
        self.file.write(f"</list>\n")
        self.file.close()

    def section(self, **kwargs) -> XmlSection:
        return XmlSection(self.file, **kwargs)
