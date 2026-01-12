import sqlite3

def criar_banco():
    con = sqlite3.connect('saves.db')
    cursor = con.cursor()
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
    id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
);
""")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aluno (
    id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    matricula TEXT NOT NULL UNIQUE,
    cpf TEXT NOT NULL UNIQUE,
    cidade_origem TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS login (
    id_login INTEGER PRIMARY KEY AUTOINCREMENT,
    id_aluno INTEGER NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    FOREIGN KEY (id_aluno) REFERENCES aluno (id_aluno)
    );
    ''')

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS socioeconomico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,

    renda_familiar_total REAL,
    renda_per_capita REAL,
    qtd_membros_familia INTEGER,
    principal_responsavel TEXT,
    estado_civil TEXT,

    possui_filhos TEXT,
    qtd_filhos INTEGER,
    idade_filhos TEXT,
    filho_comorbidade TEXT,
    desc_filho_comorbidade TEXT,

    recebe_beneficio TEXT,
    beneficio_qual TEXT,

    possui_comorbidade TEXT,
    descricao_comorbidade TEXT,

    mora_com_familia TEXT,
    paga_aluguel TEXT,
    casa_propria TEXT,
    mora_na_cidade_de_origem TEXT,
    distancia_km REAL,

    transporte_proprio TEXT,
    gastos_transporte TEXT,

    aluno_de_outra_cidade TEXT,
    distancia_residencia REAL,

    outros_fatores TEXT,

    pontuacao_vulnerabilidade REAL,
                   
    tipo_curso TEXT,
    nome_curso TEXT,
    modalidade TEXT,
    turno TEXT,
    

    FOREIGN KEY (aluno_id) REFERENCES aluno(id_aluno)
    );
    """)

    con.commit()
    con.close()
    print("Banco e tabelas criados com sucesso.")

def adicionar_aluno():
    con = sqlite3.connect('saves.db')
    cursor = con.cursor()

    print('\n=== Cadastro de Aluno ===')
    nome = input("Nome: ")
    matricula = input("Matricula: ")
    cpf = input("CPF: ")
    cidade_origem = input("Cidade de origem: ")

    cursor.execute(
        "SELECT * FROM aluno WHERE matricula = ? AND cpf = ?",
        (matricula, cpf)
    )

    if cursor.fetchone() is not None:
        print("\nEste aluno já possui cadastro!")
        con.close()
        return

    cursor.execute("INSERT INTO aluno (nome, matricula, cpf, cidade_origem) VALUES (?, ?, ?, ?)",
                   (nome, matricula, cpf, cidade_origem))
    con.commit()
    con.close()
    print("Aluno cadastrado com sucesso.")

def cadastrar_login():
    con = sqlite3.connect('saves.db')
    cursor = con.cursor()

    print("\n=== Cadastro de Login ===")
    matricula = input("Informe a matrícula do aluno: ")
    cpf = input("Informe o CPF do aluno: ")
    
    cursor.execute(
        "SELECT id_aluno FROM aluno WHERE matricula = ? AND cpf = ?",
        (matricula, cpf)
    )
    resultado = cursor.fetchone()

    if resultado is None:
        print("Matrícula e CPF não conferem.")
        print("Acesso negado.")
        con.close()
        return

    id_aluno = resultado[0]

    cursor.execute("SELECT * FROM login WHERE id_aluno = ?", (id_aluno,))
    if cursor.fetchone() is not None:
        print("Este aluno já possui login cadastrado.")
        con.close()
        return

    email = input("Email: ")
    senha = input("Senha: ")

    cursor.execute(
        "INSERT INTO login (id_aluno, email, senha) VALUES (?, ?, ?)",
        (id_aluno, email, senha)
    )

    con.commit()
    con.close()
    print("Login criado com sucesso!")

def listar_alunos():
    con = sqlite3.connect("saves.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM aluno;")
    print("Aluno:")
    print("##############################")
    for resultado in cursor.fetchall():
        print("Nome:", resultado[1])
        print("Matricula:", resultado[2])
        print("CPF:", resultado[3])
        print("Cidade de origem:", resultado[4])
        print("--------------------------")
    con.close()

