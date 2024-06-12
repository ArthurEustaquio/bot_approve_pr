from github import Github

# Autenticação no GitHub usando um token
token = 'seu_token_aqui'
g = Github(token)

# Repositório específico
owner = 'nome_do_proprietario'
repo_name = 'nome_do_repositorio'

repo = g.get_repo(f"{owner}/{repo_name}")

# Listar todos os pull requests do repositório
pulls = repo.get_pulls(state='open')  # você pode definir 'state' como 'open', 'closed' ou 'all'

# Iterar sobre os pull requests e exibir informações
for pull in pulls:
    print(f"Pull Request #{pull.number}: {pull.title}")
    print(f"Autor: {pull.user.login}")
    print(f"URL: {pull.html_url}")
    print()
