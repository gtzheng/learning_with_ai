# Learning Notes

## Efficient Attention Mechanisms
### Key Details
- [2026-03-19 21:47] self-attention, O(n²) complexity, sparse attention, axial attention, linear attention, Transformer architecture, Flash Attention, efficient transformers

### Frustration Points


## Document-Level LLMs
### Key Details
- [2026-03-22 21:06] context window, KV cache, working memory, scratchpad, RAG, vector store, in-weights memory, recurrent memory transformer, document coherence
- [2026-03-22 20:57] structural breakdown, topic drift, lost in the middle, entity inconsistency, hierarchical generation, document coherence, two-stage generation
- [2026-03-22 20:14] coherence, topic drift, lost in the middle, coreference consistency, context window, entity inconsistency, structural breakdown, repetition
- [2026-03-19 21:53] document-level LLMs, context windows, coherence, long-range dependencies, transformers, Longformer, RAG, attention mechanisms, learning path

### Frustration Points


## Efficient Parameter Sharing
### Key Details
- [2026-03-19 21:53] parameter sharing, fine-tuning, transfer learning, multi-task learning, LoRA, adapter layers, PEFT, pretrained models

### Frustration Points


## Scalability in Training and Deployment
### Key Details
- [2026-03-22 22:38] speculative decoding loop, draft model synchronization, token acceptance and rejection, context update, bonus token
- [2026-03-22 22:30] speculative decoding, draft model, verification parallelism, acceptance rate, rejection sampling, autoregressive decoding
- [2026-03-22 22:25] continuous batching, KV cache, PagedAttention, speculative decoding, quantization, inference optimization, vLLM
- [2026-03-19 21:54] LLM scalability overview, distributed training, inference optimization, scaling laws, data parallelism, model parallelism, learning resources, learning path

### Frustration Points


## Adversarial Attacks and Robustness
### Key Details
- [2026-03-22 21:34] RLHF, Constitutional AI, adversarial training, input/output filtering, prompt hardening, privilege separation, spotlighting, dual LLM pattern, human-in-the-loop, defense in depth
- [2026-03-22 21:22] jailbreaks, prompt injection, alignment bypass, instruction hijacking, LLM security, threat models
- [2026-03-19 21:54] adversarial attacks, LLM vulnerabilities, jailbreaking, prompt injection, robustness, red teaming, alignment, OWASP Top 10 for LLMs

### Frustration Points


## Compression and Quantization
### Key Details
- [2026-03-23 07:53] quantization basics, FP32 vs INT8, scale and zero-point, weight distributions, quantization error, why accuracy is preserved
- [2026-03-19 21:55] quantization, model compression, LLM deployment, memory efficiency, pruning, knowledge distillation, post-training quantization, bits and precision

### Frustration Points


## Model Fine-Tuning for Low-Resource Languages
### Key Details
- [2026-03-19 21:57] low-resource languages, fine-tuning, large language models, transfer learning, multilingual models, XLM-RoBERTa, LoRA, data scarcity, cross-lingual transfer, parameter-efficient fine-tuning

### Frustration Points


## Fine-Tuning for Specific Domains
### Key Details
- [2026-03-22 19:31] LoRA, QLoRA, low-rank adaptation, PEFT, quantization, attention matrices, trainable parameters, efficient fine-tuning
- [2026-03-20 15:33] cross-entropy loss, perplexity, natural logarithm, probability, model evaluation
- [2026-03-20 12:09] raw text format, instruction-response pairs, conversation format, data quality rules, synthetic data generation, data quantity guidelines, ChatML format, Alpaca format
- [2026-03-20 11:49] pre-training, fine-tuning, prompt engineering vs fine-tuning, domain-specific datasets, Hugging Face Trainer API, tokenization, training loop
- [2026-03-20 11:44] fine-tuning, domain adaptation, pre-trained LLMs, LoRA, PEFT, instruction tuning, dataset curation, prompt engineering vs fine-tuning

### Frustration Points


## Transfer Learning across Domains
### Key Details
- [2026-03-20 15:11] transfer learning, domain shift, LLMs, fine-tuning, domain adaptation, DAPT, LoRA

### Frustration Points


## Multilingual and Cross-Lingual LLMs
### Key Details
- [2026-03-23 07:37] multilingual training pipeline, temperature sampling, SentencePiece tokenization, zero-shot cross-lingual transfer, data imbalance, XLM-R, masked language modeling
- [2026-03-23 07:33] multilingual LLMs, cross-lingual transfer, mBERT, XLM-R, low-resource languages, tokenization, curse of multilinguality, zero-shot transfer

### Frustration Points


## Interpretable LLM Outputs
### Key Details
- [2026-03-23 07:54] interpretable ML, explainable AI, LLM outputs, attention mechanisms, SHAP, LIME, chain-of-thought, mechanistic interpretability

### Frustration Points


## Data Collection and Labeling
### Key Details
- [2026-04-02 20:27] programmatic labeling, labeling functions, Snorkel framework, label model, weak supervision, probabilistic labels, LF coverage and accuracy
- [2026-04-02 20:17] Cohen's Kappa, inter-annotator agreement, observed agreement, expected agreement, quality control in labeling pipelines
- [2026-04-02 20:04] data pipeline architecture, data lake vs warehouse, curation pipeline, labeling system design, active learning, data flywheel, inter-annotator agreement, bias types
- [2026-03-23 09:23] data collection, data labeling, dataset bias, crowdsourcing, active learning, data quality, learning path

### Frustration Points


## Data Structures
### Key Details
- [2026-03-23 09:24] data preprocessing overview, missing values, normalization, encoding categorical variables, dataset splitting, learning resources, learning path

### Frustration Points


## Feature Engineering and Selection
### Key Details
- [2026-04-03 12:24] feature engineering, feature selection, dimensionality reduction, ML pipeline, learning roadmap

### Frustration Points


## Tokenization
### Key Details
- [2026-04-04 16:34] byte-level BPE, UTF-8 encoding, 256 byte vocabulary, unknown token elimination, multilingual tokenization, GPT-2 tokenizer
- [2026-04-04 16:06] BPE side effects, letter counting failure, arithmetic inconsistency, language inequality, capitalization sensitivity, trailing space, glitch tokens, SolidGoldMagikarp
- [2026-04-04 15:27] BPE algorithm, merge rules, vocabulary building, subword tokenization, encoding with BPE
- [2026-04-04 15:15] subword tokenization, vocabulary, token IDs, BPE intuition, WordPiece, encoding process
- [2026-04-04 11:54] word-level tokenization, character-level tokenization, OOV problem, vocabulary size, subword tokenization, context window
- [2026-04-03 12:39] tokenization overview, BPE, WordPiece, SentencePiece, learning path, subword tokenization

### Frustration Points

