from talon import Module, actions, registry
from typing import *
from user.cheatsheet.doc.dict import DictDoc
from user.cheatsheet.doc.html import HtmlDoc
from user.cheatsheet.doc.tex import TeXDoc
from user.cheatsheet.doc.xml import XmlDoc
from user.cheatsheet.doc.json import JsonDoc
from user.cheatsheet.doc.tsv import TsvDoc

import os
import re
import sys

mod = Module()

list_to_include = [
                    "user.letter",
                    "user.number_key",
                    "user.modifier_key",
                    "user.special_key",
                    "user.symbol_key",
                    "user.arrow_key",
                    "user.punctuation",
                    "user.function_key",
                    "user.abbreviation",
                    "user.window_snap_positions",
                    "user.cursorless_simple_action",  
                    "user.cursorless_callback_action",
                    "user.cursorless_makeshift_action",
                    "user.cursorless_scope_type",
                    "user.cursorless_hat_color",
                ]
@mod.action_class
class CheatSheetActions:
    def print_cheatsheet(format: str):
        """
        Print out a help document of all Talon commands as <format>

        Args:
            format: The format for the help document. Must be 'HTML' or 'TeX'.
        """
        this_dir = os.path.dirname(os.path.realpath(__file__))

        if format.lower() == "html":
            doc = HtmlDoc(
                file_path=os.path.join(this_dir, "cheatsheet.html"),
                title="Talon Cheatsheet",
                css_include_path=os.path.join(this_dir, "style.css"),
            )

        if format.lower() == "html-dev":
            doc = HtmlDoc(
                file_path=os.path.join(this_dir, "cheatsheet-dev.html"),
                title="Talon Cheatsheet",
                css_href="style.sass",
            )

        if format.lower() == "tex":
            doc = TeXDoc(
                file_path=os.path.join(this_dir, "cheatsheet.tex"),
                title="Talon Cheatsheet",
                preamble_path="preamble.tex",
            )
        if format.lower() == "xml":
            doc = XmlDoc(
                file_path=os.path.join(this_dir, "cheatsheet.xml"),
                title="Talon Cheatsheet",
            )

        if format.lower() == "json":
            doc = JsonDoc(
                file_path=os.path.join(this_dir, "cheatsheet.json"),
                title="Talon Cheatsheet",
            )   
        if format.lower() == "dict":
            doc = DictDoc(
                file_path=os.path.join(this_dir, "cheatsheet.dict.json"),
                title="Talon Cheatsheet",
            )   

        if format.lower() == "tsv":
            doc = TsvDoc(
                dir_path=os.path.join(this_dir, "tsv_dir"),
                file_path=os.path.join(this_dir, "tsv_list.tex"),
                title="Talon Cheatsheet",
            )   

        with doc:
            with doc.section(cols=2, css_classes="talon-lists") as sec:
#                sec.list(
#                    list_name="user.symbol_key",
#                )
                for talon_list_name, talon_list in registry.lists.items():
                    print("----------------------------------------------------\n")
                    print("length: " + str(len(talon_list[0])))
                    if len(talon_list[0]) < 100 :
                        if "user" in talon_list_name:
                            sec.list(list_name=talon_list_name)
            with doc.section(cols=2, css_classes="talon-captures") as sec:
#                sec.list(
#                    list_name="user.symbol_key",
#                )
                for talon_capture_name, talon_capture in registry.captures.items():
                    if "user" in talon_capture_name:
                        name = str(talon_capture_name)
                        sec.capture(capture_name=name)
            with doc.section(cols=2, css_classes="talon-formatters") as sec:
                sec.formatters(
                    list_names=(
                        "user.formatter_code",
                        "user.formatter_prose",
                        "user.formatter_word",
                    ),
                    formatted_text=actions.user.format_text,
                )
            with doc.section(cols=2, css_classes="talon-contexts") as sec:
                for context_name, context in registry.contexts.items():
                    if not "personal" in context_name:
                        sec.context(context, context_name=context_name)
