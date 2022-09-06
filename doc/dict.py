from __future__ import annotations
from io import TextIOWrapper
from typing import *
from collections.abc import Iterable
from user.cheatsheet.doc.abc import *
import os
import re
import json

from rich import inspect, print
from rich.console import Console
console = Console(color_system="256")


def Dict_escape(text: str) -> str:
    return ( text
        # re.sub(r"<user.([-\w]+)>", r"&ltuser.\1&gt", text.replace(r"<phrase>", r"&ltphrase&gt")
        # .replace(r"<number>", r"&ltnumber&gt")
        # .replace(r"<number_small>", r"&ltnumber_small&gt")
        # .replace("\n", "\n<br />\n"))
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

def attr_id(kwargs)->str:
    if "title" in kwargs:
        id = kwargs['title']
        # print(id)
        id=re.sub(r'[\(\)_,.?!\t\n ]+', '-', id)
        # print(id)
        return f" id=\"{id}\""
    else:
        return ""


class DictRow(Row):
    def __init__(self, table_list:List[dict] , **kwargs):
        self.kwargs = kwargs
        self.table_list = table_list
        
    def __enter__(self) -> DictRow:
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def cell(self, contents: str, type:str, **kwargs):
       
        if type == "action":
            item = self.table_list.pop()
            item["action"] = Dict_escape(contents)
            self.table_list.append(item)
        else:
            item = {Dict_escape(type) : Dict_escape(contents)}
            self.table_list.append(item)
        
        # print(f"{item=}")
            


class DictTable(Table):
    def __init__(self,sec_list :list, **kwargs):
        self.kwargs = kwargs
        self.sec_list = sec_list
        self.table_list = []

    def __enter__(self) -> DictTable:


        self.title = Dict_escape(self.kwargs['title'])

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.sec_list.append({
            "title": self.title, 
            "commands":self.table_list})

        # print(f"{self.table_list=}")
        

    def row(self, **kwargs) -> DictRow:
        return DictRow(self.table_list, **kwargs)


class DictSection(Section):
    def __init__(self, doc_dict: dict, **kwargs):
        self.kwargs = kwargs
        self.doc_dict = doc_dict
        # self.sec_dict = {}
        self.sec_list = []
        self.name = attr_class(self.kwargs)

    def __enter__(self) -> DictSection:
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        # print(f"{self.sec_dict=}")
        # if "css_classes" in self.kwargs:
        self.doc_dict[self.name] = self.sec_list
       


    def table(self, **kwargs) -> DictTable:

        return DictTable(self.sec_list, **kwargs)


class DictDoc(Doc):
    def __init__(self, file_path: str, **kwargs):
        self.file = open(file_path, "w")
        self.doc_dict = {}
        self.kwargs = kwargs

    def __enter__(self) -> DictDoc:
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        console.print(f"{self.doc_dict=}")
        
        self.file.write(json.dumps(self.doc_dict))
        self.file.close()

    def section(self, **kwargs) -> DictSection:
        # print(f"{self.doc_dict=}")
# 
        sec = DictSection(doc_dict = self.doc_dict, **kwargs)

        # print(f"{sec.sec_dict=}")

        return sec