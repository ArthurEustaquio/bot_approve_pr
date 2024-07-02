import datetime
import os
import sqlite3
import time
from github import Github

# Autenticação no GitHub usando um token
token = open('token.txt', 'r').read()
g = Github(token)

conexao = sqlite3.connect('bank_pr.db')
cursor = conexao.cursor()
# Verificar se banco existe caso nao criar
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pullrequests (
        pr TEXT
    )
''')

# Salva as alterações
conexao.commit()
# Repositório específico
owner = 'ps-data-platform'
repo_name = 'kiruna-khronos-ci-cd-yml'

repo = g.get_repo(f"{owner}/{repo_name}")
my_login = 'ArthurEustaquio'  # substituir pelo seu login
# list_login = ['RvaleAn',
#               'tqiabertagnolli',
#               'dilmaraferreira',
#               'pedsilva',
#               'ArthurEustaquio']
list_login = ['dilmaraferreira','RvaleAn']
# Remover o proprio usuario da lista
#list_login.remove(my_login)

while True:
    # Listar todos os pull requests do repositório
    pulls = repo.get_pulls(state='open')  # você pode definir 'state' como 'open', 'closed' ou 'all'
    # Iterar sobre os pull requests e verificar se faz parte da lista de logins caso sim aprovar a pr
    for pull in pulls:
        #if pull.user.login in list_login and 'hillvalley_homolog' in pull.title:
        if pull.user.login in list_login:
            pr_number = pull.number
            pr = repo.get_pull(pr_number)
            commits_len = pr.commits
            cursor.execute(f'SELECT 1 FROM pullrequests where pr = "{pull.number}_{commits_len}"')
            exists = cursor.fetchall()
            if not exists:
                print(f"Pull Request #{pull.number}: {pull.title}, data hora: {datetime.datetime.now()}")
                print(f"Autor: {pull.user.login}")
                print(f"URL: {pull.html_url}")
                pr.create_review(event="APPROVE")
                pr.delete_labels()
                cursor.execute(f'INSERT INTO pullrequests (pr) VALUES ("{pull.number}_{commits_len}")')
                conexao.commit()
                print(f"Pull request #{pr_number} aprovado automaticamente!")

    # mudar flag caso a pr seja sua para iniciar a esteira
    #     if pull.user.login == my_login:
    #         pr_number = pull.number
    #         pr = repo.get_pull(pr_number)
    #         commits_len = pr.commits
    #         revisions = pr.get_reviews()
    #         bank_txt_read = bank_txt.read()
    #         if f"{pull.number}_{commits_len}" not in bank_txt_read and revisions.totalCount > 0:
    #             pr.delete_labels()
    #             pr.add_to_labels('dax_prod')
    #             bank_txt.write(f"{pull.number}_{commits_len}\n")
    #             print(f"Pull request #{pr_number} foi aprovada e esteira foi reiniciada automaticamente!")
    time.sleep(5)
