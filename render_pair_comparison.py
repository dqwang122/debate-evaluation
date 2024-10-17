#!/usr/bin/env python3
"""Generate forms for human evaluation."""

from jinja2 import FileSystemLoader, Environment


def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("pair_comparison.html.jinja2")

    html = template.render(
        page_title="Debate Pairwise Comparison 1",
        form_url="http://localhost:8888",
        form_id=1,
        questions=[
            {
                "title": "Question 1",
                "audio_paths": [
                    "wavs/test1.wav",
                    "wavs/test2.wav"
                ],
                "name": "q1"
            },
            {
                "title": "Question 2",
                "audio_paths": [
                    "wavs/test3.wav",
                    "wavs/test4.wav"
                ],
                "name": "q2"
            },
        ]
    )
    print(html)


if __name__ == "__main__":
    main()
