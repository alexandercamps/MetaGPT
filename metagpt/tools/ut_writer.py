#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pathlib import Path

from metagpt.provider.openai_api import OpenAIGPTAPI as GPTAPI

ICL_SAMPLE = '''Interface definition:
```text
Interface name: Tag elements
Interface path: /projects/{project_key}/node-tags
Method: POST

Request parameters:
Path parameters:
project_key

Body parameters:
Name	Type	Mandatory	Default value	Remarks
nodes	array	Yes		Nodes
	node_key	string	No		Node key
	tags	array	No		Original tag list of the node
	node_type	string	No		Node type DATASET / RECIPE
operations	array	Yes		
	tags	array	No		Operation tag list
	mode	string	No		Operation type ADD / DELETE

Returned data:
Name	Type	Mandatory	Default value	Remarks
code	integer	Yes		Status code
msg	string	Yes		Prompt message
data	object	Yes		Returned data
list	array	No		Node list true / false
node_type	string	No		Node type	DATASET / RECIPE
node_key	string	No		Node key
"""

Unit text:
```python
@pytest.mark.parametrize(
"project_key, nodes, operations, expected_msg",
[
("project_key", [{"node_key": "dataset_001", "tags": ["tag1", "tag2"], "node_type": "DATASET"}], [{"tags": ["new_tag1"], "mode": "ADD"}], "success"),
("project_key", [{"node_key": "dataset_002", "tags": ["tag1", "tag2"], "node_type": "DATASET"}], [{"tags": ["tag1"], "mode": "DELETE"}], "success"),
("", [{"node_key": "dataset_001", "tags": ["tag1", "tag2"], "node_type": "DATASET"}], [{"tags": ["new_tag1"], "mode": "ADD"}], "missing necessary parameter project_key"),
(123, [{"node_key": "dataset_001", "tags": ["tag1", "tag2"], "node_type": "DATASET"}], [{"tags": ["new_tag1"], "mode": "ADD"}], "incorrect parameter type"),
("project_key", [{"node_key": "a"*201, "tags": ["tag1", "tag2"], "node_type": "DATASET"}], [{"tags": ["new_tag1"], "mode": "ADD"}], "request parameter exceeds field boundary")
]
)
def test_node_tags(project_key, nodes, operations, expected_msg):
    pass
```
The above is an example of interface definition and unit testing.
Next, please play the role of a Google expert test manager with 20 years of experience. After I provide the interface definition, respond to me with the unit tests. There are a few requirements:
1. Only output one `@pytest.mark.parametrize` and the corresponding test_<interface_name> function (internal pass, not implemented)
   -- Include expected_msg in the function parameters for result verification
2. Use shorter text or numbers for the generated test cases, and make them as compact as possible
3. If comments are needed, use English

If you understand, please wait for me to provide the interface definition and only reply with "understand" to save tokens.

'''

ACT_PROMPT_PREFIX = '''Reference test types: such as missing request parameters, field boundary verification, incorrect field types
Please output 10 test cases within the scope of `@pytest.mark.parametrize`
```text
'''

YFT_PROMPT_PREFIX = '''Reference test types: such as SQL injection, cross-site scripting (XSS), illegal access and unauthorized access, authentication and authorization, parameter validation, exception handling, file upload and download
Please output 10 test cases within the scope of `@pytest.mark.parametrize`
```text
'''

OCR_API_DOC = '''```text
Interface name: OCR Recognition
Interface path: /api/v1/contract/treaty/task/ocr
Method: POST
Request parameters:
Path parameters:
Body parameters:
Name      Type     Required   Default Value   Remarks
file_id   string   Yes       
box       array    Yes       
contract_id number Yes        Contract id
start_time string  No         yyyy-mm-dd
end_time   string  No         yyyy-mm-dd
extract_type number No        Recognition type 1-In import 2-After import Default 1
Return data:
Name      Type     Required   Default Value   Remarks
code      integer  Yes       
message   string   Yes       
data      object   Yes       
```
'''


