#!/usr/bin/env python3
"""Generate forms for human evaluation."""

import os
import json
import argparse

from jinja2 import FileSystemLoader, Environment

DEFAULT_TEMPLATE_PATH = "./templates"
DEFAULT_S3_BUCKET = "https://debaterecords.s3.amazonaws.com"
DEFAULT_SHEET_URL = "https://script.google.com/macros/s/AKfycby4yVMejSjiW8bSUyODIY8lvW6Sf-UWqudpjHpQULUfFSqTvOsVIshdepIndj3vbOJq0w/exec"
SAVE_ROOT = "forms"

QLIST = [
    # "The most impressive / surprise / persuasive points of the for side.",
    # "The most impressive / surprise / persuasive points of the against side.",
    # "The performance of the opening / rebuttal / closing statement of each side. Anything to improve?",
    # "The quality of the proposed claims, the rebuttal actions, the summarization, etc.",
    # "How do you track the debate flow during the listening?",
    "Based on this debate between two AI systems, what specific improvements would strengthen their debate performance?",
    "Which factors were most crucial in your assessment?",
    "How long did you spend on this evaluation?",
]


def get_options():
    parser = argparse.ArgumentParser(description="Create the debate evaluation form.")
    parser.add_argument("--mode", default="pair", choices=["scalar", "pair"], help="The type of form to create.")
    parser.add_argument("--target", default="common", choices=["common", "expert", "admin", "comparison", "mixed"], help="The type of audience")
    parser.add_argument("--version", default="1007", help="The version of the form.")
    parser.add_argument("--pair_stage", default="rebuttal_for", help="The stage to pair the form. all means all stages and sides")
    parser.add_argument("--early_stop", action="store_true", help="Early stop the form.")
    args = parser.parse_args()
    return args

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
        for stage in ["opening", "rebuttal", "closing"]:
            c["transcript"][stage] = {"for": [], "against": []}

        for data in data_list:
            process = data["debate_process"]
            for p in process:
                stage = p["stage"]
                side = p["side"]
                text = p["content"].replace("\n", "<br>").replace("\\", "")
                if len(data_list) == 1:
                    c["transcript"][stage][side] = text
                else:
                    c["transcript"][stage][side].append(text)
        

    return cases
    

# def create_scalar_evaluation_form(version, id, motion, questions, addition_questions=None):
#     loader = FileSystemLoader(searchpath=DEFAULT_TEMPLATE_PATH)
#     env = Environment(loader=loader)
#     template = env.get_template("mos.html.jinja2")

#     html = template.render(
#         page_title="Debate Performance Evaluation",
#         type="scalar",
#         version=version,
#         form_url=DEFAULT_SHEET_URL,
#         form_id=id,
#         motion=motion,
#         questions=questions,
#         addition_questions=addition_questions 
#     )

#     return html

def create_pairwise_comparison_form(version, id, motion, questions, addition_questions=None, target="expert"):
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


