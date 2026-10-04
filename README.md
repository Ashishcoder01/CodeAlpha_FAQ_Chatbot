# Nexora AI — Intelligent Customer Support Assistant

<p align="center">

  <strong>An NLP-powered FAQ chatbot for intelligent customer support</strong>

  <br><br>

  <a href="https://codealpha-faq-chatbot1.streamlit.app/">
    <strong>Live Demo</strong>
  </a>
  &nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="https://github.com/Ashishcoder01/CodeAlpha_FAQ_Chatbot">
    <strong>GitHub Repository</strong>
  </a>

</p>

---

## Overview

Nexora AI is an NLP-powered FAQ chatbot designed to provide intelligent answers to customer-support questions.

The system processes natural-language questions, identifies the most relevant FAQ using intent-aware matching and TF-IDF-based similarity, and returns the best available answer with a confidence score.

Nexora AI is a fictional demonstration project created for learning, portfolio, and internship purposes.

---

## Live Demo

Try the deployed application directly in your browser:

**[Open Nexora AI](https://codealpha-faq-chatbot1.streamlit.app/)**

No local installation is required to try the live application.

---

## Features

- Natural Language Processing based question matching
- TF-IDF vectorization
- Cosine similarity
- Intent-aware matching
- 60 structured FAQs
- 12 FAQ categories
- Multiple question variations
- Confidence scoring
- Intelligent fallback handling
- Suggested questions
- Professional Streamlit interface
- Latest-question-only chat experience
- Automated Pytest test suite
- Public Streamlit deployment

---

## FAQ Knowledge Base

The chatbot contains **60 FAQs** organized into **12 categories**.

| Category | Purpose |
|---|---|
| Company | General company information |
| Products | Product-related questions |
| Pricing | Plans and pricing |
| Account | Account management |
| Security | Account and security concerns |
| Billing | Payments and billing |
| Support | Customer support |
| Getting Started | Getting started with the platform |
| Enterprise | Enterprise features |
| Integrations | Software integrations |
| Troubleshooting | Common technical problems |
| Privacy | Privacy-related questions |

---

## How It Works

```text
                    User Question
                         |
                         v
                Text Preprocessing
                         |
                         v
                  Intent Detection
                         |
                         v
                  TF-IDF Vectorizer
                         |
                         v
                 Cosine Similarity
                         |
                         v
                  Best FAQ Match
                         |
                         v
                Confidence Evaluation
                    /           \
                   /             \
          Reliable Match       Low Confidence
                |                    |
                v                    v
          FAQ Answer             Fallback