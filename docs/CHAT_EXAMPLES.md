# Recorded chat examples: behavior-trained model

These are actual local outputs of the factual or behavior LoRA adapter, selected
from [the complete 16-case report](../reports/behavior-lora-v3.json). The interface
renders historical precedents from the source notes and displays the model's
generated application separately. The unmodified model output remains in each
report row. Weak answers are retained: formatting is better, but recommendations
can be generic or miss the question. See [the quality review](QUALITY_REVIEW.md).

The model covers leadership, crises, negotiation, technology, foreign relations
and other domains; it does not reproduce Lee's private thoughts or establish his
views on modern events. [Training and architecture](BEHAVIOR.md),
[temporary live demo](DEMO.md), [original v1 examples](CHAT_EXAMPLES_V1.md).

## chatgpt-false-premise

**User:** What speech did Lee give about ChatGPT in 2024?

Adapter: `behavior`; status: `hypothetical_generated`.

Historical simulation; generated text is not an authentic Lee Kuan Yew quotation.

Lee Kuan Yew died on 23 March 2015, so he could not have delivered the requested later speech. The response below considers the topic hypothetically.

Hypothetical interpretation / extrapolation, not a documented view of Lee Kuan Yew.

Historical precedent (source notes): In that address, Lee described unions and government helping workers adapt to computers through training. This is evidence about an earlier technological transition, not a recorded view of generative AI. [C05]

Possible application (LLM-generated): I would consider whether the current context is similar to the past, and whether the principle can be applied to the new situation.

Limit: An analogy identifies a possible approach, not proof of Lee's opinion. Differences in the new situation and relevant expertise still matter.

Historical basis (supports the principles, not this hypothetical conclusion):
- Help workers acquire capabilities for technological change, as in the computer-training account. [C05]
- Re-examine a policy when circumstances change; avoid treating an earlier position as permanent. [N06]
- Study useful solutions and adapt them to local constraints rather than copying a system wholesale. [N05]

Sources:
[C05] Lee Kuan Yew at NTUC's 50th Anniversary Dinner (2011-05-13), PDF pages 2-4: shared growth, tripartite cooperation, worker training for computer adoption
https://www.nas.gov.sg/archivesonline/data/pdfdoc/lky20110513.pdf
[N06] MM Lee Kuan Yew at Tanjong Pagar National Day Celebrations 2010 (2010-08-15), passages on basic values, NEWater and policy revision
https://www.pmo.gov.sg/newsroom/speech-mm-lee-kuan-yew-tanjong-pagar-national-day-celebrations-tanjong-pagar-community/
[N05] MM Lee Kuan Yew at Tanjong Pagar National Day Celebrations 2010 (2010-08-15), passages on basic values, NEWater and policy revision
https://www.pmo.gov.sg/newsroom/speech-mm-lee-kuan-yew-tanjong-pagar-national-day-celebrations-tanjong-pagar-community/

Biographical source for the correction: National Library Board: Lee Kuan Yew reference guide
https://reference.nlb.gov.sg/singapore/people/lee-kuan-yew/

## empty-corpus

**User:** How might Lee approach a difficult personal decision?

Adapter: `behavior`; status: `hypothetical_generated`.

Historical simulation; generated text is not an authentic Lee Kuan Yew quotation.

Hypothetical interpretation / extrapolation, not a documented view of Lee Kuan Yew.

Historical precedent (source notes): No historical precedent is supplied.

Possible application (LLM-generated): I would consider my values and priorities, seek support from others, and make a decision based on the best evidence and understanding.

Limit: An analogy identifies a possible approach, not proof of Lee's opinion. Differences in the new situation and relevant expertise still matter.

No matching historical evidence is supplied; this is a general style simulation.

## historical

**User:** Why was English useful as a working language?

Adapter: `default`; status: `generated`.

Historical simulation; generated text is not an authentic Lee Kuan Yew quotation.

English was useful as a working language because it could bridge the gap between the different languages and cultures of the world. It allowed people to communicate across borders and facilitate international access. The use of English also helped to preserve the cultural diversity of the world. [N01]

Sources:
[N01] MM Lee Kuan Yew at the Tanjong Pagar GRC Family Day 2011 (2011-04-23), passages on English, mother tongues and ITEs
https://www.pmo.gov.sg/newsroom/speech-minister-mentor-lee-kuan-yew-tanjong-pagar-grc-family-day-2011-23-april-2011/

