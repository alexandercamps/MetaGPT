#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 17:45
@Author  : alexanderwu
@File    : test_write_code_review.py
"""
import pytest

from metagpt.actions.write_code_review import WriteCodeReview


@pytest.mark.asyncio
async def test_write_code_review(capfd):
    code = """
def add(a, b):
    return a + 
"""
    # write_code_review = WriteCodeReview("write_code_review")

    code = await WriteCodeReview().run(context="Write a function that adds a to b and returns a+b", code=code, filename="math.py")

    # We can't precisely predict the generated code review, but we can check if it is returned as a string
    assert isinstance(code, str)
    assert len(code) > 0

    captured = capfd.readouterr()
    print(f"Output content: {captured.out}")


# @pytest.mark.asyncio
# async def test_write_code_review_directly():
#     code = SEARCH_CODE_SAMPLE
#     write_code_review = WriteCodeReview("write_code_review")
#     review = await write_code_review.run(code)
#     logger.info(review)
