# Ready-to-paste challenge response

## Lee Kuan Yew Chatbot Implementation

I built a text-based historical simulation that can answer factual questions
and apply selected Lee Kuan Yew decision patterns to new situations. Every
response is identified as a reconstruction, not an authentic quotation or
access to his private thoughts.

The system has three trained roles: a small intent classifier, a factual LoRA
adapter and a separate behavior LoRA adapter. The two language-model variants
share a pinned Qwen2.5-0.5B-Instruct base model. The original factual adapter
trained on 28 authored examples. The behavior adapter then trained on 56 unique
examples across two stages, with additional replay; the router trained on 48
labelled questions. All runs completed locally on CPU and have recorded data
hashes, parent model hashes and training settings.

Behavior examples connect an observed public situation and response to an
inferred principle and a hypothetical application. They cover fourteen areas,
including leadership, succession, integrity, negotiation, economic crises,
technological change, education, foreign policy, social cohesion and disasters.
This is selective coverage of public decisions, not all of Lee's beliefs.

RAG retrieves historical evidence for factual questions and analogous cases
for new scenarios. For an earthquake question, a relevant precedent is the
1961 Bukit Ho Swee urban-fire rehousing response. For ChatGPT, Lee's 2011
account of helping workers adapt to computers provides an analogy. Neither
source proves what he would say about those new situations. The response
separates Precedent, Application and Limit, and cites the historical basis.

If a question falsely assumes that Lee gave a ChatGPT speech in 2024, the
application corrects the premise and continues with an explicitly hypothetical
response. It does not simply refuse because no exact document exists.

## Repository / Workflow Links

- Repository: https://github.com/DiedrickD/99group-3
- Chat examples: https://github.com/DiedrickD/99group-3/blob/main/docs/CHAT_EXAMPLES.md
- Architecture and training: https://github.com/DiedrickD/99group-3/blob/main/docs/BEHAVIOR.md
- Sources: https://github.com/DiedrickD/99group-3/blob/main/docs/DATASET.md
- Results: https://github.com/DiedrickD/99group-3/blob/main/docs/RESULTS.md
- Current temporary demo: see https://github.com/DiedrickD/99group-3/blob/main/docs/DEMO.md
- Colab: https://colab.research.google.com/github/DiedrickD/99group-3/blob/main/notebooks/train_colab.ipynb

## Technical Approach & Implementation Notes

The source corpus contains ten records supporting 21 original short research
notes: nine primary speeches and one institutional history. Sources include
PMO, MFA, NAS and NLB. Speaker identity, event date and passage locators are
recorded. Memoir full texts are not used or redistributed.

The router is a trained multinomial Naive Bayes classifier, supplemented by
explicit rules. It determines question intent rather than factual truth.
BM25 and curated topic metadata retrieve relevant notes or analogous principles.
The factual and behavior LoRA variants use the same pinned base revision and
are switched according to intent. Training uses assistant-token loss and
source-separated validation. Behavior validation token loss changed from
2.1096 to 1.7529 in the first stage and to 1.6988 after the broader stage.
Those small-set losses do not establish historical accuracy.

Evaluation separately measures routing, analogue retrieval, false-premise
corrections, three-part response structure and raw outputs. A no-behavior-adapter
comparison uses the same questions, prompt and evidence on a recorded subset.
The original 22-case factual experiment remains archived; it is not reported
as current behavior-model performance. Faithfulness, useful transfer and style
require qualitative review. The 0.5B model and synthetic dataset remain a
prototype, with no independent historian review or blind generalization claim.

Python, PyTorch, Transformers, PEFT and safetensors provide training and
inference. Gradio provides text chat and temporary public sharing. GitHub Actions
contains checks; an account restriction prevented hosted jobs from starting.
Local checks and actual public chat requests are recorded separately. The Colab
notebook is a GPU reproduction workflow, not a completed GPU run.
