#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/2 17:46
@Author  : alexanderwu
@File    : test_prompt_generator.py
"""

import pytest

from metagpt.logs import logger
from metagpt.tools.prompt_writer import (
    BEAGECTemplate,
    EnronTemplate,
    GPTPromptGenerator,
    WikiHowTemplate,
)


@pytest.mark.usefixtures("llm_api")
def test_gpt_prompt_generator(llm_api):
    generator = GPTPromptGenerator()
    example = "Product Name:WonderLab New Skin Fruit Flavor Meal Replacement Milkshake Small Fat Bottle Collagen Upgraded Version Satiety Meal Replacement Powder 6 Bottles 75g/Bottle (6 Bottles/Box) Store Name:Jinlinning Food Specialty Store " \
              "Brand:WonderLab Shelf Life:1 year Origin:China Net Content:450g"

    results = llm_api.ask_batch(generator.gen(example))
    logger.info(results)
    assert len(results) > 0


@pytest.mark.usefixtures("llm_api")
def test_wikihow_template(llm_api):
    template = WikiHowTemplate()
    question = "learn Python"
    step = 5

    results = template.gen(question, step)
    assert len(results) > 0
    assert any("Give me 5 steps to learn Python." in r for r in results)


@pytest.mark.usefixtures("llm_api")
def test_enron_template(llm_api):
    template = EnronTemplate()
    subj = "Meeting Agenda"

    results = template.gen(subj)
    assert len(results) > 0
    assert any("Write an email with the subject \"Meeting Agenda\"." in r for r in results)


def test_beagec_template():
    template = BEAGECTemplate()

    results = template.gen()
    assert len(results) > 0
    assert any("Edit and revise this document to improve its grammar, vocabulary, spelling, and style."
               in r for r in results)
