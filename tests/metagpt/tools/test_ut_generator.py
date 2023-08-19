#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/4/30 21:44
@Author  : alexanderwu
@File    : test_ut_generator.py
"""

from metagpt.const import API_QUESTIONS_PATH, SWAGGER_PATH, UT_PY_PATH
from metagpt.tools.ut_writer import YFT_PROMPT_PREFIX, UTGenerator


class TestUTWriter:
    def test_api_to_ut_sample(self):
        swagger_file = SWAGGER_PATH / "yft_swaggerApi.json"
        tags = ["test"]  # "Intelligent contract import", "Lawyer review", "AI contract review", "Drafting contracts & lawyer online review", "Contract approval", "Performance management", "Signing companies"]
        # Here, two test tags of API are manually added in the file

        utg = UTGenerator(swagger_file=swagger_file, ut_py_path=UT_PY_PATH, questions_path=API_QUESTIONS_PATH,
                          template_prefix=YFT_PROMPT_PREFIX)
        ret = utg.generate_ut(include_tags=tags)
        # Subsequent addition of verification for file content and quantity
        assert ret
