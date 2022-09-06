from __future__ import annotations
from io import SEEK_CUR, TextIOWrapper
from typing import *
from collections.abc import Iterable
from user.cheatsheet.doc.abc import *
import os
import re

def json_escape(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace('"', "\\\"")
        # .replace("\n", "\\n")
    )



def attr_class(kwargs) -> str:
    css_classes = kwargs.get("css_classes", [])
    if isinstance(css_classes, str):
        css_classes = [css_classes]
    elif isinstance(css_classes, Iterable):
        css_classes = list(css_classes)
    if css_classes:
        css_classes = " ".join(css_classes)
        css_classes = f'{css_classes}'
        return css_classes
    else:
        return ""


def attr_colspan(kwargs) -> str:
    if "cols" in kwargs:
        return f" colspan=\"{kwargs['cols']}\""
    else:
        return ""


class JsonItem(Row):
    def __init__(self, file: TextIOWrapper, **kwargs):
        self.file = file
        self.kwargs = kwargs

    def __enter__(self) -> JsonItem:
        self.file.write(f'')
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.file.write(f",\n")

    def cell(self, contents: str, type:str, **kwargs):
        if type == "spoken":
            self.file.write("\t\t\t{")
            

        self.file.write(f'"{json_escape(type)}" : "{json_escape(contents)}"')

        if type == "spoken":
            self.file.write(",")

        elif type == "action":
            self.file.write('}')


class JsonList(Table):
    def __init__(self, file: TextIOWrapper, **kwargs):
        self.file = file
        self.kwargs = kwargs

    def __enter__(self) -> JsonList:
        # self.file.write(f"<table>\n")

        if "title" in self.kwargs:
            self.file.write(
                f'\t\t"{json_escape(self.kwargs["title"])}": [\n'
            )
        else:
            self.file.write(f"\t[\n")


        # self.file.write(f"<list>\n")
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        # self.file.write(f"</list>")
        self.file.write(f"\n\t\t],\n")
        # self.file.write(f"</div>")

    def row(self, **kwargs) -> JsonItem:
        return JsonItem(self.file, **kwargs)


class JsonSection(Section):
    def __init__(self, file: TextIOWrapper, **kwargs):
        self.file = file
        self.kwargs = kwargs

    def __enter__(self) -> JsonSection:
        self.file.write(f'\t"{attr_class(self.kwargs)}" : {{\n')
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.file.write(f"\n}},\n")

    def table(self, **kwargs) -> JsonList:
        return JsonList(self.file, **kwargs)

    
class JsonDoc(Doc):
    # class JsonDoc(Doc):   
    def __init__(self, file_path: str, **kwargs):
        self.file = open(file_path, "w+")
        self.kwargs = kwargs

    def __enter__(self) -> JsonDoc:
        self.file.write(f"{{\n")
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.file.write(f"}}\n")
        self.file.close()

    def section(self, **kwargs) -> JsonSection:
        return JsonSection(self.file, **kwargs)
