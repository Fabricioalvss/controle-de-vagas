from PyQt5 import uic, QtWidgets
import mysql.connector

# Conexão com o banco de dados
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='54321',
    database='controle_academico'
)
cursor = conexao.cursor()

# Variável global para edição
id_aluno_edicao = None

def carregarCursosComboBox():
    """ Preenche o combobox com os cursos cadastrados. """
    tela.cmbCurso.clear()
    cursor.execute("SELECT id, nome FROM cursos")
    cursos = cursor.fetchall()

    if not cursos:
        print("Nenhum curso encontrado!")

    for id, nome in cursos:
        tela.cmbCurso.addItem(nome, id)
        
# FUNÇÕES: ALUNOS 

def cadastrarAluno():
    nome = tela.txtAluno.text()
    email = tela.txtEmail.text()

def cadastrarAluno():
    nome = tela.txtAluno.text()
    email = tela.txtEmail.text()
    curso_index = tela.cmbCurso.currentIndex()
    curso_id = tela.cmbCurso.itemData(curso_index)

    if nome and email and curso_id:
        sql = "INSERT INTO alunos (nome, email, curso_id) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, email, curso_id))
        conexao.commit()
        tela.txtAluno.setText('')
        tela.txtEmail.setText('')

        # ✅ Atualiza a lista de alunos imediatamente!
        listarAlunosCursos()

        QtWidgets.QMessageBox.information(tela, 'Sucesso', 'Aluno cadastrado com curso!')
    else:
        QtWidgets.QMessageBox.warning(tela, 'Erro', 'Selecione um curso!')

def listarAlunos():
    tela_lista.tblAlunos.setRowCount(0)
    cursor.execute("""
        SELECT a.id, a.nome, a.email, c.nome 
        FROM alunos a
        LEFT JOIN cursos c ON a.curso_id = c.id
    """)
    for i, (id, nome, email, curso) in enumerate(cursor.fetchall()):
        tela_lista.tblAlunos.insertRow(i)
        tela_lista.tblAlunos.setItem(i, 0, QtWidgets.QTableWidgetItem(str(id)))
        tela_lista.tblAlunos.setItem(i, 1, QtWidgets.QTableWidgetItem(nome))
        tela_lista.tblAlunos.setItem(i, 2, QtWidgets.QTableWidgetItem(email))
        tela_lista.tblAlunos.setItem(i, 3, QtWidgets.QTableWidgetItem(curso or "-"))

def excluirAluno():
    linha = tela_lista.tblAlunos.currentRow()
    if linha >= 0:
        id_aluno = tela_lista.tblAlunos.item(linha, 0).text()
        cursor.execute("DELETE FROM alunos WHERE id = %s", (id_aluno,))
        conexao.commit()
        listarAlunos()
        QtWidgets.QMessageBox.information(tela_lista, 'Sucesso', 'Aluno excluído com sucesso!')

def editarAluno():
    global id_aluno_edicao
    linha = tela_lista.tblAlunos.currentRow()
    if linha >= 0:
        id_aluno_edicao = tela_lista.tblAlunos.item(linha, 0).text()
        nome = tela_lista.tblAlunos.item(linha, 1).text()
        email = tela_lista.tblAlunos.item(linha, 2).text()
        tela_editar.txtEditarNome.setText(nome)
        tela_editar.txtEditarEmail.setText(email)
        tela_editar.show()

def salvarEdicao():
    novo_nome = tela_editar.txtEditarNome.text()
    novo_email = tela_editar.txtEditarEmail.text()

    if novo_nome and novo_email:
        sql = "UPDATE alunos SET nome = %s, email = %s WHERE id = %s"
        cursor.execute(sql, (novo_nome, novo_email, id_aluno_edicao))
        conexao.commit()
        listarAlunos()
        tela_editar.close()
        QtWidgets.QMessageBox.information(tela_lista, 'Atualizado', 'Dados atualizados com sucesso!')
    else:
        QtWidgets.QMessageBox.warning(tela_editar, 'Erro', 'Preencha todos os campos!')

