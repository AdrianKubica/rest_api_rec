from __future__ import annotations
import requests

def url_composer(url_parts: List) -> str:
    return '/'.join(url_parts)

def get_auth(user: str, password: str) -> HTTPBasicAuth:
    auth = requests.auth.HTTPBasicAuth(
        username='',
        password=''
    )
    return auth

def get_fields(repo_data: Dict) -> Dict:
    repo_fields = {
        'full_name': 'fullName',
        'description': 'description',
        'clone_url': 'cloneUrl',
        'stargazers_count': 'stars',
        'created_at': 'createdAt'}
    return {repo_fields[key]: value for key, value in repo_data.items() if key in repo_fields.keys()}

def get_repo_data(base_url: str, owner: str, repo: str) -> Dict:
    with requests.Session() as session:
        # session.auth = get_auth()
        url = url_composer([base_url, owner, repo])
        res = requests.get(url)
        repo_data = res.json()    
        return get_fields(repo_data)