def create_question_form(args, case, motion, target_stage=None, target_side=None, assigned_stance=None):
    c = case

    qid = 1
    questions = [{
        "title": f"Question {qid}: Pre-Vote Stage",
        "audio_paths": [],
        "description": f"Please choose your attitude towards the given motion before the debate begins.",
        "name": f"q{qid}",
        "stage": "Pre-Vote"
    }]
    qid += 1

    paired_stage_flag = False

    for stage in ["opening", "rebuttal", "closing"]:
        question = {
            "title": f"Question {qid}: {stage.capitalize()} Stage",
            "audio_paths": [],
            "description": f"After listening to the two statements in {stage.capitalize()} stage, please choose your attitude towards the given motion ({motion}) now",
            "transcript": [],
            "name": f"q{qid}",
            "stage": stage.capitalize()
        }

        if args.target == "comparison":
            question["audio_paths"] = [
                    ["For", f"{DEFAULT_S3_BUCKET}/audio_{args.version}/case{c['case_id']}/{stage}_for_a.mp3", "For", f"{DEFAULT_S3_BUCKET}/audio_{args.version}/case{c['case_id']}/{stage}_for_b.mp3"],
                    ["Against", f"{DEFAULT_S3_BUCKET}/audio_{args.version}/case{c['case_id']}/{stage}_against_a.mp3", "Against", f"{DEFAULT_S3_BUCKET}/audio_{args.version}/case{c['case_id']}/{stage}_against_b.mp3"],
                ]
            question["transcript"] = [c["transcript"][stage]["for"], c["transcript"][stage]["against"]]
        elif args.target == "mixed":

            assert assigned_stance is not None, "assigned_stance is required for mixed target"
            assert target_stage is not None, "target_stage is required for mixed target"
            assert target_side is not None, "target_side is required for mixed target"

            for_model = assigned_stance["for"]
            against_model = assigned_stance["against"]
            for_idx = 0 if for_model == "a" else 1
            against_idx = 0 if against_model == "a" else 1
            if target_stage == stage:
                if target_side == "for":
                    question["audio_paths"] = [
                        ["For", f"{DEFAULT_S3_BUCKET}/audio_{args.version}/case{c['case_id']}/{stage}_for_a.mp3", "For", f"{DEFAULT_S3_BUCKET}/audio_{args.version}/case{c['case_id']}/{stage}_for_b.mp3"],
                        ["Against", f"{DEFAULT_S3_BUCKET}/audio_{args.version}/case{c['case_id']}/{stage}_against_{against_model}.mp3"],
                    ]
                    question["transcript"] = [c["transcript"][stage]["for"], c["transcript"][stage]["against"][against_idx]]
                    if args.early_stop:
                        question["audio_paths"] = question["audio_paths"][:-1]
                        question["transcript"] = question["transcript"][:-1]
                else:
                    question["audio_paths"] = [
                        ["For", f"{DEFAULT_S3_BUCKET}/audio_{args.version}/case{c['case_id']}/{stage}_for_{for_model}.mp3"],
                        ["Against", f"{DEFAULT_S3_BUCKET}/audio_{args.version}/case{c['case_id']}/{stage}_against_a.mp3", "Against", f"{DEFAULT_S3_BUCKET}/audio_{args.version}/case{c['case_id']}/{stage}_against_b.mp3"],
                    ]
                    question["transcript"] = [c["transcript"][stage]["for"][for_idx], c["transcript"][stage]["against"]]
                paired_stage_flag = True
            else:
                question["audio_paths"] = [
                    ["For", f"{DEFAULT_S3_BUCKET}/audio_{args.version}/case{c['case_id']}/{stage}_for_{for_model}.mp3"],
                    ["Against", f"{DEFAULT_S3_BUCKET}/audio_{args.version}/case{c['case_id']}/{stage}_against_{against_model}.mp3"],
                ]
                question["transcript"] = [c["transcript"][stage]["for"][for_idx], c["transcript"][stage]["against"][against_idx]]
        else:
            question["audio_paths"] = [
                ["For", f"{DEFAULT_S3_BUCKET}/audio_{args.version}/case{c['case_id']}/{stage}_for.mp3"],
                ["Against", f"{DEFAULT_S3_BUCKET}/audio_{args.version}/case{c['case_id']}/{stage}_against.mp3"],
            ]

        questions.append(question)
        qid += 1

        if args.target == "mixed" and args.early_stop and paired_stage_flag:
            break


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

    save_dir = f"{SAVE_ROOT}/{args.version}/{args.target}/"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    else:
        print(f"Directory {save_dir} already exists. Clear it first.")
        os.system(f"rm -r {save_dir}/*")

    print("Generating ...")
    cases = load_case(args.version, args.mode)
    for c in cases:
        motion = c["name"].replace("_", " ").title()
        pair_stage = args.pair_stage if "paired_stage" not in c else c["paired_stage"]
        if pair_stage == "all":
            target_stage, target_side = "all", "all"
        else:
            target_stage, target_side =pair_stage.split("_")
        
        if "assigned_stance" in c:
            assigned_stance = c["assigned_stance"]
        else:
            assigned_stance = {"for": "b", "against": "a"}  # a is baseline, b is test
        
        
        if args.target == "mixed" and target_stage == "all":
            ori_case_id = c["case_id"]
            for target_stage in ["opening", "rebuttal", "closing"]:
                for target_side in ["for", "against"]:
                    new_case_id = f"{ori_case_id}_{target_stage}_{target_side}"
                    questions, addition_questions = create_question_form(args, c, motion, target_stage, target_side, assigned_stance)
                    html = create_pairwise_comparison_form(args.version, new_case_id, 
                                                    motion=motion, 
                                                    questions=questions, 
                                                    addition_questions=addition_questions,
                                                    target=args.target)
                    with open(f"{save_dir}/{new_case_id}.html", "w") as f:
                        f.write(html)
                    print(f"Saved {new_case_id}.html")
        else:
            questions, addition_questions = create_question_form(args, c, motion, target_stage, target_side, assigned_stance)
            html = create_pairwise_comparison_form(args.version, c["case_id"], 
                                                    motion=motion, 
                                                    questions=questions, 
                                                    addition_questions=addition_questions,
                                                    target=args.target)

            with open(f"{save_dir}/{c['case_id']}.html", "w") as f:
                f.write(html)
            print(f"Saved {c['case_id']}.html")

    print("Done!")

if __name__ == "__main__":
    main()
