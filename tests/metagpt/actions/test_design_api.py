#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 19:26
@Author  : alexanderwu
@File    : test_design_api.py
"""
import pytest

from metagpt.actions.design_api import WriteDesign
from metagpt.logs import logger
from tests.metagpt.actions.mock import PRD_SAMPLE


@pytest.mark.asyncio
async def test_design_api():
    prd = "We need a music player, it should have play, pause, previous track, next track, etc. functions."

    design_api = WriteDesign("design_api")

    result = await design_api.run(prd)
    logger.info(result)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_design_api_calculator():
    prd = PRD_SAMPLE

    design_api = WriteDesign("design_api")
    result = await design_api.run(prd)
    logger.info(result)

    assert len(result) > 10
