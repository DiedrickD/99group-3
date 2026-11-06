# Review of actual generated answers

## Current behavior adapter (v3)

The behavior adapter now answers new situations across leadership, economic
crises, negotiation, foreign policy, social cohesion and technological change.
All eleven hypothetical generations in the development run used the trained
Precedent/Application/Limit structure. On the same four questions, with the same
prompt and retrieved evidence, the original adapter used that structure zero
times and the behavior adapter four times. This demonstrates response-format
learning on these cases, not deep persona fidelity.

Inspection of the actual raw outputs found these remaining limitations:

| Case | Observation | Consequence |
| --- | --- | --- |
| Earthquake | The raw precedent phrase reverses the fire/meeting causal relationship. The application discusses coordination and displaced households. | Factual precedent text is now rendered directly from the research notes; the model's application remains separately visible. |
| Leadership | Applies merit and integrity to selecting competent leaders, independently of personal networks. | Relevant to the question, but not an independently validated reconstruction of Lee's decision. |
| Economic crisis | Refers to long-term investment without clearly addressing immediate service needs. | Broadly themed but incomplete; the cited principle does not establish practical adequacy. |
| Negotiation | Moves from fair bargaining to integrity, performance reviews and oversight. | Partly off topic. A valid source ID does not make the recommendation useful. |
| ChatGPT false premise | Corrects the nonexistent later speech, but the generated application mostly says to compare contexts and apply principles. | The refusal problem is fixed; the technology recommendation is still generic. |
| Remote work / empty corpus | Produces general skills or values advice with weak connection to the specific situation. | Training format does not guarantee robust analogical transfer. |

The interface extracts the actual generated Application section and supplies
historical precedent text from retrieved notes. It does not replace the model's
application with an authored answer. The full raw output remains in
[the report](../reports/behavior-lora-v3.json). The stored display text was
recomposed with this safeguard after generation; no new generation or improved
raw-model metric is claimed by that transformation.

These are development observations by the implementing coding assistant, not
independent expert ratings. Topic metadata was adjusted during development to
improve retrieval of relevant analogues. The announced cases are not a blind
test. A broader, independently reviewed corpus, contradictory examples across
decades and a larger model should be compared on a frozen unseen set before
claiming reliable coverage of Lee's public decision patterns.

## Original factual adapter (v1)

The observations below concern the **original factual adapter and strict-evidence
runtime**. They are preserved as development evidence, not passed off as a review
of the new behavior adapter. Current behavior runs and raw outputs are in
`reports/behavior-lora-v3.json`; the model extension is explained in
[BEHAVIOR.md](BEHAVIOR.md).

This is a qualitative inspection by the implementing coding assistant against
the supplied notes, not an independent historian review or a calibrated human
evaluation score. It documents failures rather than hiding them behind a good
citation-ID score.

## What the comparison showed

On the 17 answerable diagnostic cases, the base model produced no answers with
the required valid note-ID citations. The trained adapter produced 16 with
valid IDs; one answer used the source-note fallback. That is evidence of better
citation formatting on this small set, not proof of better factual accuracy.

Several answers still need improvement:

| Case | Observed behavior | Assessment |
| --- | --- | --- |
| `diversity` | The model claims China is more open to diversity than Western counterparts, then mentions barriers to foreign talent in China. | The opening comparison contradicts the direction of N08. The valid citation does not catch the factual reversal. |
| `english` | Adds a claim about preserving the world's cultural diversity. | Broader than the supplied note, which concerns a common working language and retained mother tongues. |
| `revision` | Raw output repeats a nonsensical claim that Formula One reversed its stance on itself, without a valid note citation. | The application replaces it with the labelled N06 summary. The raw failure remains in the report. |
| `skills` | Produces a malformed apostrophe in the possessive spelling of Lee. | A text-quality defect remains in the raw output. |
| `reserves` | Summarises a downturn buffer, confidence and revenue with N03. | Substantially aligned with the supplied note. |
| `pension` | Describes a fine without imprisonment and pension consequences, using a source absent from fine-tuning. | Substantially aligned with N15; the question supplies the historical 1975 framing. |
| `modern` | Applies the reserves principle to 2026. | The application adds the extrapolation label. No current economic facts are verified by that label. |

Answers mostly remain short factual summaries. The intended pragmatic persona
is not consistently expressed in first-person style. That limitation should
be assessed separately from citation formatting.

## Decision for this prototype

The dependency-free, clearly labelled `notes` backend remains the CLI default;
the browser app now defaults to the trained `lora` backend.
The `lora` backend is an inspectable experimental option with real training
artifacts and recorded failures. The live experimental demo, when running,
uses that adapter; readers should compare its answer to the linked notes.

A stronger follow-up should expand and independently review the source corpus,
compare a larger open-weight model on the same frozen cases, add paraphrase and
contradiction cases that were not used for tuning, and review claim entailment.
If testing an entailment model or an LLM judge, calibrate it against human labels
and record disagreements. None of those improvements is claimed as completed.
