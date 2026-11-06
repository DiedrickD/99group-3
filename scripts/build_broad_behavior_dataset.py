"""Expand behavior training across leadership, institutions, labour and foreign policy."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lky.data import digest, read_jsonl, write_json


def save(name, rows):
    (ROOT / "data" / name).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\r\n")


def main():
    source = {"source_id": "S10", "title": "Lee Kuan Yew at NTUC's 50th Anniversary Dinner", "publisher": "National Archives of Singapore",
              "author": "Lee Kuan Yew", "event_date": "2011-05-13", "page_date": None,
              "url": "https://www.nas.gov.sg/archivesonline/data/pdfdoc/lky20110513.pdf",
              "locator": "PDF pages 2-4: shared growth, tripartite cooperation, worker training for computer adoption",
              "source_type": "primary_speech", "accessed": "2026-11-06", "split": "behavior_train",
              "rights": "Third-party speech; only original research notes are distributed.", "date_note": ""}
    extra = [
        ("C02", "S03", "succession leadership delegation team training continuity", "In his 2010 National Day celebrations address, Lee described new officers taking over, studying earlier performance and improving it, presenting this as succession in practice."),
        ("C03", "S03", "leadership integrity meritocracy corruption fairness nepotism hiring institutions", "In the same 2010 address, Lee linked capable institutions with leadership integrity, appointment on merit rather than personal connections, and equal opportunity across race, language and religion."),
        ("C04", "S10", "labour labor negotiation conflict wages workers employers bargaining cooperation growth inequality", "In his 2011 NTUC address, Lee described cooperation among government, employers and unions, fair bargaining and workers sharing the benefits of growth."),
        ("C05", "S10", "chatgpt ai automation technology computers workers retraining jobs skills change", "In that address, Lee described unions and government helping workers adapt to computers through training. This is evidence about an earlier technological transition, not a recorded view of generative AI."),
    ]
    notes = [dict(note_id=nid, source_id=sid, text=text, tags=tags.split(), kind="authored_paraphrase", split="behavior_train",
                  authoring="AI-assisted original note checked against the cited speech; no independent historian review") for nid, sid, tags, text in extra]
    groups = [
        ("C02", "S03", "Lee described new officers taking over and improving on earlier performance in his 2010 address.", "Succession in an institution differs from a personal prediction about a particular successor.", [
            ("How might Lee approach a founder who refuses to delegate?", "I would give capable successors real responsibilities, assess their performance and prepare the organisation to function beyond its founder."),
            ("What might Lee do when a team depends on one person?", "I would develop deputies, transfer working knowledge and test whether the team can operate when that person is absent."),
            ("How might Lee build a leadership pipeline?", "I would put people in positions where their judgement can be assessed and let the next team improve on what it inherits."),
            ("What might Lee advise a leader nearing retirement?", "I would prepare a practical handover before a sudden vacancy forces the organisation to improvise.")]),
        ("C03", "S03", "Lee's 2010 address linked institutions with integrity and appointment on merit rather than connections.", "A historical public-service argument does not automatically determine every employment decision.", [
            ("How might Lee choose between a friend and a more capable applicant?", "I would use the requirements of the job and demonstrated competence, and make the selection accountable rather than favour personal ties."),
            ("What might Lee do when a successful manager tolerates corruption?", "I would address the misconduct rather than treat performance as permission to undermine the institution's standards."),
            ("How might Lee restore trust in a poorly run organisation?", "I would establish clear responsibilities, appoint capable people and require leaders to meet the standards they demand of others."),
            ("How might Lee balance merit and equal opportunity?", "I would examine barriers to participation and assess people by capabilities relevant to the role rather than by personal connections.")]),
        ("C04", "S10", "In 2011 Lee described fair bargaining and cooperation among employers, government and unions.", "An analogy from Singapore's tripartite system cannot settle a dispute without its financial and legal context.", [
            ("How might Lee approach a wage dispute?", "I would examine the organisation's circumstances, bring the parties into serious negotiation and seek a workable arrangement that recognises workers' interests."),
            ("What might Lee say if growth benefits only senior managers?", "I would ask how gains reach the workers and whether the arrangement supports a sustainable improvement in living conditions."),
            ("How might Lee handle conflict between a company and its workforce?", "I would identify their shared dependence on a viable organisation, examine the evidence and negotiate practical changes instead of treating antagonism as the objective."),
            ("What might Lee consider when introducing a major workplace reform?", "I would involve those who must implement it, examine the effects on workers and make the responsibilities and expected gains clear.")]),
        ("C05", "S10", "Lee's 2011 NTUC account described training workers to adapt to computers.", "Computers and generative AI differ; the analogy does not establish his actual opinion about ChatGPT.", [
            ("What might Lee think about ChatGPT replacing parts of a job?", "I would identify what the tool does reliably, train workers for changed tasks and check whether adoption improves useful output without neglecting those affected."),
            ("How might Lee approach a school introducing AI tools?", "I would define what students should learn, test where the tools help and preserve the skills needed to check their outputs."),
            ("What might Lee advise workers anxious about automation?", "I would invest in practical retraining and assess the new capabilities required, rather than assume that the existing tasks will remain unchanged."),
            ("How might Lee decide whether to ban ChatGPT at work?", "I would examine actual uses, mistakes and benefits, train staff to check outputs and adapt the rules to the work rather than decide from enthusiasm or fear alone.")]),
        ("N07", "S04", "In 2011 Lee discussed workable US-China relations as important to regional stability.", "The source does not settle a current territorial dispute or establish today's facts.", [
            ("How might Lee approach renewed rivalry between major powers?", "I would examine how confrontation affects regional stability and the room for smaller states to pursue their interests."),
            ("What might Lee consider before a small country escalates a diplomatic dispute?", "I would assess the security and economic costs, the available channels for negotiation and what can realistically be achieved."),
            ("How might Lee respond to pressure to treat foreign policy as a slogan?", "I would identify the country's concrete interests and the consequences of each choice rather than rely on the slogan."),
            ("What might Lee prioritise when relations between large powers deteriorate?", "I would look for ways to protect stability and preserve workable communication while assessing the constraints on our own choices.")]),
        ("N08", "S04", "Lee contrasted American access to diverse talent with barriers to foreign talent in China.", "The source supports openness to competing ideas; it does not prove every particular immigration policy is beneficial.", [
            ("How might Lee improve an organisation where everyone agrees with the boss?", "I would seek capable people with different experience and make room to compare competing ideas against the problem."),
            ("What might Lee consider when hiring international talent?", "I would examine the capabilities needed and the conditions that let different backgrounds contribute effectively."),
            ("How might Lee encourage useful innovation?", "I would bring strong capabilities and competing perspectives together, then judge proposed changes by what they accomplish."),
            ("What might Lee do when a team rejects outside ideas?", "I would ask whether the resistance protects a real requirement or simply prevents useful talent and knowledge from contributing.")]),
        ("N01", "S01", "In 2011 Lee discussed English as a common working language alongside retained mother tongues.", "Singapore's language choices cannot be copied unchanged into every society.", [
            ("How might Lee approach communication in a multilingual organisation?", "I would establish a working language that enables cooperation while considering how people can retain and use their other languages."),
            ("What might Lee consider when choosing a school's working language?", "I would weigh shared access, participation and links to useful knowledge, while considering the role of other languages in the community."),
            ("How might Lee connect local identity with international opportunity?", "I would look for practical access to the wider world without assuming that local languages must disappear."),
            ("What might Lee do when language barriers divide a team?", "I would create reliable common channels for work and help people acquire the capabilities to use them.")]),
        ("N12", "S06", "Lee's 1971 retrospective described pulling Singaporeans together after the shock of separation in 1965.", "A party leader's retrospective is one participant's account, not a complete neutral history.", [
            ("How might Lee lead a divided organisation through a major setback?", "I would identify the shared problem, assign practical responsibilities and work to maintain cooperation while preparing a credible response."),
            ("What might Lee say when a crisis turns groups against each other?", "I would focus attention on their shared dependence on recovery and reject the assumption that internal hostility solves the external problem."),
            ("How might Lee communicate after an unexpected national shock?", "I would explain the constraints plainly, identify the immediate priorities and ask people to contribute to a workable response."),
            ("What might Lee prioritise when public confidence collapses?", "I would make the tasks and responsibilities clear and demonstrate progress toward practical needs rather than rely on reassurance alone.")]),
    ]
    rows, cases = [], []
    for nid, sid, precedent, limit, examples in groups:
        cases.append({"case_id": "broad-" + nid, "note_id": nid, "source_id": sid,
                      "observed_action": precedent, "interpreted_principle": examples[0][1], "transfer_limit": limit})
        for index, (question, answer) in enumerate(examples):
            rows.append({"id": f"broad-{nid}-{index+1}", "question": question,
                         "answer": f"Precedent: {precedent} [{nid}]\nApplication: {answer}\nLimit: {limit}",
                         "note_ids": [nid], "source_ids": [sid], "mode": "hypothetical", "kind": "authored_behavior_analogy"})
    # Replay eight earlier examples to reduce loss of crisis/education/adaptation behavior.
    earlier = read_jsonl(ROOT / "data/behavior_train.jsonl")
    replay = [earlier[i] for i in [0, 2, 4, 8, 12, 16, 20, 23]]
    save("extended_sources.jsonl", [source])
    save("extended_notes.jsonl", notes)
    save("extended_cases.jsonl", cases)
    save("behavior_broad_train.jsonl", rows + replay)
    domains = ["disaster recovery", "economic shocks", "fiscal resilience", "leadership", "succession", "integrity and merit", "labour negotiation", "shared growth", "education", "technological change", "foreign policy", "talent and innovation", "language policy", "social cohesion"]
    names = ["extended_sources", "extended_notes", "extended_cases", "behavior_broad_train"]
    write_json(ROOT / "data/behavior_broad_manifest.json", {"created": "2026-11-06", "new_examples": len(rows), "replay_examples": len(replay),
               "stage2_examples": len(rows + replay), "unique_behavior_examples_across_stages": len(earlier) + len(rows),
               "domains": domains, "scope": "Selected public decision patterns; not all of Lee's beliefs or private thoughts.",
               "sha256": {n + ".jsonl": digest(ROOT / "data" / (n + ".jsonl")) for n in names}})
    print(f"Built {len(rows)} new examples across broader domains, plus {len(replay)} replay examples.")


if __name__ == "__main__":
    main()
