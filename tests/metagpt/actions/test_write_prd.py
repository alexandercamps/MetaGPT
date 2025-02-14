#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 17:45
@Author  : alexanderwu
@File    : test_write_prd.py
"""
import pytest

from metagpt.actions import BossRequirement
from metagpt.logs import logger
from metagpt.roles.product_manager import ProductManager
from metagpt.schema import Message


@pytest.mark.asyncio
async def test_write_prd():
    product_manager = ProductManager()
    requirements = "Develop a search engine based on a large language model and a private knowledge base, hoping to perform search summarization based on a large language model"
    prd = await product_manager.handle(Message(content=requirements, cause_by=BossRequirement))
    logger.info(requirements)
    logger.info(prd)

    # Assert the prd is not None or empty
    assert prd is not None
    assert prd != ""
