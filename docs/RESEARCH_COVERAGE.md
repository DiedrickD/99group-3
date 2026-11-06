# Research coverage: a public decision profile across domains

The research target is a collection of documented decisions, constraints,
tradeoffs and changes of position across Lee's public life. The current model
is an initial selective profile. Counting many paraphrases of one speech does
not turn them into independent historical evidence.

## Evidence already used in behavior training

| Area | Source-linked starting point | Candidate transfer, always inferred |
| --- | --- | --- |
| Leadership and succession | S03 / C02: new teams and officers improving on predecessors | Delegation and building an institution beyond its founder |
| Integrity and merit | S03 / C03: integrity and appointment on merit | Selecting leaders on demonstrated competence |
| Economic shocks | S06 / N11: preparation for British withdrawal | Preparing alternatives before a foreseeable disruption |
| Fiscal resilience | S02 / N03: reserves as a buffer | Maintaining capacity to withstand shocks |
| Labour negotiation and shared growth | S10 / C04: fair bargaining and cooperation | Examining shared interests and a workable agreement |
| Education and technological change | S01 / N02 and S10 / C05: vocational skills and computer training | Developing capabilities alongside new technology |
| Foreign policy | S04 / N07 and S05 / N09: major powers and small-state constraints | Assessing interests, dependencies and room to act |
| Talent and innovation | S04 / N08: attracting diverse talent | Recruiting useful capabilities rather than assuming self-sufficiency |
| Language and social cohesion | S01 / N01 and S06 / N12 | Communication across groups and maintaining workable cooperation |
| Policy revision | S03 / N05-N06: adaptation and revisiting decisions | Changing an approach when circumstances or evidence change |
| Disaster recovery | S09 / C01: urban-fire rehousing and institutional coordination | Coordinating recovery after a different disruption |

The source register and dates are in [DATASET.md](DATASET.md). The fourteen
area labels group overlapping themes; there are fourteen annotated cases and
56 unique authored training examples, not fourteen large independent corpora.
Most primary source speeches are from Lee's later public life. That temporal
skew limits any claim about his whole career.

## Routes to a substantially broader corpus

The [NAS access guide](https://corporate.nas.gov.sg/archives-reading-room/access-to-records/)
identifies speeches, government records, audiovisual materials and oral histories
as research routes. Different records can expose differences between a public
speech, a later recollection and the record of a decision. Access and reproduction
conditions must be checked for each item.

[The 2011 launch record](https://www.nas.gov.sg/archivesonline/data/pdfdoc/20111007002/press_release_launch_of_lky_papers_%28final_version%29.pdf)
describes *The Papers of Lee Kuan Yew: Speeches, Interviews and Dialogues
(1950-1990)*, compiled from NAS and other collections. It is a discovery route
to much broader chronological coverage, not an openly licensed training download.
The [NLB reference guide](https://reference.nlb.gov.sg/singapore/people/lee-kuan-yew/)
also identifies memoirs, interviews and strategic-thought studies. None of these
collections or books has been ingested wholesale by this project.

A concrete additional candidate is [NLB's published extract of Lee's 1982 oral
history about separation](https://biblioasia.nlb.gov.sg/all-sections/vol-22-issue-2-jul-sep-2026-the-days-leading-to-separation-in-lee-kuan-yews-own-words-/).
It recounts negotiations and discussions within the leadership around the 1965
separation. It was inspected as a future annotation candidate on 6 November
2026, but is not in the current training or retrieval corpus. Its retrospective
nature and the role of other participants must remain explicit.

| Research gap | Evidence needed before claiming coverage |
| --- | --- |
| Housing, land use, water and infrastructure | Multiple dated decisions, implementation records and their constraints, beyond the few references already indexed |
| Defence, security and independence | Primary policy records, contemporary context and corroboration of who decided what |
| Health, welfare, family and population policy | Dated statements and revisions; competing objectives and affected groups |
| Dissent, press, political opposition and civil liberties | Lee's stated positions alongside contested accounts and independently assessed consequences |
| Leadership conflict and failure | Examples of disagreement, unsuccessful choices and changes of position, rather than only favourable retrospective accounts |
| Personal advice and values | Relevant interviews or permissioned memoir passages; avoid inferring private preferences from state policy alone |

These are gaps and research targets, not a claim that the current model has
learned those subjects. A balanced profile should retain contested judgments
and policy costs, rather than treating every decision as a generic success story.

## Annotation and evaluation workflow

For each new event, record speaker/actor, event date, document date, exact
locator, situation, publicly observed response, stated justification, inferred
principle, transfer limits and any conflicting evidence. Distinguish Lee's own
account, collective government action and independent outcome assessment.
Do not invent motives when the record supplies none.

Create several genuinely different scenarios per reviewed principle, including
cases where the analogy should *not* transfer. Keep whole events or source
families out of training, then freeze unseen evaluation questions before tuning.
RAG supplies the relevant historical basis; behavior fine-tuning teaches how to
apply a principle and acknowledge a mismatch. A larger model may help, but must
be measured rather than assumed better.

Evaluate historical entailment, choice of analogy, relevance of the proposed
action, tradeoffs, uncertainty and consistency with dated evidence separately
from response format. Include disagreements between evidence from different
decades. Expert review is needed to judge fidelity; no automated score can
establish access to private thoughts.
