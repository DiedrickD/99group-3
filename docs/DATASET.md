# Dataset, provenance and source selection

This project builds a **new, small, AI-assisted starter dataset** from research
on official sources. It does not claim to have downloaded an official,
comprehensive Lee Kuan Yew training dataset. All sources below were inspected
on **6 November 2026**. The authored notes were checked against the cited
passages during construction; no independent historian has reviewed them.

## Exactly what is included

| File | Rows | Contents |
| --- | ---: | --- |
| `sources.jsonl` | 8 | Primary speech metadata, URL, event date, displayed page date, passage locator, rights note and split |
| `notes.jsonl` | 16 | Original short paraphrases, source ID and topic tags |
| `train.jsonl` | 28 | 24 source-grounded QA rows and 4 abstention examples |
| `validation.jsonl` | 4 | Authored QA from a source excluded from training |
| `eval.jsonl` | 22 | Diagnostic questions, relevant note IDs and expected abstention |
| `manifest.json` | 1 | Counts, source groups and SHA-256 hashes |

Two questions per training note reuse an authored answer, so 28 rows do not
represent 28 independent pieces of historical evidence. The four abstention
examples have no source because they teach the model not to invent evidence.
Answers written in a direct first-person style are **new reconstructions**,
not Lee's actual words. Retrieval returns the third-person research notes.

Rebuild with `python scripts/build_dataset.py`; validate with
`python scripts/validate_data.py`. The builder creates original dataset files
without scraping or copying source documents.

## Official primary sources used

| ID | Event date | Publisher and source | Evidence used | Group |
| --- | --- | --- | --- | --- |
| S01 | 23 Apr 2011 | [PMO: Tanjong Pagar GRC Family Day](https://www.pmo.gov.sg/newsroom/speech-minister-mentor-lee-kuan-yew-tanjong-pagar-grc-family-day-2011-23-april-2011/) | English, mother tongues and vocational education | Training |
| S02 | 9 May 2011 | [PMO: GIC 30th Anniversary Dinner](https://www.pmo.gov.sg/newsroom/speech-minister-mentor-lee-kuan-yew-gic-30th-anniversary-dinner-9-may-2011-shangri-la/) | Reserves, investment talent and calculated risk | Training |
| S03 | 15 Aug 2010 | [PMO: Tanjong Pagar National Day Celebrations](https://www.pmo.gov.sg/newsroom/speech-mm-lee-kuan-yew-tanjong-pagar-national-day-celebrations-tanjong-pagar-community/) | Local adaptation, NEWater, congestion pricing and policy revision | Training |
| S04 | 18 Oct 2011 | [MFA: Ford Theatre ceremony](https://www.mfa.gov.sg/newsroom/press-statements-transcripts-and-photos/speech-by-former-mm-lee-kuan-yew-19-oct-2014/) | US-China relations and diverse talent | Training |
| S05 | 16 Mar 1965 | [NAS: Canberra National Press Club](https://www.nas.gov.sg/archivesonline/data/pdfdoc/lky19650316.pdf) | PDF pp. 3-4: small-state constraints and overlapping international interests | Training |
| S06 | 19 Dec 1971 | [NAS: PAP Party Congress](https://www.nas.gov.sg/archivesonline/data/pdfdoc/lky19711219.pdf) | PDF pp. 2-3: separation and British military withdrawal | Training |
| S07 | 25 Sep 1984 | [NAS: Dinner for the Establishment](https://www.nas.gov.sg/archivesonline/data/pdfdoc/lky19840925.pdf) | PDF p. 5: trusteeship and orderly succession | Validation |
| S08 | 27 Mar 1975 | [NAS: Parliamentary Pensions amendment debate](https://www.nas.gov.sg/archivesonline/data/pdfdoc/lky19750327.pdf) | PDF pp. 2-3: corruption convictions and leadership integrity | Held out from fine-tuning |

The MFA page has a metadata discrepancy: its heading describes an event on
18 October 2011, while its displayed page date is 19 October 2014. Both are
preserved. The 1965 Canberra event took place while Singapore was part of
Malaysia. The 1971 source is Lee's own party-political retrospective, and the
1975 debate is a historical proposal, not a description of current law.

A final source check corrected S07's passage locator to PDF page 5. Recorded
reports identify this reference-metadata correction; model inputs, raw generations
and metrics were unchanged because passage locators are not included in prompts.

## Train, validation and retrieval separation

S01-S06 supply training examples. S07 supplies validation loss measurements.
S08 appears in neither training nor validation. This prevents the same speech's
QA examples from being randomly scattered across those groups.

All 16 notes remain in the RAG index. A model may therefore answer questions
using a source it did not see during fine-tuning, which is the point of RAG.
“Held out from fine-tuning” does not mean held out from retrieval, and does not
mean the diagnostic questions constitute a blind external benchmark.

## Other datasets and books researched

| Candidate | What it offers | Decision |
| --- | --- | --- |
| [sjsim/lky-reasoning-recipe](https://huggingface.co/datasets/sjsim/lky-reasoning-recipe) | Community dataset/recipe with historical questions and NAS links; advertises Apache-2.0 | Not used. The viewer showed a schema-generation error during inspection; upstream source rights and individual rows need verification. |
| [NLB Lee Kuan Yew reference guide](https://reference.nlb.gov.sg/singapore/people/lee-kuan-yew/) | Bibliography and research routes to memoirs, interviews and other works | Discovery reference; its page text is not a training corpus. |
| *The Singapore Story* (1998) | Relevant memoir and personal historical account | Identified, not ingested. Add only through a permissioned workflow with edition/page provenance. |
| *From Third World to First* (2000) | Relevant account of governing and development | Identified, not ingested. No full-book training or retrieval is claimed. |
| Full articles and interviews | Potentially useful additional primary evidence | Add only after checking speaker identity, source quality and permitted use. |

The shipped corpus therefore consists of research notes based on **speeches**;
it is not a corpus of memoir and article full texts. That is a material scope
limit when describing this implementation in a challenge submission.

## Rights and redistribution

[PMO's terms](https://www.pmo.gov.sg/terms-of-use/) restrict reproduction and
modification of site content. Public access is not an open dataset license.
This repository publishes brief original notes and authored QA with links,
rather than full speech transcripts, scans or memoirs. No blanket license to
train on or redistribute the underlying source works is asserted.

The project's license for its original notes does not relicense the speeches,
their expressive content, or the base model. For a larger training corpus,
document permission for the intended use separately; confirm redistribution
rights before publishing text or derived artifacts. Local private originals
belong in ignored `data/private/`, not in Git.

## Expansion workflow

1. Record URL, author/speaker, event date, publisher, language and allowed uses.
2. Obtain permitted source files; parse HTML or PDF and use OCR only when needed.
3. Check page headers, footers, translations, speaker identity and OCR errors.
4. Deduplicate documents and near-duplicate passages before splitting by source.
5. Retain book edition/chapter/page, speech paragraph/page, and translation notes.
6. Split longer sources into section-aware chunks, around 300-500 tokens with
   modest overlap. Short atomic notes in this starter need no further splitting.
7. Draft source-grounded QA, including uncertainty, conflicting evidence and
   modern extrapolation cases. Have a human review each example.
8. Freeze an independent question set before model or retrieval tuning; version
   its manifest and keep it separate from training/example generation.
