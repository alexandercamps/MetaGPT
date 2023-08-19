#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/1 22:50
@Author  : alexanderwu
@File    : test_azure_tts.py
"""
from metagpt.actions.azure_tts import AzureTTS


def test_azure_tts():
    azure_tts = AzureTTS("azure_tts")
    azure_tts.synthesize_speech(
        "zh-CN",
        "zh-CN-YunxiNeural",
        "Boy",
        "Hello, I am Kaka",
        "output.wav")

    # You need to configure SUBSCRIPTION_KEY to run
    # TODO: If you want to verify here, you also need to add the corresponding ASR, to ensure that the generation before and after is almost consistent, but not yet
