from PyQt5 import uic, QtWidgets
import mysql.connector

# Conexão com o banco de dados (tratamento de erro incluído)
try:
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='54321',
        database='controle_academico'
    )
    cursor = conexao.cursor()
except mysql.connector.Error as err:
    print(f"Erro ao conectar ao banco: {err}")
    exit()

# Variável global para edição
id_aluno_edicao = None

# ---------- FUNÇÕES: CURSOS ----------

def carregarCursosComboBox():
    """ Preenche o combobox com os cursos cadastrados. """
    tela.cmbCurso.clear()
    cursor.execute("SELECT id, nome FROM cursos")
    cursos = cursor.fetchall()

    if not cursos:
        print("Nenhum curso encontrado!")

    for id, nome in cursos:
        tela.cmbCurso.addItem(nome, id)

def cadastrarCurso():
    nome = tela_curso.txtCurso.text()
    carga = tela_curso.txtCarga.text()

    if nome and carga.isdigit():
        sql = "INSERT INTO cursos (nome, carga_horaria) VALUES (%s, %s)"
        cursor.execute(sql, (nome, int(carga)))
        conexao.commit()
        tela_curso.txtCurso.setText('')
        tela_curso.txtCarga.setText('')

        # Atualiza combo de cursos após um novo cadastro
        carregarCursosComboBox()

        QtWidgets.QMessageBox.information(tela_curso, 'Sucesso', 'Curso cadastrado com sucesso!')
    else:
        QtWidgets.QMessageBox.warning(tela_curso, 'Erro', 'Preencha todos os campos corretamente!')

def listarCursos():
    tela_curso.tblCursos.setRowCount(0)
    cursor.execute("SELECT id, nome, carga_horaria FROM cursos")
    for i, (id, nome, carga) in enumerate(cursor.fetchall()):
        tela_curso.tblCursos.insertRow(i)
        tela_curso.tblCursos.setItem(i, 0, QtWidgets.QTableWidgetItem(str(id)))
        tela_curso.tblCursos.setItem(i, 1, QtWidgets.QTableWidgetItem(nome))
        tela_curso.tblCursos.setItem(i, 2, QtWidgets.QTableWidgetItem(str(carga)))

def abrirTelaCurso():
    listarCursos()
    tela.hide()
    tela_curso.show()

def voltarTelaCurso():
    tela_curso.hide()
    tela.show()

# ---------- FUNÇÕES: ALUNOS ----------

def cadastrarAluno():
    """ Cadastro de aluno com curso selecionado """
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

def abrirLista():
    listarAlunos()
    tela.hide()
    tela_lista.show()

def voltarCadastro():
    tela_lista.hide()
    tela.show()

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
        cursor.execute("UPDATE alunos SET nome = %s, email = %s WHERE id = %s", (novo_nome, novo_email, id_aluno_edicao))
        conexao.commit()
        listarAlunos()
        tela_editar.close()
        QtWidgets.QMessageBox.information(tela_lista, 'Atualizado', 'Dados atualizados com sucesso!')
    else:
        QtWidgets.QMessageBox.warning(tela_editar, 'Erro', 'Preencha todos os campos!')

def voltarEdicao():
    tela_editar.close()

# ---------- RELATÓRIO ALUNOS + CURSOS ----------

def listarAlunosCursos():
    tela_relatorio.tblAlunosCursos.setRowCount(0)
    cursor.execute("""
        SELECT a.nome, c.nome, c.carga_horaria
        FROM alunos a
        JOIN cursos c ON a.curso_id = c.id
    """)
    for i, (aluno, curso, carga) in enumerate(cursor.fetchall()):
        tela_relatorio.tblAlunosCursos.insertRow(i)
        tela_relatorio.tblAlunosCursos.setItem(i, 0, QtWidgets.QTableWidgetItem(aluno))
        tela_relatorio.tblAlunosCursos.setItem(i, 1, QtWidgets.QTableWidgetItem(curso))
        tela_relatorio.tblAlunosCursos.setItem(i, 2, QtWidgets.QTableWidgetItem(str(carga)))

def abrirTelaAlunosCursos():
    listarAlunosCursos()
    tela.hide()
    tela_relatorio.show()

def voltarTelaAlunosCursos():
    tela_relatorio.hide()
    tela_curso.show()

# ---------- CARREGANDO TELAS ----------

app = QtWidgets.QApplication([])

tela = uic.loadUi("cadastro.ui")
tela_lista = uic.loadUi("lista_alunos.ui")
tela_editar = uic.loadUi("editar_aluno.ui")
tela_curso = uic.loadUi("Gerenciar_Cursos.ui")
tela_relatorio = uic.loadUi("lista_alunos_cursos.ui")

# Conectar botões
carregarCursosComboBox()
tela.btnCadastrar.clicked.connect(cadastrarAluno)
tela.btnlistar.clicked.connect(abrirLista)
tela.btnCurso.clicked.connect(abrirTelaCurso)
tela_curso.btnCadastrarCurso.clicked.connect(cadastrarCurso)
tela_curso.btnListaCurso.clicked.connect(listarCursos)
tela_curso.btnVoltarCurso.clicked.connect(voltarTelaCurso)

# Início
tela.show()
app.exec_()