import subprocess
import argparse
from collections import defaultdict
from datetime import datetime, timedelta


def get_git_blame(file_path, lines=[]):
    if len(lines) > 0:
        line_args = f"-L {lines[0]},{lines[1]}"
        command = ["git", "blame", "--line-porcelain", *line_args, file_path]
    else:
        command = ["git", "blame", "--line-porcelain", file_path]

    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.split("\n")


def parse_git_blame(blame_output):
    lines = []
    current_line = {}
    for line in blame_output:
        if line.startswith("\t"):
            if current_line:
                lines.append(current_line)
                current_line = {}
        elif " " in line:
            key, value = line.split(" ", 1)
            current_line[key] = value
    return lines


def analyze_file(file_path, age_threshold=None, lines=[]):
    blame_output = get_git_blame(file_path, lines)
    parsed_blame = parse_git_blame(blame_output)

    analysis = defaultdict(lambda: {"lines": 0, "last_modified": None})
    old_lines = []

    for line in parsed_blame:
        author = line.get("author", "Unknown")
        timestamp = int(line.get("author-time", "0"))
        date = datetime.fromtimestamp(timestamp)

        analysis[author]["lines"] += 1
        if (
            analysis[author]["last_modified"] is None
            or date > analysis[author]["last_modified"]
        ):
            analysis[author]["last_modified"] = date

        if age_threshold and date < datetime.now() - timedelta(
            days=365 * age_threshold
        ):
            old_lines.append(
                {
                    "line_number": line.get("line_number", "Unknown"),
                    "content": line.get("contents", "").strip(),
                    "author": author,
                    "date": date.strftime("%Y-%m-%d"),
                }
            )

    return dict(analysis), old_lines


"""
CLI options for the code review co-pilot
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Git file history")
    parser.add_argument("--file", type=str, help="File to analyze")
    parser.add_argument("--age", type=int, help="Age threshold in years")
    parser.add_argument("--api", action="store_true", help="Run as API server")
    parser.add_argument("--lines", type=int, nargs=2, help="Lines to analyze")
    args = parser.parse_args()

    analysis, old_lines = analyze_file(args.file, args.age)
    print("Author Analysis:")
    for author, data in analysis.items():
        print(f"{author}: {data['lines']} lines, last modified {data['last_modified']}")
    if old_lines:
        print("\nOld Lines:")
        for line in old_lines:
            print(
                f"Line {line['line_number']}: {line['content']} (by {line['author']} on {line['date']})"
            )
