from __future__ import annotations
from contextlib import AbstractContextManager
from talon import actions, registry
from talon.scripting.context import Context  # type: ignore
from typing import *
from user.cheatsheet.doc.talon_script.describe import Describe
import re

# Abstract classes for printing cheatsheet document

class Row(AbstractContextManager):
    def cell(self, contents: str, type:str **kwargs):
        """
        Writes a cell to the row.
        """


class Table(AbstractContextManager):
    def row(self, **kwargs) -> Row:
        """
        Creates a row.
        """


class Section(AbstractContextManager):
    def table(self, title: str, **kwargs) -> Table:
        """Creates a table with <cols> columns."""

    def list(self, list_name: str, **kwargs) -> None:
        """
        Create a table for a Talon list.
        """
        """
        Create a table for a Talon list.

        Args:
            list_name: The name of the list.
            **table_title: The table title.
        """

        # Set the default title based on the list name:
        kwargs["title"] = kwargs.get("title", list_name) + " list"

        with self.table(cols=2, **kwargs) as table:
            for key, value in registry.lists[list_name][0].items():
                with table.row(**kwargs) as row:
                    # kwargs["type"] = 'spoken'
                    row.cell(key, type='spoken', **kwargs)
                    row.cell(value, type='action',**kwargs)

    
    def capture(self, capture_name: str, **kwargs) -> None:
        """
        Create a table for a Talon capture.

        Args:
            capture_name: The name of the capture.
            **table_title: The table title.
        """

        # Set the default title based on the capture name:
        kwargs["title"] = kwargs.get("title", capture_name) + " capture"

        with self.table(cols=2, **kwargs) as table:
            with table.row(**kwargs) as row:
                row.cell(capture_name,type='spoken' ,**kwargs)
                capture_pattern = str(registry.captures[capture_name][0])
                print("**************************************")
                print(capture_pattern)
                
                # if re.search(r'<(?!user|self)([^>^\s]+)>', capture_pattern):
                #     capture_pattern = re.sub(r'<(?!user|self)([^>^\s]+)>', r' &lt;\1&gt;  ', capture_pattern)
                    
                # if re.search(r'<user.([^>^\s]+)>', capture_pattern):
                #     print(capture_pattern)
                #     capture_pattern = re.sub(r'<user.([^>]+)>', r' <a href="#user-\1_capture"> &lt;user.\1&gt; </a> ', capture_pattern)
                #     print(capture_pattern)
                    
                # if re.search(r'<self.([^>^\s]+)>', capture_pattern):
                #     print(capture_pattern)
                #     capture_pattern = re.sub(r'<self.([^>]+)>', r' <a href="#user-\1_capture"> &lt;self.\1&gt; </a> ', capture_pattern)
                #     print(capture_pattern)
                
                # if re.search(r'{user.([^}^\s]+)}', capture_pattern):
                #     print(capture_pattern)
                #     capture_pattern = re.sub(r'{user.([^}^\s]+)}', r'<a href="#user-\1_list">  {user.\1}  </a>', capture_pattern)
                #     print(capture_pattern)
                
                # if re.search(r'{self.([^}^\s]+)}', capture_pattern):
                #     print(capture_pattern)
                #     capture_pattern = re.sub(r'{self.([^}^\s]+)}', r'<a href="#user-\1_list">  {self.\1}  </a>', capture_pattern)
                #     print(capture_pattern)
                
                final_string = capture_pattern.replace("_", "-") ## this replacement makes the links work but also replaces the underscores in the display name, making them incorrect.
                final_string_1 = final_string.replace("|", " | ")
                row.cell(final_string_1, type='action',**kwargs)

    def formatters(self, **kwargs) -> None:
        """
        """
        """
        Create table for the talon formatters list.

        Args:
            **list_names: The names of the formatters lists. Defaults to 'user.formatters'.
            **formatted_text: The name of the formatter function. Defaults to 'actions.user.formatted_text'.
            **table_title: The table title.
            **context_name: The Talon context name. Used to generate the table title if the **table_title keyword is not given.
        """

        # Set the default list name and formatting function:
        list_names = kwargs.get("list_names", ("user.formatters",))
        formatted_text = kwargs.get("formatted_text", actions.user.formatted_text)
        for list_name in list_names:
            with self.table(cols=2, title=list_name, **kwargs) as table:
                if list_name in registry.lists:
                    items = registry.lists[list_name]
                    if isinstance(items, list):
                        items = items[0]
                    for key, val in items.items():
                        with table.row(**kwargs) as row:
                            example = formatted_text(f"example of formatting with {key}", val)
                            # kwargs["type"] = 'spoken'
                            row.cell(key, type="spoken",**kwargs)
                            row.cell(example,type="action" **kwargs)

    def context(self, context: Context, **kwargs) -> None:
        """
        Write each command and its implementation as a table.

        Args:
            context: The Talon context object.
            **table_title: The table title.
            **context_name: The Talon context name. Used to generate the table title if the **table_title keyword is not given.
        """
        if context.commands:
            # Set the default context name:
            # Set the default table title based on the context name:
            if 'context_name' in kwargs:
                kwargs["title"] = kwargs.get("title", \
                    Describe.context_name(kwargs["context_name"]))

            # Create table to describe context:
            with self.table(cols=2, **kwargs) as table:
                for command in context.commands.values():
                    with table.row(**kwargs) as row:
                        # kwargs["type"] = 'spoken'
                        row.cell(Describe.command_rule(command), non_breaking=True, type='spoken', **kwargs)
                        docs = Describe.command(command)
                        impl = Describe.command_impl(command)
                        # kwargs["type"] = 'action'
                        if docs is not None:
                            row.cell(docs, type='action', **kwargs)
                        else:
                            row.cell(impl, css_classes='talon-script',  type='action',**kwargs)
        else:
            pass


class Doc(AbstractContextManager):
    def section(self, **kwargs) -> Section:
        """
        Create a new section.

        Args:
            **section_title: The section title.
        """
