#!/usr/bin/env python3
"""Generate forms for human evaluation."""

import os
import copy
import json
import random
import argparse

from jinja2 import FileSystemLoader, Environment

DEFAULT_TEMPLATE_PATH = "./templates"
DEFAULT_S3_BUCKET = "https://debaterecords.s3.amazonaws.com"
DEFAULT_SHEET_URL = "https://script.google.com/macros/s/AKfycbxK1mGaCBuSe0j6xvplXCkDM7W0LwAYsoOPd7ICKAYv0klYOnFUE4yzGzTxLvBtT6bbkg/exec"
SAVE_ROOT = "forms"

QLIST = [
    # "The most impressive / surprise / persuasive points of the for side.",
    # "The most impressive / surprise / persuasive points of the against side.",
    # "The performance of the opening / rebuttal / closing statement of each side. Anything to improve?",
    # "The quality of the proposed claims, the rebuttal actions, the summarization, etc.",
    # "How do you track the debate flow during the listening?",
    # "Based on this debate between two AI systems, what specific improvements would strengthen their debate performance?",
    "Which factors were most crucial in your assessment?",
    "How long did you spend on this evaluation?",
]

def get_options():
    parser = argparse.ArgumentParser(description="Create the debate evaluation form.")
    parser.add_argument("--mode", default="pair", choices=["single", "pair"], help="The type of form to create.")
    parser.add_argument("--target", default="common", choices=["common", "expert", "admin", "comparison", "mixed", "expr"], help="The type of audience")
    parser.add_argument("--version", default="1007", help="The version of the form.")
    parser.add_argument("--pair_stage", default="rebuttal_for", help="The stage to pair the form. all means all stages and sides")
    parser.add_argument("--every_k", default=1, type=int, help="The number of head-to-head comparisons.")
    parser.add_argument("--early_stop", action="store_true", help="Early stop the form.")
    args = parser.parse_args()
    return args

def check_and_save(name, html):
    if os.path.exists(name):
        print(f"File {name} already exists. Regenerating ...")
    
    with open(name, "w") as f:
        f.write(html)
    print(f"Saved {name}")


def get_sanity_check_questions(data, side, stage):
    if "debate_thoughts" not in data:
        return {}
    if stage == "opening":
        context = [p for p in data["debate_thoughts"][side] if p["mode"] == "choose_main_claims"]
        if len(context) == 0:
            return {}
        else:
            candidates = context[0]["ranked_claims"]
            correct = context[0]["selected_claims"]
            incorrect = [o for o in candidates if o not in correct]
            correct_answer = random.choice(correct)
            incorrect_answer = random.sample(incorrect, 3)
            options = [correct_answer] + incorrect_answer
            random.shuffle(options)
            options.append("None of the above")
            answer = options.index(correct_answer)
            question = {
                "title": f"Which claim is proposed by <strong>{side.capitalize()}</strong> side as one of its main claims during the opening statement? If multiple options apply, please choose the best one.",
                "options": options,
                "answer": answer,
                "stage": stage,
                "side": side,
                "type": "choice",
            }
            return question
    elif stage == "rebuttal":
        return {}
    else:
        return {
            "title": f"Which is the main battlefield / conflict / question mentioned by <strong>{side.capitalize()}</strong> side in its closing statement?",
            "stage": stage,
            "side": side,
            "type": "text",
        }

def load_case(version, mode):
    file = "assets/metadata.json"
    with open(file) as f:
        info = json.load(f)
    cases = info[version]
    cases = [case for case in cases if mode in case["mode"]]
    for c in cases:
        if isinstance(c["transcript"], str):
            c["transcript"] = [c["transcript"]]

        data_list = []
        for t in c["transcript"]:
            with open(t) as f:
                data = json.load(f)
                data_list.append(data)
        
        c["transcript"] = {}
        c["sanity_check_questions"] = {}
        for stage in ["opening", "rebuttal", "closing"]:
            c["transcript"][stage] = {"for": [], "against": []}
            c["sanity_check_questions"][stage] = {"for": [], "against": []}

        # may have multiple transcripts (output a and b)
        for data in data_list:
            process = data["debate_process"]
            for p in process:
                stage = p["stage"]
                side = p["side"]
                text = p["content"].replace("\n", "<br>").replace("\\", "")
                sanity_check_question = get_sanity_check_questions(data, side, stage)
                if len(data_list) == 1:
                    c["transcript"][stage][side] = text
                else:
                    c["transcript"][stage][side].append(text)
                
                if len(sanity_check_question) > 0:
                    c["sanity_check_questions"][stage][side].append(sanity_check_question)
                    
    return cases
    

