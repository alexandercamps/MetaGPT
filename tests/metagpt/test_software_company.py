#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/15 11:40
@Author  : alexanderwu
@File    : test_software_company.py
"""
import pytest

from metagpt.logs import logger
from metagpt.software_company import SoftwareCompany


@pytest.mark.asyncio
async def test_software_company():
    company = SoftwareCompany()
    company.start_project("Build a basic search engine that can support a knowledge base")
    history = await company.run(n_round=5)
    logger.info(history)