class UTGenerator:
    """UT Generator: Construct UT through API documentation"""

    def __init__(self, swagger_file: str, ut_py_path: str, questions_path: str,
                 chatgpt_method: str = "API", template_prefix=YFT_PROMPT_PREFIX) -> None:
        """Initialize UT generator

        Args:
            swagger_file: Swagger path
            ut_py_path: Path to store the test cases
            questions_path: Path to store templates, convenient for subsequent investigation
            chatgpt_method: API
            template_prefix: Use the template, the default is YFT_UT_PROMPT
        """
        self.swagger_file = swagger_file
        self.ut_py_path = ut_py_path
        self.questions_path = questions_path
        assert chatgpt_method in ["API"], "Illegal chatgpt_method"
        self.chatgpt_method = chatgpt_method

        # ICL: In-Context Learning, here's an example, GPT is asked to imitate the example
        self.icl_sample = ICL_SAMPLE
        self.template_prefix = template_prefix

    def get_swagger_json(self) -> dict:
        """Load Swagger JSON from local file"""
        with open(self.swagger_file, "r", encoding="utf-8") as file:
            swagger_json = json.load(file)
        return swagger_json

    def __para_to_str(self, prop, required, name=""):
        name = name or prop["name"]
        ptype = prop["type"]
        title = prop.get("title", "")
        desc = prop.get("description", "")
        return f'{name}\t{ptype}\t{"Yes" if required else "No"}\t{title}\t{desc}'

    def _para_to_str(self, prop):
        required = prop.get("required", False)
        return self.__para_to_str(prop, required)

    def para_to_str(self, name, prop, prop_object_required):
        required = name in prop_object_required
        return self.__para_to_str(prop, required, name)

    def build_object_properties(self, node, prop_object_required, level: int = 0) -> str:
        """Recursively output the sub-properties of object and array[object] types

        Args:
            node (_type_): Value of the sub-item
            prop_object_required (_type_): Whether it is a required field
            level: Current recursion depth
        """

        doc = ""

        def dive_into_object(node):
            """If it is an object type, recursively output sub-properties"""
            if node.get("type") == "object":
                sub_properties = node.get("properties", {})
                return self.build_object_properties(sub_properties, prop_object_required, level=level + 1)
            return ""

        if node.get("in", "") in ["query", "header", "formData"]:
            doc += f'{"\t" * level}{self._para_to_str(node)}\n'
            doc += dive_into_object(node)
            return doc

        for name, prop in node.items():
            doc += f'{"\t" * level}{self.para_to_str(name, prop, prop_object_required)}\n'
            doc += dive_into_object(prop)
            if prop["type"] == "array":
                items = prop.get("items", {})
                doc += dive_into_object(items)
        return doc

    def get_tags_mapping(self) -> dict:
        """Handle tag and path

        Returns:
            Dict: Corresponding relationship between tag and path
        """
        swagger_data = self.get_swagger_json()
        paths = swagger_data["paths"]
        tags = {}

        for path, path_obj in paths.items():
            for method, method_obj in path_obj.items():
                for tag in method_obj["tags"]:
                    if tag not in tags:
                        tags[tag] = {}
                    if path not in tags[tag]:
                        tags[tag][path] = {}
                    tags[tag][path][method] = method_obj

        return tags

    def generate_ut(self, include_tags) -> bool:
        """Generate test case files"""
        tags = self.get_tags_mapping()
        for tag, paths in tags.items():
            if include_tags is None or tag in include_tags:
                self._generate_ut(tag, paths)
        return True

    def build_api_doc(self, node: dict, path: str, method: str) -> str:
        summary = node["summary"]

        doc = f"Interface name: {summary}\nInterface path: {path}\nMethod: {method.upper()}\n"
        doc += "\nRequest parameters:\n"
        if "parameters" in node:
            parameters = node["parameters"]
            doc += "Path parameters:\n"

            # param["in"]: path / formData / body / query / header
            for param in parameters:
                if param["in"] == "path":
                    doc += f'{param["name"]} \n'

            doc += "\nBody parameters:\n"
            doc += "Name\tType\tRequired\tDefault Value\tRemarks\n"
            for param in parameters:
                if param["in"] == "body":
                    schema = param.get("schema", {})
                    prop_properties = schema.get("properties", {})
                    prop_required = schema.get("required", [])
                    doc += self.build_object_properties(prop_properties, prop_required)
                else:
                    doc += self.build_object_properties(param, [])

        # Output return data information
        doc += "\nReturn data:\n"
        doc += "Name\tType\tRequired\tDefault Value\tRemarks\n"
        responses = node["responses"]
        response = responses.get("200", {})
        schema = response.get("schema", {})
        properties = schema.get("properties", {})
        required = schema.get("required", {})

        doc += self.build_object_properties(properties, required)
        doc += "\n"
        doc += "```"

        return doc

    def _store(self, data, base, folder, fname):
        file_path = self.get_file_path(Path(base) / folder, fname)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(data)

    def ask_gpt_and_save(self, question: str, tag: str, fname: str):
        """Generate question and store question and answer"""
        messages = [self.icl_sample, question]
        result = self.gpt_msgs_to_code(messages=messages)

        self._store(question, self.questions_path, tag, f"{fname}.txt")
        self._store(result, self.ut_py_path, tag, f"{fname}.py")

    def _generate_ut(self, tag, paths):
        """Process the structure under the data path

        Args:
            tag (_type_): Module name
            paths (_type_): Path Object
        """
        for path, path_obj in paths.items():
            for method, node in path_obj.items():
                summary = node["summary"]
                question = self.template_prefix
                question += self.build_api_doc(node, path, method)
                self.ask_gpt_and_save(question, tag, summary)

    def gpt_msgs_to_code(self, messages: list) -> str:
        """Choose according to different call methods"""
        result = ''
        if self.chatgpt_method == "API":
            result = GPTAPI().ask_code(msgs=messages)

        return result

    def get_file_path(self, base: Path, fname: str):
        """Save different file paths

        Args:
            base (str): Path
            fname (str): File name
        """
        path = Path(base)
        path.mkdir(parents=True, exist_ok=True)
        file_path = path / fname
        return str(file_path)
