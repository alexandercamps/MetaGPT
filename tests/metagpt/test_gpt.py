#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/4/29 19:47
@Author  : alexanderwu
@File    : test_gpt.py
"""

import pytest

from metagpt.logs import logger


@pytest.mark.usefixtures("llm_api")
class TestGPT:
    def test_llm_api_ask(self, llm_api):
        answer = llm_api.ask('hello chatgpt')
        assert len(answer) > 0

    # def test_gptapi_ask_batch(self, llm_api):
    #     answer = llm_api.ask_batch(['Please act as a Google Python expert engineer, reply clearly if you understand', 'Write a hello world'])
    #     assert len(answer) > 0

    def test_llm_api_ask_code(self, llm_api):
        answer = llm_api.ask_code(['Please act as a Google Python expert engineer, reply clearly if you understand', 'Write a hello world'])
        assert len(answer) > 0

    @pytest.mark.asyncio
    async def test_llm_api_aask(self, llm_api):
        answer = await llm_api.aask('hello chatgpt')
        assert len(answer) > 0

    @pytest.mark.asyncio
    async def test_llm_api_aask_code(self, llm_api):
        answer = await llm_api.aask_code(['Please act as a Google Python expert engineer, reply clearly if you understand', 'Write a hello world'])
        assert len(answer) > 0

    @pytest.mark.asyncio
    async def test_llm_api_costs(self, llm_api):
        await llm_api.aask('hello chatgpt')
        costs = llm_api.get_costs()
        logger.info(costs)
        assert costs.total_cost > 0