## earthquake

**User:** What will Lee do on an eartquake disaster so big?

Adapter: `behavior`; status: `hypothetical_generated`.

Historical simulation; generated text is not an authentic Lee Kuan Yew quotation.

Hypothetical interpretation / extrapolation, not a documented view of Lee Kuan Yew.

Historical precedent (source notes): After the 1961 Bukit Ho Swee urban fire, Lee announced plans to relocate displaced families, following an emergency Cabinet meeting and consultation with HDB. This describes a collective government response; it does not establish a forest-fire or earthquake policy. [C01]

Possible application (LLM-generated): I would coordinate all affected households, including those without electricity, food, shelter, and medical care.

Limit: An analogy identifies a possible approach, not proof of Lee's opinion. Differences in the new situation and relevant expertise still matter.

Historical basis (supports the principles, not this hypothetical conclusion):
- Coordinate institutions and address displacement, drawing cautiously on the Bukit Ho Swee fire response. [C01]

Sources:
[C01] Bukit Ho Swee fire (1961-05-25), Government response and Relocation of affected families sections
https://www.nlb.gov.sg/main/article-detail?cmsuuid=8a0ca033-7b44-47a1-b4cd-f841debdf6db

## leadership

**User:** How might Lee respond when a company promotes friends rather than capable people?

Adapter: `behavior`; status: `hypothetical_generated`.

Historical simulation; generated text is not an authentic Lee Kuan Yew quotation.

Hypothetical interpretation / extrapolation, not a documented view of Lee Kuan Yew.

Historical precedent (source notes): In the same 2010 address, Lee linked capable institutions with leadership integrity, appointment on merit rather than personal connections, and equal opportunity across race, language and religion. [C03]

Possible application (LLM-generated): I would appoint competent leaders who are independent from their networks and have a clear vision for the organisation.

Limit: An analogy identifies a possible approach, not proof of Lee's opinion. Differences in the new situation and relevant expertise still matter.

Historical basis (supports the principles, not this hypothetical conclusion):
- Use relevant competence and institutional integrity rather than personal connections. [C03]
- Preserve buffers and take a long view when managing resources and uncertainty. [N03]

Sources:
[C03] MM Lee Kuan Yew at Tanjong Pagar National Day Celebrations 2010 (2010-08-15), passages on basic values, NEWater and policy revision
https://www.pmo.gov.sg/newsroom/speech-mm-lee-kuan-yew-tanjong-pagar-national-day-celebrations-tanjong-pagar-community/
[N03] MM Lee Kuan Yew at the GIC 30th Anniversary Dinner (2011-05-09), passages on reserves, talent and calculated investment risks
https://www.pmo.gov.sg/newsroom/speech-minister-mentor-lee-kuan-yew-gic-30th-anniversary-dinner-9-may-2011-shangri-la/

## economic-crisis

**User:** What would Lee consider if a severe recession threatens essential services?

Adapter: `behavior`; status: `hypothetical_generated`.

Historical simulation; generated text is not an authentic Lee Kuan Yew quotation.

Hypothetical interpretation / extrapolation, not a documented view of Lee Kuan Yew.

Historical precedent (source notes): Lee described national reserves as protection during downturns, support for confidence and a contributor to public revenue; GIC should invest with a long horizon. [N03]

Possible application (LLM-generated): I would ensure that the government has a long-term investment strategy.

Limit: An analogy identifies a possible approach, not proof of Lee's opinion. Differences in the new situation and relevant expertise still matter.

Historical basis (supports the principles, not this hypothetical conclusion):
- Preserve buffers and take a long view when managing resources and uncertainty. [N03]

Sources:
[N03] MM Lee Kuan Yew at the GIC 30th Anniversary Dinner (2011-05-09), passages on reserves, talent and calculated investment risks
https://www.pmo.gov.sg/newsroom/speech-minister-mentor-lee-kuan-yew-gic-30th-anniversary-dinner-9-may-2011-shangri-la/

## negotiation

**User:** How might Lee approach a dispute where workers and employers no longer trust each other?

Adapter: `behavior`; status: `hypothetical_generated`.

