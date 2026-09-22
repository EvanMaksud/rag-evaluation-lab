# RAG Retrieval Evaluation Report

## Summary

- Questions: **3**
- Hit rate@5: **1.000**
- Recall@5: **1.000**
- Precision@5: **0.333**
- MRR@5: **1.000**
- Answer-term coverage: **1.000**

## Per-Question Results

### mini-rag-1

Question: Why evaluate retrieval before generation in a RAG system?

- Hit: **True**
- Recall: **1.000**
- Precision: **0.333**
- Reciprocal rank: **1.000**
- Answer-term coverage: **1.000**

| Rank | Score | Document | Chunk |
| ---: | ---: | --- | --- |
| 1 | 0.3484 | `rag_basics` | # RAG Basics Retrieval-augmented generation separates document retrieval from answer generation . The retriever selects grounded context bef... |
| 2 | 0.0000 | `vision_quality` | # Vision Dataset Quality Computer-vision model quality depends on annotation consistency , balanced classes , valid bounding boxes , and car... |
| 3 | 0.0000 | `model_serving` | # Model Serving Machine-learning services need typed inputs , validated outputs , clear error messages , versioned artifacts , and monitorin... |

### mini-cv-1

Question: What dataset issues can hurt computer vision model quality?

- Hit: **True**
- Recall: **1.000**
- Precision: **0.333**
- Reciprocal rank: **1.000**
- Answer-term coverage: **1.000**

| Rank | Score | Document | Chunk |
| ---: | ---: | --- | --- |
| 1 | 0.4175 | `vision_quality` | # Vision Dataset Quality Computer-vision model quality depends on annotation consistency , balanced classes , valid bounding boxes , and car... |
| 2 | 0.0183 | `model_serving` | # Model Serving Machine-learning services need typed inputs , validated outputs , clear error messages , versioned artifacts , and monitorin... |
| 3 | 0.0162 | `rag_basics` | # RAG Basics Retrieval-augmented generation separates document retrieval from answer generation . The retriever selects grounded context bef... |

### mini-serving-1

Question: What matters when turning a model into a service?

- Hit: **True**
- Recall: **1.000**
- Precision: **0.333**
- Reciprocal rank: **1.000**
- Answer-term coverage: **1.000**

| Rank | Score | Document | Chunk |
| ---: | ---: | --- | --- |
| 1 | 0.0842 | `model_serving` | # Model Serving Machine-learning services need typed inputs , validated outputs , clear error messages , versioned artifacts , and monitorin... |
| 2 | 0.0744 | `rag_basics` | # RAG Basics Retrieval-augmented generation separates document retrieval from answer generation . The retriever selects grounded context bef... |
| 3 | 0.0709 | `vision_quality` | # Vision Dataset Quality Computer-vision model quality depends on annotation consistency , balanced classes , valid bounding boxes , and car... |
