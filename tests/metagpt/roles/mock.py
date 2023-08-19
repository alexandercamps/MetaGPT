#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/12 13:05
@Author  : alexanderwu
@File    : mock.py
"""
from metagpt.actions import BossRequirement, WriteDesign, WritePRD, WriteTasks
from metagpt.schema import Message

BOSS_REQUIREMENT = """Develop a search engine based on a large language model and private knowledge base, hoping to conduct searches and summaries based on a large language model"""

DETAIL_REQUIREMENT = """Requirements: Develop a search engine based on LLM (Large Language Model) and private knowledge base, with the following capabilities:
1. Users can search in the private knowledge base and then summarize based on the large language model, and the output includes the summary
2. The private knowledge base can be updated in real time, based on ElasticSearch
3. The private knowledge base supports various file formats such as pdf, word, txt, which can be parsed into text on the server after uploading and stored in ES

Resources:
1. The large language model already has a front-end abstraction and deployment, which can be directly called through `from metagpt.llm import LLM`, and then using `LLM().ask(prompt)`
2. Elastic is already [deployed](http://192.168.50.82:9200/), and the code can directly use this deployment"""

PRD = '''## Original Requirements
```python
"""
We hope to develop a search engine based on a large language model and private knowledge base. This search engine should be able to perform intelligent searches based on user input queries and summarize the search results based on the large language model, so that users can quickly obtain the information they need. The search engine should be able to handle large-scale data while maintaining the accuracy and relevance of the search results. We hope that this product can reduce users' workload in finding, filtering, and understanding information, and improve their work efficiency.
"""
```

## Product Goals
```python
[
    "Provide highly accurate and relevant search results to meet users' query needs",
    "Intelligently summarize search results based on a large language model to help users quickly obtain the required information",
    "Handle large-scale data, ensure the speed and efficiency of the search, and improve users' work efficiency"
]
```

## User Stories
```python
[
    "Assume the user is a researcher working on a report on global climate change. He enters 'Latest research on global climate change,' and our search engine quickly returns relevant articles, reports, datasets, etc., and intelligently summarizes this information using a large language model. The researcher can quickly understand the latest research trends and discoveries.",
    "The user is a student, revising for an upcoming history exam. He enters 'Main battles of World War II,' and the search engine returns relevant materials, and the large language model summarizes the main battles' time, location, results, and other key information, helping the student to memorize quickly.",
    "The user is an entrepreneur looking for information on the latest market trends. He enters '2023 Artificial Intelligence Market Trends,' and the search engine returns various reports, news, and analysis articles. The large language model summarizes this information, and the user can quickly understand the latest market dynamics and trends."
]
```

## Competitive Analysis
```python
[
    "Google Search: Google Search is the main search engine on the market, providing a vast array of search results. But Google Search does not offer a summary of search results, and users need to read and understand the results themselves.",
    "Microsoft Bing: Bing Search can also provide rich search results but does not offer a summary of the results.",
    "Wolfram Alpha: Wolfram Alpha is a computational search engine based on a knowledge base that can provide direct answers and summaries for certain types of queries. However, its knowledge base coverage is limited and cannot handle large-scale data."
]
```

## Development Requirement Pool
```python
[
    ("Develop intelligent summarization functionality based on a large language model", 5),
    ("Develop search engine core algorithms, including index building, query handling, result ranking, etc.", 7),
    ("Design and implement user interface, including query input, search result display, summary result display, etc.", 3),
    ("Build and maintain private knowledge base, including data collection, cleaning, updating, etc.", 7),
    ("Optimize search engine performance, including search speed, accuracy, relevance, etc.", 6),
    ("Develop user feedback mechanism, including feedback interface, feedback processing, etc.", 2),
    ("Develop security protection mechanism to prevent malicious queries and attacks", 3),
    ("Integrate large language model, including model selection, optimization, updating, etc.", 5),
    ("Conduct large-scale testing, including functional testing, performance testing, stress testing, etc.", 5),
    ("Develop data monitoring and logging system to monitor the running status and performance of the search engine", 4)
]
```
'''

SYSTEM_DESIGN = '''## Python package name
```python
"smart_search_engine"
```

## Task list:
```python
[
    "smart_search_engine/__init__.py",
    "smart_search_engine/main.py",
    "smart_search_engine/search.py",
    "smart_search_engine/index.py",
    "smart_search_engine/ranking.py",
    "smart_search_engine/summary.py",
    "smart_search_engine/knowledge_base.py",
    "smart_search_engine/interface.py",
    "smart_search_engine/user_feedback.py",
    "smart_search_engine/security.py",
    "smart_search_engine/testing.py",
    "smart_search_engine/monitoring.py"
]
```

## Data structures and interface definitions
```mermaid
classDiagram
    class Main {
        -SearchEngine search_engine
        +main() str
    }
    class SearchEngine {
        -Index index
        -Ranking ranking
        -Summary summary
        +search(query: str) str
    }
    class Index {
        -KnowledgeBase knowledge_base
        +create_index(data: dict)
        +query_index(query: str) list
    }
    class Ranking {
        +rank_results(results: list) list
    }
    class Summary {
        +summarize_results(results: list) str
    }
    class KnowledgeBase

 {
        +update(data: dict)
        +fetch_data(query: str) dict
    }
    Main --> SearchEngine
    SearchEngine --> Index
    SearchEngine --> Ranking
    SearchEngine --> Summary
    Index --> KnowledgeBase
```

## Program call flow
```mermaid
sequenceDiagram
    participant M as Main
    participant SE as SearchEngine
    participant I as Index
    participant R as Ranking
    participant S as Summary
    participant KB as KnowledgeBase
    M->>SE: search(query)
    SE->>I: query_index(query)
    I->>KB: fetch_data(query)
    KB-->>I: return data
    I-->>SE: return results
    SE->>R: rank_results(results)
    R-->>SE: return ranked_results
    SE->>S: summarize_results(ranked_results)
    S-->>SE: return summary
    SE-->>M: return summary
```
'''

TASKS = '''## Logic Analysis

In this project, all modules depend on the "SearchEngine" class, which is the main entry point, and other modules (Index, Ranking, and Summary) interact through it. Additionally, the "Index" class depends on the "KnowledgeBase" class, as it needs to fetch data from the knowledge base.

- "main.py" contains the "Main" class, which is the program entry point, calling "SearchEngine" for search operations, so "SearchEngine" must be defined before any other modules.
- "search.py" defines the "SearchEngine" class, dependent on "Index," "Ranking," and "Summary," so these modules need to be defined before "search.py."
- "index.py" defines the "Index" class, fetching data from "knowledge_base.py" to create indexes, so "knowledge_base.py" must be defined before "index.py."
- "ranking.py" and "summary.py" are relatively independent and only need to be defined before "search.py."
- "knowledge_base.py" is an independent module and can be developed first.
- "interface.py," "user_feedback.py," "security.py," "testing.py," and "monitoring.py" appear to be supporting functional modules and can be developed in parallel after the main functional modules are completed.

## Task list

```python
task_list = [
    "smart_search_engine/knowledge_base.py",
    "smart_search_engine/index.py",
    "smart_search_engine/ranking.py",
    "smart_search_engine/summary.py",
    "smart_search_engine/search.py",
    "smart_search_engine/main.py",
    "smart_search_engine/interface.py",
    "smart_search_engine/user_feedback.py",
    "smart_search_engine/security.py",
    "smart_search_engine/testing.py",
    "smart_search_engine/monitoring.py",
]
```
This task list first defines the most basic modules, followed by modules dependent on them, and finally the supporting modules. Depending on the team's capabilities and resources, multiple tasks can be developed simultaneously, as long as dependencies are met. For example, before developing "search.py," you can simultaneously develop "knowledge_base.py," "index.py," "ranking.py," and "summary.py."
'''

TASKS_TOMATO_CLOCK = '''## Required Python third-party packages: Provided in requirements.txt format
```python
Flask==2.1.1
Jinja2==3.1.0
Bootstrap==5.3.0-alpha1
```

## Logic Analysis: Provided as a Python str, analyze the dependencies between the files, which work should be done first
```python
"""
1. Start by setting up the Flask app, config.py, and requirements.txt to create the basic structure of the web application.
2. Create the timer functionality using JavaScript and the Web Audio API in the timer.js file.
3. Develop the frontend templates (index.html and settings.html) using Jinja2 and integrate the timer functionality.
4. Add the necessary static files (main.css, main.js, and notification.mp3) for styling and interactivity.
5. Implement the ProgressBar class in main.js and integrate it with the Timer class in timer.js.
6. Write tests for the application in test_app.py.
"""
```

## Task list: Provided as Python list[str], each str is a file, the more at the beginning, the more it is a prerequisite dependency, should be done first
```python
task_list = [
    'app.py',
    'config.py',
    'requirements.txt',
    'static/js/timer.js',
    'templates/index.html',
    'templates/settings.html',
    'static/css/main.css',
    'static/js/main.js',
    'static/audio/notification.mp3',
    'static/js/progressbar.js',
    'tests/test_app.py'
]
```
'''

TASK = """smart_search_engine/knowledge_base.py"""

STRS_FOR_PARSING = [
"""
## 1
```python
a
```
""",
"""
##2
```python
"a"
```
""",
"""
## 3
```python
a = "a"
```
""",
"""
## 4
```python
a = 'a'
```
"""
]


class MockMessages:
    req = Message(role="Boss", content=BOSS_REQUIREMENT, cause_by=BossRequirement)
    prd = Message(role="Product Manager", content=PRD, cause_by=WritePRD)
    system_design = Message(role="Architect", content=SYSTEM_DESIGN, cause_by=WriteDesign)
    tasks = Message(role="Project Manager", content=TASKS, cause_by=WriteTasks)
