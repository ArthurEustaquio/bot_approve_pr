from github import Github

# Autenticação no GitHub usando um token

token = open('token.txt','r').read()
g = Github(token)

# Repositório específico
owner = 'ps-data-platform'
repo_name = 'kiruna-khronos-ci-cd-yml'

repo = g.get_repo(f"{owner}/{repo_name}")

# Listar todos os pull requests do repositório
pulls = repo.get_pulls(state='open')  # você pode definir 'state' como 'open', 'closed' ou 'all'

list_login = ['rvale', 'tqi_abertagnolli', 'dfsantos', 'pedsilva', 'ctl_aeustaquio']
# Iterar sobre os pull requests e exibir informações
for pull in pulls:
    if pull.user.login in list_login:
        if 'hillvalley_homolog' in pull.title:
            print(f"Pull Request #{pull.number}: {pull.title}")
            print(f"Autor: {pull.user.login}")
            print(f"URL: {pull.html_url}")
            pr_number = pull.number
            pr = repo.get_pull(pr_number)
            pr.create_review(event="APPROVE")
            pr.add_to_labels('dax_prod')
            print(f"Pull request #{pr_number} aprovado automaticamente!")