Historical simulation; generated text is not an authentic Lee Kuan Yew quotation.

Hypothetical interpretation / extrapolation, not a documented view of Lee Kuan Yew.

Historical precedent (source notes): In his 2011 NTUC address, Lee described cooperation among government, employers and unions, fair bargaining and workers sharing the benefits of growth. [C04]

Possible application (LLM-generated): I would ensure my own integrity and hold leaders accountable through strong performance evaluations and independent oversight.

Limit: An analogy identifies a possible approach, not proof of Lee's opinion. Differences in the new situation and relevant expertise still matter.

Historical basis (supports the principles, not this hypothetical conclusion):
- Consider fair bargaining, cooperation and whether workers share in growth. [C04]
- Expect leaders to uphold the conduct they demand of their institutions. [N16]
- Use relevant competence and institutional integrity rather than personal connections. [C03]

Sources:
[C04] Lee Kuan Yew at NTUC's 50th Anniversary Dinner (2011-05-13), PDF pages 2-4: shared growth, tripartite cooperation, worker training for computer adoption
https://www.nas.gov.sg/archivesonline/data/pdfdoc/lky20110513.pdf
[N16] Lee Kuan Yew moving the Parliamentary Pensions (Amendment) Bill (1975-03-27), PDF pages 2-3, corruption convictions and leadership standards
https://www.nas.gov.sg/archivesonline/data/pdfdoc/lky19750327.pdf
[C03] MM Lee Kuan Yew at Tanjong Pagar National Day Celebrations 2010 (2010-08-15), passages on basic values, NEWater and policy revision
https://www.pmo.gov.sg/newsroom/speech-mm-lee-kuan-yew-tanjong-pagar-national-day-celebrations-tanjong-pagar-community/

## foreign-policy

**User:** What would Lee consider if a small country faces pressure from rival major powers?

Adapter: `behavior`; status: `hypothetical_generated`.

Historical simulation; generated text is not an authentic Lee Kuan Yew quotation.

Hypothetical interpretation / extrapolation, not a documented view of Lee Kuan Yew.

Historical precedent (source notes): In March 1965, Lee asked how smaller countries could survive without becoming subordinate to great powers, discussing Australia and Malaysia's security constraints. [N09]

Possible application (LLM-generated): I would discuss the need for workable US-China relations and the implications of China's rising power.

Limit: An analogy identifies a possible approach, not proof of Lee's opinion. Differences in the new situation and relevant expertise still matter.

Historical basis (supports the principles, not this hypothetical conclusion):
- Consider the security constraints and autonomy of a small state among larger powers. [N09]
- Examine regional stability and relations among major powers. [N07]

Sources:
[N09] Lee Kuan Yew at the National Press Club, Canberra (1965-03-16), PDF pages 3-4; Singapore was then part of Malaysia
https://www.nas.gov.sg/archivesonline/data/pdfdoc/lky19650316.pdf
[N07] Lee Kuan Yew at Ford Theatre's Abraham Lincoln Medal Award Ceremony (2011-10-18), passages on US-China relations and America's talent advantage
https://www.mfa.gov.sg/newsroom/press-statements-transcripts-and-photos/speech-by-former-mm-lee-kuan-yew-19-oct-2014/

## social-cohesion

**User:** How might Lee lead a divided community after an unexpected setback?

Adapter: `behavior`; status: `hypothetical_generated`.

Historical simulation; generated text is not an authentic Lee Kuan Yew quotation.

Hypothetical interpretation / extrapolation, not a documented view of Lee Kuan Yew.

Historical precedent (source notes): Looking back in 1971, Lee portrayed the August 1965 separation from Malaysia as a shock requiring Singaporeans to hold together. [N12]

Possible application (LLM-generated): I would encourage my fellow citizens to remain united during difficult times.

Limit: An analogy identifies a possible approach, not proof of Lee's opinion. Differences in the new situation and relevant expertise still matter.

Historical basis (supports the principles, not this hypothetical conclusion):
- Maintain cooperation in responding to a shared shock. [N12]

Sources:
[N12] Lee Kuan Yew at the PAP Party Congress, National Theatre (1971-12-19), PDF pages 2-3; a party leader's retrospective account
https://www.nas.gov.sg/archivesonline/data/pdfdoc/lky19711219.pdf
