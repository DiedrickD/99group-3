# Review of actual generated answers

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

The dependency-free, clearly labelled `notes` backend remains the default.
The `lora` backend is an inspectable experimental option with real training
artifacts and recorded failures. The live experimental demo, when running,
uses that adapter; readers should compare its answer to the linked notes.

A stronger follow-up should expand and independently review the source corpus,
compare a larger open-weight model on the same frozen cases, add paraphrase and
contradiction cases that were not used for tuning, and review claim entailment.
If testing an entailment model or an LLM judge, calibrate it against human labels
and record disagreements. None of those improvements is claimed as completed.
