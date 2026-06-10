# AI Model Decision Matrix: Haiku vs. GPT-4o-mini vs. Gemini Flash

This document provides a comparative analysis of the three leading "small/fast" models as of June 2026. Use this matrix to determine the most cost-effective and performant model for your specific use case.

## 📊 At-a-Glance Comparison

| Feature | Claude 3 Haiku | GPT-4o-mini | Gemini 1.5 Flash |
| :--- | :--- | :--- | :--- |
| **Provider** | Anthropic | OpenAI | Google |
| **Context Window** | 200,000 | 128,000 | **1,000,000+** |
| **Speed (Latency)** | Fast | **Extremely Fast** | Fast |
| **Intelligence Tier** | High-Efficiency | **High (Reasoning)** | High (Multimodal) |
| **Multimodal Support** | Images | Images | **Video, Audio, Images** |
| **Best For** | Human-like Chat | Structured Data/JSON | Long Context/Multimodal |

---

## 💰 Cost Table (Per 1 Million Tokens)

| Model | Input Price | Output Price | Note |
| :--- | :--- | :--- | :--- |
| **Gemini 1.5 Flash** | **$0.075** | **$0.30** | Cheapest for < 128k context. |
| **GPT-4o-mini** | $0.15 | $0.60 | Standard economy rate. |
| **Claude 3 Haiku** | $0.25 | $1.25 | Premium pricing for high-quality text. |

*Pricing is based on standard API rates and may vary by provider (e.g., OpenRouter, AWS Bedrock, Vertex AI).*

---

## 🛠️ When to Choose Which Model?

### 🚀 Choose **Gemini 1.5 Flash** when...
*   **Massive Context:** You need to analyze entire books, long PDF reports, or large codebases in one go.
*   **Multimodal Input:** You are processing **video** (up to 1 hour) or **audio** (up to 11 hours) directly.
*   **Lowest Cost:** You have high-volume, simple tasks and want the absolute lowest price per token.

### 🧠 Choose **GPT-4o-mini** when...
*   **Structured Outputs:** You need reliable **JSON** formatting, tool use, or function calling.
*   **Complex Reasoning:** You need the highest "intelligence" possible within a small, fast model.
*   **Ecosystem Integration:** You are already using OpenAI’s API and want a seamless, high-uptime experience.

### ✍️ Choose **Claude 3 Haiku** when...
*   **Human-like Tone:** You need creative writing, customer support, or "natural" sounding dialogue.
*   **Nuanced Instructions:** You have complex system prompts that require strict adherence to style or personality.
*   **Anthropic Loyalty:** You are integrated into AWS Bedrock or prefer Anthropic's safety-first alignment.

---

## ⚡ Prompting Quick-Start

### How to Run Prompts (Generic Examples)

#### **Example: Data Extraction (Best on GPT-4o-mini)**
```python
# Use for extracting structured data from messy text
system_prompt = "Extract the invoice total and date as JSON."
user_prompt = "Invoice #123, Date: 2024-05-12, Total: $450.00"
```

#### **Example: Large Document Analysis (Best on Gemini Flash)**
```python
# Use for summarizing a 500-page PDF
system_prompt = "Summarize the key financial risks in this document."
user_prompt = "[Insert 500k tokens of text here...]"
```

#### **Example: Customer Support (Best on Claude Haiku)**
```python
# Use for polite, helpful brand-aligned responses
system_prompt = "You are a helpful assistant for a boutique hotel. Use a warm, professional tone."
user_prompt = "How late is the pool open?"
```

---

## 🎯 Summary Decision Matrix

| If your priority is... | Use this Model |
| :--- | :--- |
| **Lowest Cost** | Gemini 1.5 Flash |
| **Largest File Support** | Gemini 1.5 Flash |
| **Best JSON/Logic** | GPT-4o-mini |
| **Natural Writing Style** | Claude 3 Haiku |
| **Real-time Latency** | GPT-4o-mini |
