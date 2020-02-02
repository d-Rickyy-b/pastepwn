# -*- coding: utf-8 -*-
from string import Template

from pastepwn.util import DictWrapper


class TemplatingEngine(object):
    """Wrapper class around the python templating feature"""

    @staticmethod
    def fill_template(paste, analyzer_name, template_string, **kwargs):
        """
        Returns a templated text with paste contents inserted into the template string
        Use ${key_name} in the template_string to insert paste contents into it
        :param paste: A paste which serves as the source for template filling
        :param analyzer_name: Name of the analyzer
        :param template_string: A template string describing how the variables should be filled in
        :return: Filled template
        """

        paste_dict = paste.to_dict()
        paste_dict["analyzer_name"] = analyzer_name

        # Possibility to insert own/custom values into the paste_dict thus gives more control over the template string
        for name, value in kwargs.items():
            paste_dict[name] = value

        # Fallback if the template string is empty or non existent
        if template_string is None or template_string == "":
            template_string = "New paste matched by analyzer '${analyzer_name}' - Link: ${full_url}"

        template = Template(template_string)
        text = template.safe_substitute(DictWrapper(paste_dict))
        return text
