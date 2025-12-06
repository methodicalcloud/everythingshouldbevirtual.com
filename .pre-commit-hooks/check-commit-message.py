#!/usr/bin/env python3
"""
Pre-commit hook to block AI tool references in commit messages.

This hook prevents commits that contain references to AI tools like Claude,
Codex, Gemini, etc. while allowing clean development workflow.
"""

import re
import sys
from pathlib import Path


def check_commit_message(commit_msg_file):
    """Check commit message for AI tool references."""

    # Read the commit message
    try:
        with open(commit_msg_file, "r", encoding="utf-8") as f:
            commit_message = f.read()
    except Exception as e:
        print(f"Error reading commit message file: {e}")
        return 1

    # Patterns to block (case-insensitive)
    blocked_patterns = [
        # Claude specific
        r"claude\s+code",
        r"co-authored-by:\s*claude",
        r"noreply@anthropic\.com",
        r"generated\s+with\s+\[?claude",
        # Other AI tools
        r"\bcodex\b",
        r"\bgemini\b",
        r"\bchatgpt\b",
        r"\bgpt-4\b",
        r"\bcopilot\b",
        # Generic AI patterns
        r"🤖\s*generated\s+with",
        r"ai\s+generated",
        r"generated\s+by\s+ai",
        r"@openai\.com",
        r"@anthropic\.com",
        # Common AI assistance phrases
        r"with\s+ai\s+assistance",
        r"ai\s+assisted",
        r"generated\s+using\s+ai",
    ]

    # Check each pattern
    violations = []
    for pattern in blocked_patterns:
        matches = re.finditer(pattern, commit_message, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            violations.append(
                {
                    "pattern": pattern,
                    "match": match.group(),
                    "line": commit_message[: match.start()].count("\n") + 1,
                }
            )

    # Report violations
    if violations:
        print("🚫 COMMIT BLOCKED: AI tool references detected in commit message")
        print("")
        print("The following AI tool references were found:")
        for violation in violations:
            print(f"  Line {violation['line']}: '{violation['match']}'")

        print("")
        print("To maintain clean commit history, please remove AI tool references.")
        print("Common patterns to avoid:")
        print("  • Claude Code, Co-Authored-By: Claude")
        print("  • Generated with [tool name]")
        print("  • AI tool names (Codex, Gemini, ChatGPT, etc.)")
        print("  • 🤖 Generated with [tool]")
        print("")
        print("To bypass this check (if absolutely necessary):")
        print("  git commit --no-verify")

        return 1

    return 0


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: check-commit-message.py <commit-msg-file>")
        return 1

    commit_msg_file = sys.argv[1]

    if not Path(commit_msg_file).exists():
        print(f"Error: Commit message file '{commit_msg_file}' not found")
        return 1

    return check_commit_message(commit_msg_file)


if __name__ == "__main__":
    sys.exit(main())
