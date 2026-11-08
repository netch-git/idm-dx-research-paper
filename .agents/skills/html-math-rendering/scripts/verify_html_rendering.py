#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML Math Rendering Verification & Auto-Fix Script
IDM-DX Research Project Governance Tool

Usage:
    python verify_html_rendering.py <path_to_html_file> [--fix]
"""

import sys
import os
import re
import argparse

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Common LaTeX to Unicode replacements
LATEX_TO_UNICODE = [
    # Greek letters
    (r'\\alpha', 'α'),
    (r'\\beta', 'β'),
    (r'\\gamma', 'γ'),
    (r'\\delta', 'δ'),
    (r'\\epsilon', 'ε'),
    (r'\\zeta', 'ζ'),
    (r'\\eta', 'η'),
    (r'\\theta', 'θ'),
    (r'\\lambda', 'λ'),
    (r'\\mu', 'μ'),
    (r'\\sigma', 'σ'),
    (r'\\tau', 'τ'),
    (r'\\chi', 'χ'),
    (r'\\omega', 'ω'),
    (r'\\Delta', 'Δ'),
    (r'\\Sigma', 'Σ'),
    
    # Operators and relations
    (r'\\ge\b|\\geq\b', '≥'),
    (r'\\le\b|\\leq\b', '≤'),
    (r'\\ne\b|\\neq\b', '≠'),
    (r'\\pm\b', '±'),
    (r'\\times\b', '×'),
    (r'\\div\b', '÷'),
    (r'\\approx\b', '≈'),
    
    # Superscripts
    (r'\^2\b|\^{2}', '²'),
    (r'\^3\b|\^{3}', '³'),
    (r'\^(\d+)', r'<sup>\1</sup>'),
    
    # Subscripts
    (r'_\{?([a-zA-Z0-9]+)\}?', r'<sub>\1</sub>'),
    
    # Text commands
    (r'\\text\{([^}]+)\}', r'\1'),
    (r'\\overline\{([^}]+)\}', r'\1̄'),
]


def check_and_clean_latex(text: str) -> str:
    """Clean inside $...$ content to pure unicode."""
    cleaned = text
    for pattern, repl in LATEX_TO_UNICODE:
        cleaned = re.sub(pattern, repl, cleaned)
    # Remove remaining backslashes if any
    cleaned = cleaned.replace('\\', '')
    return cleaned.strip()


def verify_file(filepath: str, auto_fix: bool = False) -> bool:
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern for inline latex: $...$ but not escaped (\$ or currency like $100 without math)
    # Typically $ followed by non-space, non-dollar, containing backslash or letters, closed by $
    # Also \begin{...} or \(...\)
    latex_pattern = re.compile(r'(?<!\\)\$([^$\n]+?)(?<!\\)\$')
    backslash_pattern = re.compile(r'\\(alpha|beta|gamma|eta|chi|mu|sigma|ge|le|neq|pm|times)')

    lines = content.splitlines()
    issues = []

    in_script = False
    in_style = False

    for line_idx, line in enumerate(lines, 1):
        # Handle script and style tag state transitions
        if '<script' in line:
            in_script = True
        if '</script>' in line:
            in_script = False
            continue
        if '<style' in line:
            in_style = True
        if '</style>' in line:
            in_style = False
            continue
        if in_script or in_style:
            continue

        # Find $...$ occurrences
        matches = latex_pattern.findall(line)
        for match in matches:
            # Check if it looks like a math/stats expression (contains greek, operators, or letters like N, p, GAP)
            if any(k in match for k in ['\\', 'alpha', 'beta', 'eta', 'chi', 'ge', 'le', 'N =', 'p <', 'GAP', 'dissonance', '^', '_']):
                suggested = check_and_clean_latex(match)
                issues.append({
                    'line_num': line_idx,
                    'raw': f"${match}$",
                    'clean': suggested,
                    'line_text': line.strip()
                })

    if not issues:
        print(f"[SUCCESS] No raw LaTeX notations found in: {filepath}")
        return True

    print(f"\n[FOUND ISSUES] Found {len(issues)} raw LaTeX math expressions in {filepath}:")
    print("-" * 75)
    for issue in issues:
        print(f"Line {issue['line_num']:4d}: {issue['raw']:25s}  -->  Suggested: {issue['clean']}")
    print("-" * 75)

    if auto_fix:
        print("\n[ACTION] Applying auto-fixes...")
        fixed_content = content
        for issue in issues:
            fixed_content = fixed_content.replace(issue['raw'], issue['clean'])

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"[COMPLETE] Auto-fix applied successfully to {filepath}!")
        return True
    else:
        print("\nRun with --fix to automatically replace these with clean Unicode.")
        return False


def main():
    parser = argparse.ArgumentParser(description="Verify and fix LaTeX math rendering in HTML files.")
    parser.add_argument("html_file", help="Path to the HTML file to inspect")
    parser.add_argument("--fix", action="store_true", help="Automatically replace raw LaTeX with clean Unicode")
    args = parser.parse_args()

    success = verify_file(args.html_file, auto_fix=args.fix)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
