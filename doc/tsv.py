from __future__ import annotations
from genericpath import exists
from io import TextIOWrapper
from typing import *
from collections.abc import Iterable
from user.cheatsheet.doc.abc import *
import pathlib
import os

import pprint


_latex_special_chars = {
    '{': r'\{',
    '}': r'\}',
    '\\': r'\textbackslash{}',
    '&': r'\&',
    '%': r'\%',
    '$': r'\$',
    '#': r'\#',
    '_': r'\_',
    '~': r'\textasciitilde{}',
    '^': r'\^{}',
    '\n': '\\newline%\n',
    '-': r'{-}',
    '\xA0': '~',  # Non-breaking space
    '[': r'{[}',
    ']': r'{]}',
    '<': r'$<$',
    '>': r'$>$',

}


def latex_escape(text: str) -> str:
    """
    Escape the text so that it can be used in a LaTeX document.
    @param text - the text to be escaped           
    @return the escaped text
    """
    for key,value in  _latex_special_chars.items():
        text = text.replace(key, value)


    return text

def file_name_escape(text: str) -> str:
    return ((text))

def tsv_escape(text: str) -> str:
    return (latex_escape(text))


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


class TsvItem(Row):
    def __init__(self, file: TextIOWrapper, **kwargs):
        self.file = file
        self.kwargs = kwargs
        
    def __enter__(self) -> TsvItem:
        self.file.write(f"")
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.file.write(f"\n")

    def cell(self, contents: str, type:str, **kwargs):
        self.file.write(f"{{ {tsv_escape(contents)} }}\t")


class TsvList(Table):
    def __init__(self, sec_dir: pathlib.Path, file: TextIOWrapper, section:str, **kwargs):
        self.kwargs = kwargs
        self.section = section
        self.list_file = file
        self.file_path = sec_dir / (file_name_escape(self.kwargs['title']) + ".tsv")
        self.file =  open(self.file_path, "w")

    def __enter__(self) -> TsvList:
        # self.file.write(f"<table>\n")
        self.list_file.write(f"\processseparatedfile[MyTable][tsv_dir/{self.section}/{tsv_escape(self.kwargs['title'])}.tsv]\n\n")
        self.file.write(f"Command\tResult\n")
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.file.close()
        tmp_lines = []
        with open(self.file_path, "r") as f:
            for line in f:
                tmp_lines.append(line.strip())
        with open(self.file_path, "w") as f:
            for line in tmp_lines:
                f.write(f"{line}\n")

    def row(self, **kwargs) -> TsvItem:
        return TsvItem(self.file, **kwargs)


class TsvSection(Section):
    def __init__(self, parrent_dir: pathlib.Path, file: TextIOWrapper, **kwargs):
        self.kwargs = kwargs
        self.name = attr_class(self.kwargs)
        self.file=file
        self.sec_dir = parrent_dir / pathlib.Path(self.name)
        pathlib.Path(self.sec_dir).mkdir(parents=True, exist_ok=True)


    def __enter__(self) -> TsvSection:
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        # self.file.write(f"</section>\n")
        pass

    def table(self, **kwargs) -> TsvList:
        return TsvList(self.sec_dir, file = self.file, section=self.name,**kwargs)


class TsvDoc(Doc):
    # class TsvDoc(Doc):   
    def __init__(self, file_path:str,dir_path: str, **kwargs):
        self.dir_path = pathlib.Path(dir_path)
        pathlib.Path(self.dir_path).mkdir(parents=True, exist_ok=True)
        self.file = open(file_path, "w")
        self.kwargs = kwargs

    def __enter__(self) -> TsvDoc:
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.file.close()
        pass

    def section(self, **kwargs) -> TsvSection:
        return TsvSection(self.dir_path, file=self.file, **kwargs)
