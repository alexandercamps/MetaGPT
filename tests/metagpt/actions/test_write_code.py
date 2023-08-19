#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 17:45
@Author  : alexanderwu
@File    : test_write_code.py
"""
import pytest

from metagpt.actions.write_code import WriteCode
from metagpt.llm import LLM
from metagpt.logs import logger
from tests.metagpt.actions.mock import TASKS_2, WRITE_CODE_PROMPT_SAMPLE


@pytest.mark.asyncio
async def test_write_code():
    api_design = "Design a function named 'add' that takes two integers as input and returns their sum."
    write_code = WriteCode("write_code")

    code = await write_code.run(api_design)
    logger.info(code)

    # We can't precisely predict the generated code, but we can check for certain keywords
    assert 'def add' in code
    assert 'return' in code


@pytest.mark.asyncio
async def test_write_code_directly():
    prompt = WRITE_CODE_PROMPT_SAMPLE + '\n' + TASKS_2[0]
    llm = LLM()
    rsp = await llm.aask(prompt)
    logger.info(rsp)