def create_form(version, id, motion, questions, addition_questions=None, target="expert"):
    loader = FileSystemLoader(searchpath=DEFAULT_TEMPLATE_PATH)
    env = Environment(loader=loader)
    if target == "expert":
        template = env.get_template("expert.html.jinja2")
    elif target == "common":
        template = env.get_template("common.html.jinja2")
    elif target == "admin":
        template = env.get_template("admin.html.jinja2")
    elif target == "comparison":
        template = env.get_template("comparison.html.jinja2")
    elif target == "mixed":
        template = env.get_template("mixed.html.jinja2")
    elif target == "expr":
        template = env.get_template("expr.html.jinja2")
    else:
        raise ValueError(f"Unknown target: {target}")


    html = template.render(
        page_title="Debate Pairwise Comparison",
        type="pair",
        version=version,
        form_url=DEFAULT_SHEET_URL,
        form_id=id,
        motion=motion,
        questions=questions,
        addition_questions=addition_questions 
    )

    return html


def create_question_form(args, case, motion, head_to_head=None, assigned_stance=None):
    c = case
    reverse = c["reverse"] if "reverse" in c else False

    current_head_num = 0

    qid = 1
    questions = [{
        "title": f"Question {qid}: Pre-Vote Stage",
        "audio_paths": [],
        "description": f"Please choose your attitude towards the given motion before the debate begins.",
        "name": f"q{qid}",
        "stage": "Pre-Vote"
    }]
    qid += 1

    audio_root = f"{DEFAULT_S3_BUCKET}/audio_{args.version}/case{c['case_id']}"

    for stage in ["opening", "rebuttal", "closing"]:
        question = {
            "title": f"Question {qid}: {stage.capitalize()} Stage",
            "audio_paths": [],
            "description": f"After listening to the two statements in {stage.capitalize()} stage, please choose your attitude towards the given motion ({motion}) now",
            "transcript": [],
            "name": f"q{qid}",
            "stage": stage.capitalize(),
            "sanity_check": []
        }

        if args.target == "comparison":
            if reverse:
                question["audio_paths"] = [
                        ["For", f"{audio_root}/{stage}_for_b.mp3", "For", f"{audio_root}/{stage}_for_a.mp3"],
                        ["Against", f"{audio_root}/{stage}_against_b.mp3", "Against", f"{audio_root}/{stage}_against_a.mp3"],
                    ]
                question["transcript"] = [c["transcript"][stage]["for"][::-1], c["transcript"][stage]["against"][::-1]]
            else:
                question["audio_paths"] = [
                        ["For", f"{audio_root}/{stage}_for_a.mp3", "For", f"{audio_root}/{stage}_for_b.mp3"],
                        ["Against", f"{audio_root}/{stage}_against_a.mp3", "Against", f"{audio_root}/{stage}_against_b.mp3"],
                    ]
                question["transcript"] = [c["transcript"][stage]["for"], c["transcript"][stage]["against"]]
        
        elif args.target in ["mixed", "expr"]:
            assert assigned_stance is not None, "assigned_stance is required for mixed target"
            assert head_to_head is not None, "target_stage is required for mixed target"

            # baseline idx=0, test idx=1; a is baseline, b is test
            for_model = assigned_stance["for"]
            against_model = assigned_stance["against"]
            for_idx = 0 if for_model == "a" else 1
            against_idx = 0 if against_model == "a" else 1
            if stage in head_to_head:
                if "for" in head_to_head[stage]:
                    if reverse:
                        question["audio_paths"].append(["For", f"{audio_root}/{stage}_for_b.mp3", "For", f"{audio_root}/{stage}_for_a.mp3"])
                        question["transcript"].append(c["transcript"][stage]["for"][::-1])
                    else:
                        question["audio_paths"].append(["For", f"{audio_root}/{stage}_for_a.mp3", "For", f"{audio_root}/{stage}_for_b.mp3"])
                        question["transcript"].append(c["transcript"][stage]["for"])
                    current_head_num += 1
                else:
                    question["audio_paths"].append(["For", f"{audio_root}/{stage}_for_{for_model}.mp3"])
                    question["transcript"].append(c["transcript"][stage]["for"][for_idx])

                if "against" in head_to_head[stage]:
                    if reverse:
                        question["audio_paths"].append(["Against", f"{audio_root}/{stage}_against_b.mp3", "Against", f"{audio_root}/{stage}_against_a.mp3"])
                        question["transcript"].append(c["transcript"][stage]["against"][::-1])
                    else:
                        question["audio_paths"].append(["Against", f"{audio_root}/{stage}_against_a.mp3", "Against", f"{audio_root}/{stage}_against_b.mp3"])
                        question["transcript"].append(c["transcript"][stage]["against"])
                    current_head_num += 1
                else:
                    question["audio_paths"].append(["Against", f"{audio_root}/{stage}_against_{against_model}.mp3"])
                    question["transcript"].append(c["transcript"][stage]["against"][against_idx])
            else:
                question["audio_paths"] = [
                    ["For", f"{audio_root}/{stage}_for_{for_model}.mp3"],
                    ["Against", f"{audio_root}/{stage}_against_{against_model}.mp3"],
                ]
                question["transcript"] = [c["transcript"][stage]["for"][for_idx], c["transcript"][stage]["against"][against_idx]]
        
        else:
            question["audio_paths"] = [
                ["For", f"{audio_root}/{stage}_for.mp3"],
                ["Against", f"{audio_root}/{stage}_against.mp3"],
            ]
            question["transcript"] = [c["transcript"][stage]["for"], c["transcript"][stage]["against"]]

        if "sanity_check_questions" in c :
            if args.target in ["mixed", "expr"]:
                for side in ["for", "against"]:
                    if len(c["sanity_check_questions"][stage][side]) > 0:
                        sanity_check = copy.deepcopy(c["sanity_check_questions"][stage][side][-1])
                        if head_to_head is not None and stage in head_to_head and side in head_to_head[stage]:
                            # sanity check is always for our test output
                            if reverse:
                                sanity_check["title"] = sanity_check["title"].replace("by", f"by <strong>Output A's</strong>")
                            else:
                                sanity_check["title"] = sanity_check["title"].replace("by", f"by <strong>Output B's</strong>")
                            question["sanity_check"].append(sanity_check)
                        else:
                            if (side == "for" and for_model == "b") or (side == "against" and against_model == "b"):
                                question["sanity_check"].append(sanity_check)
            else:
                for side in ["for", "against"]:
                    if len(c["sanity_check_questions"][stage][side]) > 0:
                        sanity_check = copy.deepcopy(c["sanity_check_questions"][stage][side][-1])
                        if reverse:
                            sanity_check["title"] = sanity_check["title"].replace("by", f"by <strong>Output A's</strong>")
                        else:
                            sanity_check["title"] = sanity_check["title"].replace("by", f"by <strong>Output B's</strong>")
                        question["sanity_check"].append(sanity_check)





        questions.append(question)
        qid += 1

    if args.target in ["mixed", "expr"] and args.early_stop:
        # remove stage after the last head_to_head stage
        last_stage_flag = False
        for i in range(len(questions) - 1, -1, -1):
            if not last_stage_flag:
                if questions[i]["stage"].lower() not in head_to_head:
                    questions.pop(i)
                else:
                    last_stage_flag = True
                    if "against" not in head_to_head[questions[i]["stage"].lower()]:
                        # remove the against side
                        questions[i]["audio_paths"] = questions[i]["audio_paths"][:-1]
                        questions[i]["transcript"] = questions[i]["transcript"][:-1]
                        if len(questions[i]["sanity_check"]) > 0 and questions[i]["sanity_check"][-1]["side"] == "against":
                            questions[i]["sanity_check"] = questions[i]["sanity_check"][:-1]


    print([q["sanity_check"] for q in questions if "sanity_check" in q])

    addition_questions = []
    for q in QLIST:
        addition_questions.append({
            "title": f"(Optional) Question {qid}: {q}",
            "name": f"q{qid}",
            "type": "text",
        })
        qid += 1

    return questions, addition_questions

