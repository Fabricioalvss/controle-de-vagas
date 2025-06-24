# controle-de-vagas
Sistema de Controle Acadêmico — Python + MySQL"

Descrição do Projeto
Este projeto foi desenvolvido em Python + MySQL, com o objetivo de realizar o controle acadêmico de uma instituição.
O sistema permite cadastrar alunos, cursos, listar, editar, excluir registros e gerar relatórios com as informações armazenadas no banco de dados.

## ✅ Funcionalidades  
- Cadastro de alunos  
- Cadastro de cursos  
- Listagem de alunos e cursos cadastrados  
- Edição de dados de alunos  
- Exclusão de registros de alunos  
- Relacionamento entre alunos e cursos (um aluno pertence a um curso)  
- Relatórios de alunos matriculados em cada curso  

## 🗄️ Modelagem do Banco de Dados  
O sistema possui as seguintes tabelas:

| Tabela  | Descrição                                                |  
|---------|----------------------------------------------------------|  
| alunos  | Armazena dados dos alunos (id, nome, email, curso_id)   |  
| cursos  | Armazena dados dos cursos (id, nome, carga_horária)     |  

## 📁 Estrutura dos Arquivos no Repositório  

| Arquivo                          | Função                                                  |  
|-----------------------------------|---------------------------------------------------------|  
| Controle_Curso.py                 | Arquivo principal do sistema em Python                  |  
| criação do banco de dados.sql     | Script SQL para criação do banco e tabelas              |  
| inserindo dados.sql               | Script SQL para inserir dados de exemplo                |  
| Controle_Curso.spec               | Arquivo de configuração do executável (PyInstaller)     |  
| README.md                         | Documentação do projeto                                 |  


## 🚀 Tecnologias Utilizadas  
- 🐍 Python 3  
- 🗄️ MySQL  
- 🎨 PyQt5 (Interface gráfica) ou terminal  
- 🗂️ SQL (manipulação e modelagem de dados)

## 🚀 Como Executar o Projeto  

1. Clone este repositório para sua máquina:  
git clone https://github.com/seu-usuario/nome-do-repositorio.git
 
2. Instale as dependências necessárias:
pip install mysql-connector-python
pip install pyqt5

3. Crie o banco de dados no MySQL executando o arquivo:
criação do banco de dados.sql

4. (Opcional) Insira dados de exemplo usando:
inserindo dados.sql

Execute o sistema:
python Controle_Curso.py

Autor
Fabricio Santos

📧 Contato: fabricioalvs2003@gmail.com

💼 LinkedIn: www.linkedin.com/in/fabricio-santos-0248b716b

