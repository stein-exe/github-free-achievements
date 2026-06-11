

import requests
import time
import base64
from datetime import datetime

# ─── CONFIG ──────────────────────────────────────────────────────────────────
GITHUB_TOKEN = "ghp_yourtokenhere"  # REPLACE with your GitHub Personal Access Token (with repo permissions)
OWNER        = "your-github-username"  # REPLACE with your GitHub username
REPO         = "your-repo-name"  # REPLACE with your repository name , make a fake one quickly

# Optional co-author for the Pair Extraordinaire achievement. Format: "Name <email>"
CO_AUTHOR='AnotherYou <another-account@users.noreply.github.com>'
BASE_URL='https://api.github.com'
rest_headers={'Authorization':f"token {GITHUB_TOKEN}",'Accept':'application/vnd.github.v3+json'}
graphql_headers={'Authorization':f"bearer {GITHUB_TOKEN}",'Content-Type':'application/json'}
def gql(query:str,variables:dict=None)->dict:
	payload={'query':query}
	if variables:payload['variables']=variables
	r=requests.post('https://api.github.com/graphql',headers=graphql_headers,json=payload);r.raise_for_status();data=r.json()
	if data.get('errors'):raise RuntimeError(f"GraphQL error: {data['errors']}")
	return data['data']
def initialize_repo_if_empty(branch:str)->bool:
	'Creates an initial commit if the repo has no commits yet. Returns True if initialized.';r=requests.get(f"{BASE_URL}/repos/{OWNER}/{REPO}/git/refs",headers=rest_headers)
	if r.status_code==200 and r.json():return False
	print('  ℹ️  Repo is empty — creating initial commit…');content_b64=base64.b64encode(b'# free-achievments\n\nGitHub achievement farming repo.\n').decode();r2=requests.put(f"{BASE_URL}/repos/{OWNER}/{REPO}/contents/README.md",headers=rest_headers,json={'message':'Initial commit','content':content_b64,'branch':branch})
	if r2.status_code in(200,201):print('  ✅ Initial commit created');return True
	print(f"  ❌ Init commit failed: {r2.status_code} {r2.text[:200]}");return False
def get_default_branch()->tuple[str,str]:'Returns (branch_name, head_sha). Initializes repo if empty.';r=requests.get(f"{BASE_URL}/repos/{OWNER}/{REPO}",headers=rest_headers);r.raise_for_status();branch=r.json()['default_branch'];initialize_repo_if_empty(branch);r2=requests.get(f"{BASE_URL}/repos/{OWNER}/{REPO}/git/ref/heads/{branch}",headers=rest_headers);r2.raise_for_status();return branch,r2.json()['object']['sha']
def create_branch(name:str,sha:str)->bool:r=requests.post(f"{BASE_URL}/repos/{OWNER}/{REPO}/git/refs",headers=rest_headers,json={'ref':f"refs/heads/{name}",'sha':sha});ok=r.status_code==201;print(f"  {'✅'if ok else'❌'} Branch '{name}': {r.status_code}");return ok
def get_file(path:str,branch:str)->dict|None:r=requests.get(f"{BASE_URL}/repos/{OWNER}/{REPO}/contents/{path}",headers=rest_headers,params={'ref':branch});return r.json()if r.status_code==200 else None
def commit_file(path:str,message:str,content:str,branch:str,file_sha:str=None)->bool:
	payload={'message':message,'content':base64.b64encode(content.encode()).decode(),'branch':branch}
	if file_sha:payload['sha']=file_sha
	r=requests.put(f"{BASE_URL}/repos/{OWNER}/{REPO}/contents/{path}",headers=rest_headers,json=payload);ok=r.status_code in(200,201);print(f"  {'✅'if ok else'❌'} Commit '{path}': {r.status_code}")
	if not ok:print(f"     {r.text[:200]}")
	return ok
def create_pr(title:str,body:str,head:str,base:str)->int|None:
	r=requests.post(f"{BASE_URL}/repos/{OWNER}/{REPO}/pulls",headers=rest_headers,json={'title':title,'body':body,'head':head,'base':base})
	if r.status_code==201:pr=r.json();print(f"  ✅ PR #{pr['number']} created → {pr['html_url']}");return pr['number']
	print(f"  ❌ PR creation failed {r.status_code}: {r.text[:200]}");return None
def merge_pr(pr_number:int)->bool:
	time.sleep(2);r=requests.put(f"{BASE_URL}/repos/{OWNER}/{REPO}/pulls/{pr_number}/merge",headers=rest_headers,json={'merge_method':'merge'});ok=r.status_code==200;print(f"  {'✅'if ok else'❌'} Merge PR #{pr_number}: {r.status_code}")
	if not ok:print(f"     {r.text[:200]}")
	return ok
