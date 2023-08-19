#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 19:31
@Author  : alexanderwu
@File    : test_design_api_review.py
"""
import pytest

from metagpt.actions.design_api_review import DesignReview


@pytest.mark.asyncio
async def test_design_api_review():
    prd = "We need a music player, it should have play, pause, previous track, next track, etc. functions."
    api_design = """
Data structure:
1. Song: Contains song information, such as title, artist, etc.
2. Playlist: Contains a series of songs.

API list:
1. play(song: Song): Start playing the specified song.
2. pause(): Pause the currently playing song.
3. next(): Skip to the next song in the playlist.
4. previous(): Skip to the previous song in the playlist.
"""
    _ = "The API design looks very reasonable and meets all the requirements in the PRD."

    design_api_review = DesignReview("design_api_review")

    result = await design_api_review.run(prd, api_design)

    _ = f"The following is the Product Requirement Document (PRD):\n\n{prd}\n\nThe following is the API list designed based on this PRD:\n\n{api_design}\n\nPlease review whether this API design meets the PRD requirements and whether it complies with good design practices."
    # mock_llm.ask.assert_called_once_with(prompt)
    assert len(result) > 0
