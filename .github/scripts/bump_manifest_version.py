#!/usr/bin/env python3
import json
import subprocess
import sys
import re
from pathlib import Path
import os

MANIFEST_PATH = Path('custom_components/bach_cantata/manifest.json')

def run(cmd):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode().strip()
    except subprocess.CalledProcessError as e:
        return None

def parse_version(v):
    m = re.match(r"v?(\d+)\.(\d+)\.(\d+)", v)
    if not m:
        return None
    return [int(m.group(1)), int(m.group(2)), int(m.group(3))]

def version_to_str(parts):
    return f"{parts[0]}.{parts[1]}.{parts[2]}"

def increment_version(parts, level):
    major, minor, patch = parts
    if level == 'major':
        return [major+1, 0, 0]
    if level == 'minor':
        return [major, minor+1, 0]
    if level == 'patch':
        return [major, minor, patch+1]
    return parts

# get latest tag
latest_tag = run(['git', 'describe', '--tags', '--abbrev=0'])

# get commits since latest_tag (if exists) else all commits
if latest_tag:
    log_range = f"{latest_tag}..HEAD"
else:
    log_range = None

if log_range:
    commits_raw = run(['git', 'log', log_range, '--pretty=format:%s%n%b%n==END=='])
else:
    commits_raw = run(['git', 'log', '--pretty=format:%s%n%b%n==END=='])

commits = []
if commits_raw:
    for chunk in commits_raw.split('==END=='):
        chunk = chunk.strip()
        if not chunk:
            continue
        lines = chunk.splitlines()
        header = lines[0].strip()
        body = '\n'.join(lines[1:]).strip()
        commits.append((header, body))

# determine bump level
level = None
for header, body in commits:
    # Breaking change in body
    if 'BREAKING CHANGE' in body or re.search(r"!\:", header) or re.search(r"\w+\(.*\)!", header):
        level = 'major'
        break
    # feat -> minor
    if re.match(r"^feat(\(|:|$)", header, re.IGNORECASE):
        if level != 'major':
            level = 'minor'
        continue
    # fix -> patch
    if re.match(r"^fix(\(|:|$)", header, re.IGNORECASE):
        if level not in ('major','minor'):
            level = 'patch'
        continue

# read current manifest version
if not MANIFEST_PATH.exists():
    print(f"bumped=false")
    print(f"reason=manifest_not_found")
    sys.exit(0)

with MANIFEST_PATH.open('r', encoding='utf-8') as f:
    manifest = json.load(f)

manifest_version = manifest.get('version', '0.0.0')
manifest_parts = parse_version(manifest_version) or [0,0,0]

# determine base version for bump (use latest tag if available, else manifest)
if latest_tag:
    tag_parts = parse_version(latest_tag) or manifest_parts
else:
    tag_parts = manifest_parts

if not level:
    # no relevant commits
    print("bumped=false")
    print("reason=no_relevant_commits")
    sys.exit(0)

new_parts = increment_version(tag_parts, level)
new_version = version_to_str(new_parts)
new_tag = f"v{new_version}"

# if tag already exists do nothing
existing_tag = run(['git', 'rev-parse', '--verify', new_tag])
if existing_tag:
    print("bumped=false")
    print("reason=tag_already_exists")
    print(f"tag_name={new_tag}")
    sys.exit(0)

# if manifest already at or above new_version, but tag missing we will still create tag
cmp_manifest = manifest_parts
if new_parts <= cmp_manifest:
    # manifest already up-to-date or newer; create tag only if missing
    create_tag = True
    update_manifest = False
else:
    create_tag = True
    update_manifest = True

# update manifest if needed
if update_manifest:
    manifest['version'] = new_version
    with MANIFEST_PATH.open('w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write('\n')

# commit, push, and create tag
# configure git
subprocess.check_call(['git', 'config', 'user.name', 'github-actions[bot]'])
subprocess.check_call(['git', 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com'])

if update_manifest:
    subprocess.check_call(['git', 'add', str(MANIFEST_PATH)])
    subprocess.check_call(['git', 'commit', '-m', f'chore(release): bump version to {new_version} [skip ci]'])
    # push the commit
    # Determine a fully-qualified ref to push to (preferred) to avoid "not a full refname" errors.
    push_ref = None
    github_ref = os.environ.get('GITHUB_REF', '')
    github_ref_name = os.environ.get('GITHUB_REF_NAME', '')
    if github_ref.startswith('refs/heads/'):
        branch = github_ref.split('/', 2)[2]
        push_ref = f'HEAD:refs/heads/{branch}'
    elif github_ref_name:
        push_ref = f'HEAD:refs/heads/{github_ref_name}'
    else:
        # Try to resolve the current branch name locally
        current_branch = run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        if current_branch and current_branch != 'HEAD':
            push_ref = f'HEAD:refs/heads/{current_branch}'

    try:
        if push_ref:
            subprocess.check_call(['git', 'push', 'origin', push_ref])
        else:
            subprocess.check_call(['git', 'push', 'origin', 'HEAD'])
    except subprocess.CalledProcessError:
        # Fallback: try a plain HEAD push to allow older setups to continue (will fail in some runner setups)
        subprocess.check_call(['git', 'push', 'origin', 'HEAD'])

# create and push tag
subprocess.check_call(['git', 'tag', new_tag])
subprocess.check_call(['git', 'push', 'origin', new_tag])

# output results
print(f"bumped=true")
print(f"new_version={new_version}")
print(f"tag_name={new_tag}")
print(f"reason=bumped_based_on_commits")

sys.exit(0)