def achievement_quickdraw():
	'Open an issue and close it immediately (within 5 minutes).';print('\n⚡ QUICKDRAW ─────────────────────────');r=requests.post(f"{BASE_URL}/repos/{OWNER}/{REPO}/issues",headers=rest_headers,json={'title':'Quick test issue','body':'Farming Quickdraw achievement.'})
	if r.status_code!=201:print(f"  ❌ Issue creation failed: {r.status_code} {r.text[:200]}");return
	issue_number=r.json()['number'];print(f"  ✅ Issue #{issue_number} created");r2=requests.patch(f"{BASE_URL}/repos/{OWNER}/{REPO}/issues/{issue_number}",headers=rest_headers,json={'state':'closed'});print(f"  {'✅'if r2.status_code==200 else'❌'} Issue #{issue_number} closed")
def make_pr_and_merge(label:str,base_branch:str,base_sha:str,commit_message:str)->bool:
	'Generic helper: branch → commit → PR → merge. Returns True on success.';ts=datetime.now().strftime('%Y%m%d%H%M%S%f');branch=f"auto/{label.lower().replace(' ','-')}-{ts}"
	if not create_branch(branch,base_sha):return False
	readme=get_file('README.md',branch)
	if readme:current=base64.b64decode(readme['content']).decode(errors='replace');new_content=current.rstrip('\n')+f"\n<!-- auto-update {ts} -->\n";ok=commit_file('README.md',commit_message,new_content,branch,readme['sha'])
	else:ok=commit_file(f"notes/update-{ts}.txt",commit_message,f"Automated update at {datetime.now().isoformat()}\n",branch)
	if not ok:return False
	pr_num=create_pr(f"[Auto] {label}",'Automated PR for GitHub achievement.',branch,base_branch)
	if not pr_num:return False
	return merge_pr(pr_num)
def achievement_yolo(base_branch:str,base_sha:str)->str:'YOLO: merge a PR without requesting a review.';print('\n🤠 YOLO ──────────────────────────────');make_pr_and_merge('YOLO',base_branch,base_sha,'chore: automated YOLO commit');_,new_sha=get_default_branch();return new_sha
def achievement_pair_extraordinaire(base_branch:str,base_sha:str)->str:'Pair Extraordinaire: PR with a co-authored commit.';print('\n👥 PAIR EXTRAORDINAIRE ───────────────');commit_msg=f"chore: co-authored update\n\nCo-authored-by: {CO_AUTHOR}";make_pr_and_merge('Pair-Extraordinaire',base_branch,base_sha,commit_msg);_,new_sha=get_default_branch();return new_sha
def achievement_pull_shark_extras(base_branch:str,base_sha:str,count:int=1):
	'Extra merged PRs to push Pull Shark counter higher.'
	for i in range(1,count+1):print(f"\n🦈 PULL SHARK extra #{i} ─────────────────");make_pr_and_merge(f"Pull-Shark-{i}",base_branch,base_sha,f"chore: pull shark run #{i}");_,base_sha=get_default_branch()
def achievement_galaxy_brain():
	'Galaxy Brain: create Q&A discussion, post answer, mark accepted.';print('\n🧠 GALAXY BRAIN ──────────────────────');r=requests.patch(f"{BASE_URL}/repos/{OWNER}/{REPO}",headers=rest_headers,json={'has_discussions':True});print(f"  {'✅'if r.status_code==200 else'⚠️ '} Discussions enabled: {r.status_code}");repo_data=gql('\n        query($owner: String!, $name: String!) {\n          repository(owner: $owner, name: $name) {\n            id\n            discussionCategories(first: 15) {\n              nodes { id name isAnswerable }\n            }\n          }\n        }\n        ',{'owner':OWNER,'name':REPO});repo_id=repo_data['repository']['id'];categories=repo_data['repository']['discussionCategories']['nodes'];qa_cat=next((c for c in categories if c['isAnswerable']),None)
	if not qa_cat:print('  ❌ No Q&A category found. Enable Discussions on the repo first.');return
	print(f"  ✅ Using category: {qa_cat['name']}");disc_data=gql('\n        mutation($repoId: ID!, $catId: ID!, $title: String!, $body: String!) {\n          createDiscussion(input: {\n            repositoryId: $repoId, categoryId: $catId,\n            title: $title, body: $body\n          }) { discussion { id url } }\n        }\n        ',{'repoId':repo_id,'catId':qa_cat['id'],'title':'How can I contribute to open source?','body':'I want to start contributing to open source projects. Any tips?'});discussion_id=disc_data['createDiscussion']['discussion']['id'];discussion_url=disc_data['createDiscussion']['discussion']['url'];print(f"  ✅ Discussion created → {discussion_url}");comment_data=gql('\n        mutation($discId: ID!, $body: String!) {\n          addDiscussionComment(input: { discussionId: $discId, body: $body }) {\n            comment { id }\n          }\n        }\n        ',{'discId':discussion_id,'body':'Start small: pick a project you use, read CONTRIBUTING.md, fix a docs typo or a small bug, and open a pull request. Consistency matters more than the size of your first contribution!'});comment_id=comment_data['addDiscussionComment']['comment']['id'];print('  ✅ Answer posted');gql('\n        mutation($commentId: ID!) {\n          markDiscussionCommentAsAnswer(input: { id: $commentId }) {\n            discussion { id }\n          }\n        }\n        ',{'commentId':comment_id});print('  ✅ Answer marked as accepted → Galaxy Brain!')