def atualizar_aluno():
    con = sqlite3.connect("saves.db")
    cursor = con.cursor()
    matricula = input("Informe a matrícula do aluno que deseja atualizar: ")
    print("Selecione o campo que deseja atualizar:")
    print("1 - Nome")
    print("2 - CPF")
    print("3 - Cidade")
    opcao = input("Opção: ")

    campo = None
    novo_valor = None

    if opcao == "1":
        campo = "nome"
        novo_valor = input("Digite o novo nome: ")
    elif opcao == "2":
        campo = "cpf"
        novo_valor = input("Digite o novo CPF: ")
    elif opcao == "3":
        campo = "cidade_origem"
        novo_valor = input("Digite a nova cidade: ")
    else:
        print("Opção inválida.")
        exit()

    cursor.execute("SELECT matricula FROM aluno WHERE matricula = ?", (matricula,))
    if cursor.fetchone() is None:
        print("Matrícula não encontrada.")
        con.close()
        exit()

    sql = f"UPDATE aluno SET {campo} = ? WHERE matricula = ?"
    cursor.execute(sql, (novo_valor, matricula))
    con.commit()
    con.close()

    print("Atualização realizada com sucesso.")

def adicionar_socioeconomico():
    con = sqlite3.connect("saves.db")
    cursor = con.cursor()

    print("\n=== Formulário Socioeconômico ===")

    matricula = input("Informe a matrícula do aluno: ")

    cursor.execute("SELECT id_aluno FROM aluno WHERE matricula = ?", (matricula,))
    resultado = cursor.fetchone()

    if resultado is None:
        print("Matrícula não encontrada. Retornando ao menu.")
        con.close()
        return

    aluno_id = resultado[0]

    cursor.execute(
        "SELECT * FROM socioeconomico WHERE aluno_id = ?",
        (aluno_id,)
    )

    if cursor.fetchone() is not None:
        print("\nEste aluno já possui cadastro socioeconômico.")
        con.close()
        return

    
    while True:
        try:
            renda_familiar_total = float(input("Renda familiar total: ").replace(',', '.'))
            break
        except ValueError:
            print("Digite um valor numérico válido.")

    while True:
        try:
            qtd_membros_familia = int(input("Quantidade de membros na família: "))
            if qtd_membros_familia <= 0:
                print("A quantidade de membros deve ser maior que zero.")
                continue
            break
        except ValueError:
            print("Digite um número inteiro válido.")

    renda_per_capita = renda_familiar_total / qtd_membros_familia

    principal_responsavel = input("Você é o(a) principal responsável financeiro(a)? (sim/não): ")
    estado_civil = input("Estado civil: ")

    possui_filhos = input("Possui filhos? (sim/não): ")

    if possui_filhos.lower() == "sim":
        qtd_filhos = int(input("Quantos filhos? "))
        idades = []
        for i in range(qtd_filhos):
            idade = input(f"Idade do filho {i + 1}: ")
            idades.append(idade)
        idade_filhos = ", ".join(idades)

        filho_comorbidade = input("Algum filho tem comorbidade? (sim/não): ")
        if filho_comorbidade.lower() == "sim":
            desc_filho_comorbidade = input("Descreva a comorbidade: ")
        else:
            desc_filho_comorbidade = ""
    else:
        qtd_filhos = 0
        idade_filhos = ""
        filho_comorbidade = "não"
        desc_filho_comorbidade = ""

    recebe_beneficio = input("Recebe benefício governamental? (sim/não): ")
    beneficio_qual = ""
    if recebe_beneficio.lower() == "sim":
        beneficio_qual = input("Qual benefício? ")

    possui_comorbidade = input("Você possui comorbidade? (sim/não): ")
    if possui_comorbidade.lower() == "sim":
        descricao_comorbidade = input("Descreva sua comorbidade: ")
    else:
        descricao_comorbidade = ""

    mora_com_familia = input("Mora com a família? (sim/não): ")
    paga_aluguel = input("Paga aluguel? (sim/não): ")
    casa_propria = input("Casa própria? (sim/não): ")

    mora_na_cidade_de_origem = input("Mora na cidade de origem? (sim/não): ")
    if mora_na_cidade_de_origem.lower() == "não":
        distancia_km = float(input("Distância até a cidade (em km): "))
    else:
        distancia_km = 0

    transporte_proprio = input("Possui transporte próprio? (sim/não): ")
    gastos_transporte = input("Gasto mensal com transporte: ")

    aluno_de_outra_cidade = input("Aluno de outra cidade? (sim/não): ")
    if aluno_de_outra_cidade.lower() == "sim":
        distancia_residencia = float(input("Distância da residência até o campus (km): "))
    else:
        distancia_residencia = 0

    outros_fatores = input("Deseja informar outros fatores? ")

    

    
    tipo_curso = input("Tipo de curso (Técnico / Superior / Especialização): ")
    nome_curso = input("Nome do curso: ")
    modalidade = input("Modalidade (Presencial / EAD / Semipresencial): ")
    turno = input("Turno (Matutino / Vespertino / Noturno / Diurno): ")

    pontuacao_vulnerabilidade = calcular_indice_vulnerabilidade(
    renda_per_capita,
    recebe_beneficio,
    mora_com_familia,
    paga_aluguel,
    transporte_proprio,
    possui_filhos,
    aluno_de_outra_cidade
)

    cursor.execute("""
    INSERT INTO socioeconomico (
        aluno_id, renda_familiar_total, renda_per_capita, qtd_membros_familia,
        principal_responsavel, estado_civil, possui_filhos, qtd_filhos, idade_filhos,
        filho_comorbidade, desc_filho_comorbidade, recebe_beneficio, beneficio_qual,
        possui_comorbidade, descricao_comorbidade, mora_com_familia, paga_aluguel,
        casa_propria, mora_na_cidade_de_origem, distancia_km, transporte_proprio,
        gastos_transporte, aluno_de_outra_cidade, distancia_residencia, outros_fatores,
        pontuacao_vulnerabilidade, tipo_curso, nome_curso, modalidade, turno
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        aluno_id, renda_familiar_total, renda_per_capita, qtd_membros_familia,
        principal_responsavel, estado_civil, possui_filhos, qtd_filhos, idade_filhos,
        filho_comorbidade, desc_filho_comorbidade, recebe_beneficio, beneficio_qual,
        possui_comorbidade, descricao_comorbidade, mora_com_familia, paga_aluguel,
        casa_propria, mora_na_cidade_de_origem, distancia_km, transporte_proprio,
        gastos_transporte, aluno_de_outra_cidade, distancia_residencia, outros_fatores,
        pontuacao_vulnerabilidade, tipo_curso, nome_curso, modalidade, turno
    ))

    


    con.commit()
    con.close()
    print("\nFormulário socioeconômico registrado com sucesso!")

def menu_principal():
    opcao = 0
    while opcao != 3:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Acesso Aluno")
        print("2. Acesso Administrador")
        print("3. Sair")

        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            menu_acesso_aluno()
        elif opcao == 2:
            menu_acesso_admin()
        elif opcao == 3:
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_acesso_aluno():
    opcao = 0
    while opcao != 4:
        print("\n=== Acesso do Aluno ===")
        print("1. Já tenho cadastro (apenas criar login)")
        print("2. Login")
        print("3. Criar cadastro")
        print("4. Esqueci minha senha")
        print("5. Voltar")

        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            cadastrar_login()  
              
        elif opcao == 2:
            login_aluno()
        elif opcao == 3:
            criar_conta_aluno()
        elif opcao == 4:
            recuperar_senha_aluno()
        elif opcao == 5:
            print("Voltando ao menu principal...")
            return
        else:
            print("Opção inválida.")


def menu_interno_aluno():
    opcao = 0
    while opcao != 4:
        print("\n=== Acesso Interno do Aluno ===")
        print("1. Cadastrar dados socioeconômicos")
        print("2. Ver meus dados socioeconômicos")
        print("3. Atualizar meus dados socioeconômicos")
        print("4. Voltar")

        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            adicionar_socioeconomico()
        elif opcao == 2:
            visualiza_socioeconomico()  
        elif opcao == 3:
            atualizar_socioeconomico() 
        elif opcao == 4:
            print("Voltando ao menu principal...")
            return
        else:
            print("Opção inválida.")



def criar_conta_admin():
    con = sqlite3.connect('saves.db')
    cursor = con.cursor()

    print("\n=== Criar Conta Administrador ===")
    email = input("Email: ")
    senha = input("Senha: ")

    try:
        cursor.execute(
            "INSERT INTO admin (email, senha) VALUES (?, ?)",
            (email, senha)
        )
        con.commit()
        print("Conta de administrador criada com sucesso!")
    except sqlite3.IntegrityError:
        print("Este email já está cadastrado.")

    con.close()

def login_admin():
    con = sqlite3.connect('saves.db')
    cursor = con.cursor()

    print("\n=== Login do Administrador ===")
    email = input("Email: ")
    senha = input("Senha: ")

    cursor.execute(
        "SELECT * FROM admin WHERE email = ? AND senha = ?",
        (email, senha)
    )

    resultado = cursor.fetchone()

    if resultado is None:
        print("Email ou senha inválidos.")
    else:
        print("Login realizado com sucesso!")
        menu_interno_admin()

    con.close()



def menu_acesso_admin():
    opcao = 0
    while opcao != 4:
        print("\n=== Acesso do Administrador ===")
        print("1. Login")
        print("2. Criar conta")
        print("3. Esqueci minha senha")
        print("4. Voltar")

        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            login_admin()
        elif opcao == 2:
            criar_conta_admin()
        elif opcao == 3:
            recuperar_senha_admin()
        elif opcao == 4:
            print("Voltando ao menu principal...")
            menu_principal()
            return
        else:
            print("Opção inválida.")

def menu_interno_admin():
    opcao = 0
    while opcao != 10:
        print("\n=== Acesso Interno do Administrador ===")
        print("1. Cadastrar Aluno")
        print("2. Listar Alunos")
        print("3. Atualizar aluno")
        print("4. Cadastrar login")
        print("5. Cadastrar dados socioeconômicos")
        print("6. Listar dados socioeconômicos")
        print("7. Atualizar dados socioeconômicos")
        print("8. Ver ranking de prioridade")
        print("9. Deletar Dados (aluno)")
        print("10. Voltar")
        
        

        opcao = int(input("Escolha uma opção: "))
        if opcao == 1:
            adicionar_aluno()
        elif opcao == 2:
            listar_alunos()
        elif opcao == 3:
            atualizar_aluno()
        elif opcao == 4:
            cadastrar_login()
        elif opcao == 5:
            adicionar_socioeconomico()
        elif opcao == 6:
            listar_socioeconomico()
        elif opcao == 7:
            atualizar_socioeconomico()
        elif opcao == 8:
            listar_ranking_prioridade()
        elif opcao == 9:
            deletar_aluno_admin()
        elif opcao == 10:
            menu_acesso_admin()
            return
        
        
        else:
            print("Opção inválida.")

def listar_socioeconomico():
    con = sqlite3.connect('saves.db')
    cursor = con.cursor()

    cursor.execute("""
        SELECT 
            aluno.nome,
            aluno.matricula,
            socioeconomico.renda_per_capita,
            socioeconomico.pontuacao_vulnerabilidade,
            socioeconomico.tipo_curso,
            socioeconomico.turno
        FROM socioeconomico
        JOIN aluno ON socioeconomico.aluno_id = aluno.id_aluno
    """)

    dados = cursor.fetchall()

    if not dados:
        print("\nNenhum dado encontrado.")
    else:
        print("\n=== DADOS SOCIOECONÔMICOS ===")
        for d in dados:
            print(f"""
Aluno: {d[0]}
Matrícula: {d[1]}
Renda per capita: R$ {d[2]}
Pontuação: {d[3]}
Curso: {d[4]}
Turno: {d[5]}
-------------------------
""")


    con.close()

def calcular_indice_vulnerabilidade(
    renda_per_capita,
    recebe_beneficio,
    mora_com_familia,
    paga_aluguel,
    transporte_proprio,
    possui_filhos,
    aluno_de_outra_cidade
):
    pontos = 0

    
    if renda_per_capita <= 500:
        pontos += 5
    elif renda_per_capita <= 1000:
        pontos += 3
    else:
        pontos += 1

    
    if recebe_beneficio.lower() == "sim":
        pontos += 2

    if mora_com_familia.lower() == "não":
        pontos += 2

    
    if paga_aluguel.lower() == "sim":
        pontos += 2

    
    if transporte_proprio.lower() == "não":
        pontos += 2

    
    if possui_filhos.lower() == "sim":
        pontos += 2

    
    if aluno_de_outra_cidade.lower() == "sim":
        pontos += 2

    return pontos

def listar_ranking_prioridade():
    con = sqlite3.connect("saves.db")
    cursor = con.cursor()

    print("\n=== RANKING DE PRIORIDADE ===")
    print("Do mais vulnerável para o menos vulnerável:\n")

    cursor.execute("""
        SELECT 
            aluno.nome,
            aluno.matricula,
            socioeconomico.pontuacao_vulnerabilidade
        FROM socioeconomico
        JOIN aluno ON socioeconomico.aluno_id = aluno.id_aluno
        ORDER BY socioeconomico.pontuacao_vulnerabilidade DESC
    """)

    resultados = cursor.fetchall()
    
    

    if not resultados:
        print("Nenhum aluno com pontuação cadastrada.")
    else:
        posicao = 1
        for nome, matricula, pontuacao in resultados:
            print(f"{posicao}º lugar")
            print("Nome:", nome)
            print("Matrícula:", matricula)
            print("Pontuação:", pontuacao)
            print("-------------------------------")
            posicao += 1

    con.close()
    menu_interno_admin()
    return



def recuperar_senha_admin():
    con = sqlite3.connect('saves.db')
    cursor = con.cursor()

    print("\n=== Recuperar Senha ===")
    email = input("Digite seu email: ")

    cursor.execute(
        "SELECT id_admin FROM admin WHERE email = ?",
        (email,)
    )
    resultado = cursor.fetchone()

    if resultado is None:
        print("Email não encontrado.")
        con.close()
        return

    id_admin = resultado[0]

    nova_senha = input("Digite a nova senha: ")

    cursor.execute(
        "UPDATE admin SET senha = ? WHERE id_admin = ?",
        (nova_senha, id_admin)
    )

    con.commit()
    con.close()
    print("Senha atualizada com sucesso!")


def deletar_aluno_admin():
    con = sqlite3.connect('saves.db')
    cursor = con.cursor()

    print("\n=== EXCLUIR ALUNO (ADMIN) ===")
    matricula = input("Digite a matrícula do aluno que deseja excluir: ")

   
    cursor.execute("SELECT id_aluno, nome FROM aluno WHERE matricula = ?", (matricula,))
    resultado = cursor.fetchone()

    if resultado is None:
        print("Aluno não encontrado.")
        con.close()
        menu_interno_admin()
        return

    aluno_id = resultado[0]
    nome_aluno = resultado[1]

    print("\nAluno encontrado:")
    print("Nome:", nome_aluno)
    print("Matrícula:", matricula)

    confirmacao = input("\nATENÇÃO: Isso apagará TODOS os dados do aluno.\nDigite 'sim' para confirmar (ou N para cancelar): ")

    if confirmacao.lower() != "sim":
        print("Operação cancelada.")
        con.close()
        menu_interno_admin()
        return

    
    cursor.execute("DELETE FROM socioeconomico WHERE aluno_id = ?", (aluno_id,))

    
    cursor.execute("DELETE FROM login WHERE id_aluno = ?", (aluno_id,))

    
    cursor.execute("DELETE FROM aluno WHERE id_aluno = ?", (aluno_id,))

    con.commit()
    con.close()
    

    print("Aluno e todos os seus dados foram excluídos com sucesso.")
    menu_interno_admin() 

def criar_conta_aluno():
    adicionar_aluno()
    
    


def recuperar_senha_aluno():
    con = sqlite3.connect('saves.db')
    cursor = con.cursor()

    print("\n=== Recuperar Senha ===")
    matricula = input("Digite sua matrícula: ")
    cpf = input("Digite seu CPF: ")

    cursor.execute(
        "SELECT id_aluno FROM aluno WHERE matricula = ? AND cpf = ?",
        (matricula, cpf)
    )
    resultado = cursor.fetchone()

    if resultado is None:
        print("\nMatrícula e CPF não conferem.")
        con.close()
        menu_acesso_aluno()
        return
    

    id_aluno = resultado[0]

    cursor.execute("SELECT * FROM login WHERE id_aluno = ?", (id_aluno,))
    if cursor.fetchone() is None:
        print("Este aluno ainda não possui login.")
        con.close()
        menu_acesso_aluno()
        return

    nova_senha = input("Digite a nova senha: ")

    cursor.execute(
        "UPDATE login SET senha = ? WHERE id_aluno = ?",
        (nova_senha, id_aluno)
    )

    con.commit()
    con.close()
    print("Senha atualizada com sucesso!")
    menu_acesso_aluno()
    return


def login_aluno():
    con = sqlite3.connect('saves.db')
    cursor = con.cursor()

    print("\n=== Login do Aluno ===")
    email = input("Email: ")
    senha = input("Senha: ")

    cursor.execute(
        "SELECT * FROM login WHERE email = ? AND senha = ?",
        (email, senha)
    )

    resultado = cursor.fetchone()

    if resultado is None:
        print("Email ou senha inválidos.")
    else:
        print("Login realizado com sucesso!")
        menu_interno_aluno()

    con.close()


def visualiza_socioeconomico():
    con = sqlite3.connect('saves.db')
    cursor = con.cursor()

    matricula = input("Digite sua matrícula: ")

    cursor.execute("SELECT id_aluno FROM aluno WHERE matricula = ?", (matricula,))
    resultado = cursor.fetchone()

    if resultado is None:
        print("Aluno não encontrado.")
        con.close()
        return

    aluno_id = resultado[0]

    cursor.execute("""
        SELECT 
            renda_familiar_total,
            renda_per_capita,
            qtd_membros_familia,
            estado_civil,
            recebe_beneficio,
            beneficio_qual,
            possui_comorbidade,
            descricao_comorbidade,
            mora_com_familia,
            paga_aluguel,
            casa_propria,
            mora_na_cidade_de_origem,
            distancia_km,
            transporte_proprio,
            gastos_transporte,
            aluno_de_outra_cidade,
            distancia_residencia,
            outros_fatores,
            
            tipo_curso,
            nome_curso,
            modalidade,
            turno
        FROM socioeconomico
        WHERE aluno_id = ?
    """, (aluno_id,))

    dados = cursor.fetchone()

    if dados is None:
        print("Nenhum dado socioeconômico encontrado.")
    else:
        print("\n=== Seus Dados Socioeconômicos ===")

        print("Renda Familiar:", dados[0])
        print("Renda Per Capita:", dados[1])
        print("Qtd Membros da Família:", dados[2])
        print("Estado Civil:", dados[3])

        print("Recebe Benefício:", dados[4])
        print("Benefício:", dados[5])

        print("Possui Comorbidade:", dados[6])
        print("Descrição da Comorbidade:", dados[7])

        print("Mora com a Família:", dados[8])
        print("Paga Aluguel:", dados[9])
        print("Casa Própria:", dados[10])

        print("Mora na Cidade de Origem:", dados[11])
        print("Distância (km):", dados[12])

        print("Transporte Próprio:", dados[13])
        print("Gasto com Transporte:", dados[14])

        print("Aluno de Outra Cidade:", dados[15])
        print("Distância da Residência:", dados[16])

        print("Outros Fatores:", dados[17])
        print("Tipo de Curso:", dados[18])
        print("Nome do Curso:", dados[19])
        print("Modalidade:", dados[20])
        print("Turno:", dados[21])

    con.close()


def atualizar_socioeconomico():
    con = sqlite3.connect('saves.db')
    cursor = con.cursor()

    matricula = input("Informe sua matrícula: ")

    cursor.execute("SELECT id_aluno FROM aluno WHERE matricula = ?", (matricula,))
    resultado = cursor.fetchone()

    if resultado is None:
        print("Aluno não encontrado.")
        con.close()
        return

    aluno_id = resultado[0]

    print("\n=== O QUE DESEJA ATUALIZAR? ===")
    print("1 - Renda Familiar")
    print("2 - Quantidade de membros da família")
    print("3 - Recebe benefício")
    print("4 - Mora com a família")
    print("5 - Paga aluguel")
    print("6 - Possui transporte próprio")
    print("7 - Gasto com transporte")
    print("8 - Tipo de curso")
    print("9 - Nome do curso")
    print("10 - Modalidade")
    print("11 - Turno")

    opcao = input("Opção: ")

    if opcao == "1":
        novo_valor = float(input("Nova renda familiar: "))
        campo = "renda_familiar_total"

    elif opcao == "2":
        novo_valor = int(input("Nova quantidade de membros: "))
        campo = "qtd_membros_familia"

    elif opcao == "3":
        novo_valor = input("Recebe benefício (sim/não): ")
        campo = "recebe_beneficio"

    elif opcao == "4":
        novo_valor = input("Mora com a família (sim/não): ")
        campo = "mora_com_familia"

    elif opcao == "5":
        novo_valor = input("Paga aluguel (sim/não): ")
        campo = "paga_aluguel"

    elif opcao == "6":
        novo_valor = input("Possui transporte próprio (sim/não): ")
        campo = "transporte_proprio"

    elif opcao == "7":
        novo_valor = input("Novo gasto com transporte: ")
        campo = "gastos_transporte"

    elif opcao == "8":
        novo_valor = input("Novo tipo de curso: ")
        campo = "tipo_curso"

    elif opcao == "9":
        novo_valor = input("Novo nome do curso: ")
        campo = "nome_curso"

    elif opcao == "10":
        novo_valor = input("Nova modalidade: ")
        campo = "modalidade"

    elif opcao == "11":
        novo_valor = input("Novo turno: ")
        campo = "turno"

    else:
        print("Opção inválida.")
        con.close()
        return

    cursor.execute(
        f"UPDATE socioeconomico SET {campo} = ? WHERE aluno_id = ?",
        (novo_valor, aluno_id)
    )

    con.commit()
    con.close()
    print("Dados atualizados com sucesso!")


criar_banco()
menu_principal()