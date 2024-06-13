import time

from github import Github

# Autenticação no GitHub usando um token

token = open('token.txt', 'r').read()
bank_txt = open('bank.txt', 'w').write('***********\n')
g = Github(token)

# Repositório específico
owner = 'ps-data-platform'
repo_name = 'kiruna-khronos-ci-cd-yml'

repo = g.get_repo(f"{owner}/{repo_name}")

list_login = ['RvaleAn',
              'tqiabertagnolli',
              'dilmaraferreira',
              'pedsilva',
              'ArthurEustaquio']

while True:
    # Listar todos os pull requests do repositório
    pulls = repo.get_pulls(state='open')  # você pode definir 'state' como 'open', 'closed' ou 'all'
    # Iterar sobre os pull requests e exibir informações
    for pull in pulls:
        if pull.user.login in list_login:
            if 'hillvalley_homolog' in pull.title:
                with open('bank.txt', 'r+') as bank_txt:
                    bank_txt_read = bank_txt.read()
                    if f"{pull.number}_{pull.merge_commit_sha}" not in bank_txt_read:
                        print(f"Pull Request #{pull.number}: {pull.title}")
                        print(f"Autor: {pull.user.login}")
                        print(f"URL: {pull.html_url}")
                        pr_number = pull.number
                        pr = repo.get_pull(pr_number)
                        pr.create_review(event="APPROVE")
                        pr.add_to_labels('dax_prod')
                        print(f"Pull request #{pr_number} aprovado automaticamente!")
                        bank_txt.write(f"{pull.number}_{pull.merge_commit_sha}\n")

    time.sleep(5)