def achievement_heart_on_sleeve():
	'Heart On Sleeve: give ❤️ reactions on 10+ issues/PRs.';print('\n❤️  HEART ON SLEEVE ───────────────────');r=requests.get(f"{BASE_URL}/repos/{OWNER}/{REPO}/issues",headers=rest_headers,params={'state':'all','per_page':50});r.raise_for_status();existing=[item['number']for item in r.json()];print(f"  Found {len(existing)} existing issue/PR numbers: {existing}");needed=max(0,10-len(existing))
	for i in range(needed):
		rc=requests.post(f"{BASE_URL}/repos/{OWNER}/{REPO}/issues",headers=rest_headers,json={'title':f"Reaction target #{i+1}",'body':'Temporary issue for Heart on Sleeve.'})
		if rc.status_code==201:num=rc.json()['number'];existing.append(num);print(f"  ✅ Created issue #{num}")
	react_headers={**rest_headers,'Accept':'application/vnd.github.squirrel-girl-preview+json'};count=0
	for num in existing[:max(10,len(existing))]:
		rr=requests.post(f"{BASE_URL}/repos/{OWNER}/{REPO}/issues/{num}/reactions",headers=react_headers,json={'content':'heart'})
		if rr.status_code in(200,201):count+=1;print(f"  ❤️  Reacted to #{num} ({count})")
		else:print(f"  ⚠️  Reaction on #{num}: {rr.status_code}")
		time.sleep(.3)
	print(f"  {'✅'if count>=10 else'⚠️ '} Total heart reactions given: {count}")
def achievement_public_sighting():
	'Public Sighting: get @-mentioned in an issue/comment.';print('\n👀 PUBLIC SIGHTING ────────────────────');r=requests.post(f"{BASE_URL}/repos/{OWNER}/{REPO}/issues",headers=rest_headers,json={'title':'Shoutout to the maintainer','body':f"Big thanks to @{OWNER} for maintaining this repo! 🎉\n\nKeep up the great work."})
	if r.status_code==201:print(f"  ✅ Issue #{r.json()['number']} created with @{OWNER} mention → {r.json()['html_url']}")
	else:print(f"  ❌ Failed: {r.status_code} {r.text[:200]}")
def achievement_first_interaction():
	'First Interaction: post a comment on any issue/PR.';print('\n💬 FIRST INTERACTION ──────────────────');r=requests.post(f"{BASE_URL}/repos/{OWNER}/{REPO}/issues/1/comments",headers=rest_headers,json={'body':'Great work on this repository! Looking forward to seeing more. 🚀'})
	if r.status_code==201:print(f"  ✅ Comment posted → {r.json()['html_url']}")
	else:print(f"  ⚠️  {r.status_code} {r.text[:200]}")
def achievement_open_source_heart(base_branch:str,base_sha:str)->str:
	'Open Source Heart / Open Sourcerer: PR into a repo with hacktoberfest topic.';print('\n🌱 OPEN SOURCE HEART ──────────────────');r=requests.put(f"{BASE_URL}/repos/{OWNER}/{REPO}/topics",headers={**rest_headers,'Accept':'application/vnd.github.mercy-preview+json'},json={'names':['hacktoberfest','open-source','automation']});print(f"  {'✅'if r.status_code==200 else'⚠️ '} Topics set (hacktoberfest): {r.status_code}");ts=datetime.now().strftime('%Y%m%d%H%M%S%f');branch=f"auto/hacktoberfest-{ts}"
	if create_branch(branch,base_sha):
		readme=get_file('README.md',branch)
		if readme:
			current=base64.b64decode(readme['content']).decode(errors='replace');new_content=current.rstrip('\n')+f"\n<!-- hacktoberfest update {ts} -->\n"
			if commit_file('README.md','chore: hacktoberfest contribution',new_content,branch,readme['sha']):
				pr_num=create_pr('[Hacktoberfest] Open Source Heart','Contributing to a hacktoberfest repo.',branch,base_branch)
				if pr_num:merge_pr(pr_num)
	_,new_sha=get_default_branch();return new_sha
