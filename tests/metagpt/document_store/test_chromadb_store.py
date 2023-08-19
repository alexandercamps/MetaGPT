#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/6/6 00:41
@Author  : alexanderwu
@File    : test_chromadb_store.py
"""
from metagpt.document_store.chromadb_store import ChromaStore


# @pytest.mark.skip()
def test_chroma_store():
    """FIXME: The use of chroma feels very strange, and it hangs when using Python, and also in test cases"""
    # Create a ChromaStore instance, using the 'sample_collection' collection
    document_store = ChromaStore('sample_collection_1')

    # Use the write method to add multiple documents
    document_store.write(["This is document1", "This is document2"],
                [{"source": "google-docs"}, {"source": "notion"}],
                ["doc1", "doc2"])

    # Use the add method to add a single document
    document_store.add("This is document3", {"source": "notion"}, "doc3")

    # Search for documents
    results = document_store.search("This is a query document", n_results=3)
    assert len(results) > 0