def main():
    args = get_options()

    save_dir = f"{SAVE_ROOT}/{args.version}/{args.target}"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # else:
    #     print(f"Directory {save_dir} already exists. Clear it first.")
    #     os.system(f"rm -r {save_dir}/*")

    print("Generating ...")
    cases = load_case(args.version, args.mode)
    for c in cases:
        motion = c["name"].replace("_", " ").title()
        pair_stage = args.pair_stage if "pair_stage" not in c else c["pair_stage"]
        if pair_stage == "all":
            if args.every_k == 1:
                head_to_head = [{stage: [side]} for stage in ["opening", "rebuttal", "closing"] for side in ["for", "against"]]
            elif args.every_k == 2:
                head_to_head = [{"opening": ["for", "against"]}, {"rebuttal": ["for", "against"]}, {"closing": ["for", "against"]}]
            elif args.every_k == 3:
                head_to_head = [{"opening": ["for", "against"], "rebuttal": ["for"]}, {"rebuttal": ["against"], "closing": ["for", "against"]}]
            else:
                raise ValueError(f"every_k must be 1, 2, or 3, but got {args.every_k}")
        else:
            target_stage, target_side = pair_stage.split("_")
            head_to_head = [{target_stage: [target_side]}]
        
        if "assigned_stance" in c:
            assigned_stance = c["assigned_stance"]
        else:
            assigned_stance = {"for": "b", "against": "a"}  # a is baseline, b is test
        
        
        if args.target in ["mixed", "expr"]:
            ori_case_id = c["case_id"]
            for idx, h2h in enumerate(head_to_head):
                name_all = f"T{args.every_k}_n{idx}"
                new_case_id = f"{ori_case_id}({name_all})"
                questions, addition_questions = create_question_form(args, c, motion, h2h, assigned_stance)
                html = create_form(args.version, new_case_id, 
                                                motion=motion, 
                                                questions=questions, 
                                                addition_questions=addition_questions,
                                                target=args.target)
                check_and_save(f"{save_dir}/{new_case_id}.html", html)
        else:
            questions, addition_questions= create_question_form(args, c, motion, head_to_head, assigned_stance)
            html = create_form(args.version, c["case_id"], 
                                                    motion=motion, 
                                                    questions=questions, 
                                                    addition_questions=addition_questions,
                                                    target=args.target)

            check_and_save(f"{save_dir}/{c['case_id']}.html", html)

    print("Done!")

if __name__ == "__main__":
    main()