def abrirLista():
    listarAlunos()
    tela.hide()
    tela_lista.show()

def voltarCadastro():
    tela_lista.hide()
    tela.show()

def voltarEdicao():
    tela_editar.close()

# FUNÇÕES: CURSOS 

def cadastrarCurso():
    nome = tela_curso.txtCurso.text()
    carga = tela_curso.txtCarga.text()

    if nome and carga.isdigit():
        sql = "INSERT INTO cursos (nome, carga_horaria) VALUES (%s, %s)"
        cursor.execute(sql, (nome, int(carga)))
        conexao.commit()
        tela_curso.txtCurso.setText('')
        tela_curso.txtCarga.setText('')
        QtWidgets.QMessageBox.information(tela_curso, 'Sucesso', 'Curso cadastrado com sucesso!')
    else:
        QtWidgets.QMessageBox.warning(tela_curso, 'Erro', 'Preencha todos os campos corretamente!')

def abrirTelaCurso():
    tela.hide()
    tela_curso.show()

def voltarTelaCurso():
    tela_curso.hide()
    tela.show()

# FUNÇÕES: RELATÓRIO ALUNOS + CURSOS

def listarAlunosCursos():
    tela_alunos_cursos.tblAlunosCursos.setRowCount(0)
    sql = """
        SELECT a.nome, c.nome, c.carga_horaria
        FROM alunos a
        JOIN cursos c ON a.curso_id = c.id
    """
    cursor.execute(sql)
    for i, (aluno, curso, carga) in enumerate(cursor.fetchall()):
        tela_alunos_cursos.tblAlunosCursos.insertRow(i)
        tela_alunos_cursos.tblAlunosCursos.setItem(i, 0, QtWidgets.QTableWidgetItem(aluno))
        tela_alunos_cursos.tblAlunosCursos.setItem(i, 1, QtWidgets.QTableWidgetItem(curso))
        tela_alunos_cursos.tblAlunosCursos.setItem(i, 2, QtWidgets.QTableWidgetItem(str(carga)))

def abrirTelaAlunosCursos():
    listarAlunosCursos()
    tela.hide()
    tela_alunos_cursos.show()

def voltarTelaAlunosCursos():
    tela_alunos_cursos.hide()
    tela_curso.show()

# CARREGANDO TELAS

app = QtWidgets.QApplication([])

tela = uic.loadUi("cadastro.ui")
tela_lista = uic.loadUi("lista_alunos.ui")
tela_editar = uic.loadUi("editar_aluno.ui")
tela_curso = uic.loadUi("Gerenciar_Cursos.ui")
tela_alunos_cursos = uic.loadUi("lista_alunos_cursos.ui")

# CONEXÕES

# Tela principal
carregarCursosComboBox()
tela.btnCadastrar.clicked.connect(cadastrarAluno)
tela.btnlistar.clicked.connect(abrirLista)
tela.btnCurso.clicked.connect(abrirTelaCurso)
tela_curso.btnListaCurso.clicked.connect(abrirTelaAlunosCursos)

# Tela listagem
tela_lista.btnExcluir.clicked.connect(excluirAluno)
tela_lista.btnEditar.clicked.connect(editarAluno)
tela_lista.btnVoltar.clicked.connect(voltarCadastro)

# Tela edição
tela_editar.btnSalvarEdicao.clicked.connect(salvarEdicao)
tela_editar.btnVoltarEdicao.clicked.connect(voltarEdicao)

# Tela cursos
tela_curso.btnCadastrarCurso.clicked.connect(cadastrarCurso)
tela_curso.btnListaCurso.clicked.connect(listarAlunosCursos)
tela_curso.btnVoltarCurso.clicked.connect(voltarTelaCurso)

# Tela alunos + cursos
listarAlunosCursos()
tela_alunos_cursos.btnVoltarAlunos.clicked.connect(voltarTelaAlunosCursos)

# INÍCIO
tela.show()
app.exec_()