def achievement_github_pages(base_branch:str,base_sha:str):
	'GitHub Pages: publish a website from the repo.';print('\n🌐 GITHUB PAGES ───────────────────────');html="<!DOCTYPE html>\n<html lang='en'>\n<head>\n  <meta charset='UTF-8'>\n  <title>free-achievments</title>\n</head>\n<body>\n  <h1>Hello from GitHub Pages 🚀</h1>\n  <p>Achievement unlocked!</p>\n</body>\n</html>\n";existing=get_file('index.html',base_branch);committed=commit_file('index.html','chore: add GitHub Pages index.html',html,base_branch,existing['sha']if existing else None)
	if not committed:print('  ⚠️  Could not commit index.html, trying to enable Pages anyway…')
	payload={'source':{'branch':base_branch,'path':'/'}};r=requests.post(f"{BASE_URL}/repos/{OWNER}/{REPO}/pages",headers={**rest_headers,'Accept':'application/vnd.github+json'},json=payload)
	if r.status_code in(201,409):print(f"  ✅ GitHub Pages enabled (status {r.status_code}) → https://{OWNER}.github.io/{REPO}/")
	else:
		r2=requests.put(f"{BASE_URL}/repos/{OWNER}/{REPO}/pages",headers={**rest_headers,'Accept':'application/vnd.github+json'},json=payload);print(f"  {'✅'if r2.status_code in(200,204)else'⚠️ '} Pages update: {r2.status_code}")
		if r2.status_code not in(200,204):print(f"     {r2.text[:300]}")
def count_merged_prs()->int:
	'Count total merged PRs in the repo (handles pagination).';total=0;page=1
	while True:
		r=requests.get(f"{BASE_URL}/repos/{OWNER}/{REPO}/pulls",headers=rest_headers,params={'state':'closed','per_page':100,'page':page});r.raise_for_status();items=r.json()
		if not items:break
		total+=sum(1 for pr in items if pr.get('merged_at'))
		if len(items)<100:break
		page+=1
	return total
def achievement_pull_shark_gold(base_branch:str,base_sha:str,target:int=128):
	'Pull Shark Gold + Maintainer + Mars: reach target merged PRs.';print(f"\n🦈🌕 PULL SHARK GOLD / MARS (target: {target} merged PRs) ──");current=count_merged_prs();print(f"  Currently merged PRs: {current}");needed=max(0,target-current);print(f"  Need to merge {needed} more PRs…");sha=base_sha
	for i in range(1,needed+1):
		ts=datetime.now().strftime('%Y%m%d%H%M%S%f');branch=f"auto/mass-pr-{ts}"
		if not create_branch(branch,sha):time.sleep(1);continue
		readme=get_file('README.md',branch)
		if readme:current_content=base64.b64decode(readme['content']).decode(errors='replace');new_content=current_content.rstrip('\n')+f"\n<!-- run {i} @ {ts} -->\n";ok=commit_file('README.md',f"chore: automated run #{i}",new_content,branch,readme['sha'])
		else:ok=commit_file(f"notes/run-{ts}.txt",f"chore: automated run #{i}",f"run {i} at {datetime.now().isoformat()}\n",branch)
		if not ok:time.sleep(1);continue
		pr_num=create_pr(f"[Auto] Run #{i}",f"Automated PR #{i} for Pull Shark Gold.",branch,base_branch)
		if pr_num:merge_pr(pr_num);_,sha=get_default_branch()
		if i%10==0:print(f"  ── Progress: {i}/{needed} PRs merged ──")
		time.sleep(.5)
	final=count_merged_prs();print(f"  ✅ Total merged PRs now: {final}")
def main():print('='*55);print('  🚀 GitHub Achievement Farmer — Full Run');print(f"  Repo: {OWNER}/{REPO}");print('='*55);default_branch,base_sha=get_default_branch();print(f"\nDefault branch : {default_branch}");print(f"HEAD SHA       : {base_sha[:12]}…");_,base_sha=get_default_branch();achievement_heart_on_sleeve();achievement_public_sighting();achievement_first_interaction();base_sha=achievement_open_source_heart(default_branch,base_sha);achievement_github_pages(default_branch,base_sha);_,base_sha=get_default_branch();achievement_pull_shark_gold(default_branch,base_sha,target=128);print('\n'+'='*55);print('  Done! New achievements targeted:');print('  ❤️  Heart on Sleeve       – 10+ heart reactions given');print('  👀 Public Sighting        – @stein-exe mentioned in issue');print('  💬 First Interaction      – comment posted');print('  🌱 Open Source Heart      – PR into hacktoberfest repo');print('  🌐 GitHub Pages           – site published');print('  🦈 Pull Shark Gold / Mars – 128 merged PRs total');print('='*55);print('\n⚠️  REVOKE YOUR TOKEN NOW at https://github.com/settings/tokens')
if __name__=='__main__':main()