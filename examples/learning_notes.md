# Learning Notes

## Attention Optimization Strategies
### Key Details
- [2026-03-19 21:47] self-attention, O(n²) complexity, sparse attention, linear attention, Flash Attention, multi-query attention

### Frustration Points


## Long-Context Modeling
### Key Details
- [2026-03-22 21:06] context window, KV cache, working memory, scratchpad, RAG, vector store, recurrent memory transformer, document coherence
- [2026-03-22 20:57] structural breakdown, topic drift, lost in the middle, entity inconsistency, hierarchical generation, two-stage generation
- [2026-03-22 20:14] coherence, topic drift, lost in the middle, coreference consistency, context window, entity inconsistency, repetition
- [2026-03-19 21:53] long-context modeling, context windows, coherence, long-range dependencies, Longformer, RAG, attention mechanisms

### Frustration Points


## Parameter-Efficient Fine-Tuning
### Key Details
- [2026-03-22 19:31] LoRA, QLoRA, low-rank adaptation, PEFT, quantization, attention matrices, trainable parameters
- [2026-03-20 15:33] cross-entropy loss, perplexity, natural logarithm, probability, model evaluation
- [2026-03-20 12:09] raw text format, instruction-response pairs, conversation format, data quality, synthetic data generation, ChatML format, Alpaca format
- [2026-03-20 11:49] pre-training, fine-tuning, prompt engineering vs fine-tuning, domain-specific datasets, Hugging Face Trainer API, tokenization
- [2026-03-20 11:44] fine-tuning, domain adaptation, pre-trained LLMs, LoRA, PEFT, instruction tuning, dataset curation
- [2026-03-19 21:53] parameter sharing, multi-task learning, LoRA, adapter layers, PEFT, pretrained models

### Frustration Points


## Scaling Laws and Training Efficiency
### Key Details
- [2026-03-22 22:38] speculative decoding loop, draft model synchronization, token acceptance and rejection, context update
- [2026-03-22 22:30] speculative decoding, draft model, verification parallelism, acceptance rate, rejection sampling, autoregressive decoding
- [2026-03-22 22:25] continuous batching, KV cache, PagedAttention, speculative decoding, quantization, inference optimization, vLLM
- [2026-03-19 21:54] scalability overview, distributed training, inference optimization, scaling laws, data parallelism, model parallelism

### Frustration Points


## Robustness and Adversarial Inputs
### Key Details
- [2026-03-22 21:34] RLHF, Constitutional AI, adversarial training, input/output filtering, prompt hardening, privilege separation, defense in depth
- [2026-03-22 21:22] jailbreaks, prompt injection, alignment bypass, instruction hijacking, LLM security, threat models
- [2026-03-19 21:54] adversarial attacks, LLM vulnerabilities, jailbreaking, prompt injection, robustness, red teaming, alignment

### Frustration Points


## Model Compression Techniques
### Key Details
- [2026-03-23 07:53] quantization basics, FP32 vs INT8, scale and zero-point, weight distributions, quantization error
- [2026-03-19 21:55] quantization, model compression, pruning, knowledge distillation, post-training quantization, bits and precision

### Frustration Points


## Multilingual Language Models
### Key Details
- [2026-03-23 07:37] multilingual training pipeline, temperature sampling, SentencePiece tokenization, zero-shot cross-lingual transfer, data imbalance, XLM-R
- [2026-03-23 07:33] multilingual LLMs, cross-lingual transfer, mBERT, XLM-R, low-resource languages, tokenization, curse of multilinguality
- [2026-03-19 21:57] low-resource languages, fine-tuning, transfer learning, multilingual models, XLM-RoBERTa, LoRA, cross-lingual transfer

### Frustration Points


## Cross-Domain Adaptation
### Key Details
- [2026-03-20 15:11] domain shift, continued pretraining, fine-tuning, domain adaptation, LoRA

### Frustration Points


## Interpretability and Mechanistic Analysis
### Key Details
- [2026-03-23 07:54] interpretable ML, explainable AI, attention mechanisms, SHAP, LIME, chain-of-thought, mechanistic interpretability

### Frustration Points


## Tokenization and Vocabulary Design
### Key Details
- [2026-04-04 16:34] byte-level BPE, UTF-8 encoding, 256 byte vocabulary, unknown token elimination, multilingual tokenization, GPT-2 tokenizer
- [2026-04-04 16:06] BPE side effects, letter counting failure, arithmetic inconsistency, language inequality, capitalization sensitivity, glitch tokens
- [2026-04-04 15:27] BPE algorithm, merge rules, vocabulary building, subword tokenization, encoding with BPE
- [2026-04-04 15:15] subword tokenization, vocabulary, token IDs, BPE intuition, WordPiece, encoding process
- [2026-04-04 11:54] word-level tokenization, character-level tokenization, OOV problem, vocabulary size, subword tokenization, context window
- [2026-04-03 12:39] tokenization overview, BPE, WordPiece, SentencePiece, subword tokenization

### Frustration Points


## Dataset Construction and Labeling
### Key Details
- [2026-04-02 20:27] programmatic labeling, labeling functions, Snorkel framework, label model, weak supervision, probabilistic labels
- [2026-04-02 20:17] Cohen's Kappa, inter-annotator agreement, observed agreement, expected agreement, quality control
- [2026-04-02 20:04] data pipeline architecture, data lake vs warehouse, curation pipeline, labeling system design, active learning, data flywheel
- [2026-03-23 09:23] data collection, data labeling, dataset bias, crowdsourcing, active learning, data quality

### Frustration Points


## Data Preprocessing Pipelines
### Key Details
- [2026-03-23 09:24] data preprocessing overview, missing values, normalization, encoding categorical variables, dataset splitting

### Frustration Points


## Feature Engineering Practices
### Key Details
- [2026-04-03 12:24] feature engineering, feature selection, dimensionality reduction, ML pipeline

### Frustration Points
