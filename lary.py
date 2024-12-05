import pandas as pd
import streamlit as st
from datetime import datetime
import base64

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('rosa.png')

# Estilos personalizados para as abas
st.markdown(
    """
    <style>
    .css-1d391kg { 
        background-color: #F4A460; /* Cor do fundo da sidebar */
    }

    .stSidebar > div > div > div:nth-child(1) {
        background-color: #F4A460 !important; /* Cor para a aba de navegação*/
    }

    .stSidebar .css-1d391kg {
        background-color: #F4A460;  /* Cor da barra de fundo da sidebar */
    }

    .stSidebar .css-1noxpgk {
        background-color: #F4A460;  /* Cor da aba de navegação*/
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Criação das abas
aba_selecionada = st.sidebar.radio("Selecione <3", 
                                  ["Pagina inicial", "Planner Semanal", "Diário Pessoal", "Tarefas e Despesas", "Rastreador de Dívidas", "Calculadora econômica","Registro Final"])

if aba_selecionada == "Pagina inicial":
    st.markdown("<h1 style='color:Chocolate; text-align: center;'>PLANNER PESSOAL</h1>", unsafe_allow_html=True)
    
    st.image("viagem.png", use_column_width=True)  # Substitua com o caminho da sua imagem
    
    st.markdown("""
    <p style="text-align: center;">
        Este aplicativo foi desenvolvido para ajudá-lo a planejar suas tarefas semanais, registrar suas despesas,
        acompanhar seu progresso financeiro e organizar suas dívidas.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #FF8C00;'>Selecione uma das opções acima para começar!</h3>", unsafe_allow_html=True)

elif aba_selecionada == "Planner Semanal":
    st.markdown("<h1 style='color:Chocolate;'>GUIA DE PLANEJAMENTO:</h1>", unsafe_allow_html=True)
    st.title("Planner Semanal")
    st.write('Escreva seu planejamento da semana!:white_check_mark:')
    
    # Se o planejamento não foi registrado ainda, inicialize o dicionário
    if 'agenda' not in st.session_state:
        st.session_state.agenda = {day: "" for day in ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]}
    
    # Exibição das text areas para cada dia da semana, usando valores armazenados no session_state
    days = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    for day in days:
        st.session_state.agenda[day] = st.text_area(f"{day}:", value=st.session_state.agenda.get(day, ""), height=5)
    
    # Exibição do planejamento registrado na sessão
    st.write(pd.DataFrame(st.session_state.agenda.items(), columns=["Dia", "Atividades"]))

elif aba_selecionada == "Diário Pessoal":
    st.markdown("<h1 style='color:Chocolate;'>DIARIO:</h1>", unsafe_allow_html=True)
    st.write(':sparkles: Diario Pessoal')

    # Armazenamento das entradas do diário
    if 'entradas' not in st.session_state:
        st.session_state.entradas = pd.DataFrame(columns=["Entrada"])

    # Formulário para adicionar uma nova entrada no diário
    with st.form(key='entrada_diario'):
        entrada = st.text_area("Escreva sua reflexão do dia:")
        submit_button = st.form_submit_button("Adicionar Entrada")

    if submit_button and entrada:
        nova_entrada = pd.DataFrame([[entrada]], columns=["Entrada"])
        st.session_state.entradas = pd.concat([st.session_state.entradas, nova_entrada], ignore_index=True)
        st.success("Entrada adicionada com sucesso!")

    # Exibir entradas do diário
    st.subheader("Entradas do Diário")
    if not st.session_state.entradas.empty:
        for index, row in st.session_state.entradas.iterrows():
            st.write(f"{row['Entrada']}")
    else:
        st.write("Nenhuma entrada registrada.")

    # Opção para limpar entradas
    if st.button("Limpar Diário"):
        st.session_state.entradas = pd.DataFrame(columns=["Entrada"])
        st.success("Diário limpo!")

elif aba_selecionada == "Tarefas e Despesas":
    # Tarefas Domésticas e Controle de Despesas Domésticas
    st.markdown("<h1 style='color:Chocolate;'>Tarefas domésticas:</h1>", unsafe_allow_html=True)
    st.write('Tarefas para ser cumpridas :white_check_mark:')
    
    # Armazenamento das tarefas
    if 'tarefas' not in st.session_state:
        st.session_state.tarefas = pd.DataFrame(columns=["Tarefa", "Concluída"])

    # Formulário para adicionar tarefas
    with st.form(key='task_form'):
        nova_tarefa = st.text_input("Tarefa")
        submit_button = st.form_submit_button("Adicionar Tarefa")

    if submit_button and nova_tarefa:
        nova_tarefa_df = pd.DataFrame([[nova_tarefa, False]], columns=["Tarefa", "Concluída"])
        st.session_state.tarefas = pd.concat([st.session_state.tarefas, nova_tarefa_df], ignore_index=True)
        st.success("Tarefa adicionada!")

    # Exibição das tarefas
    st.subheader("Tarefas Registradas")
    if not st.session_state.tarefas.empty:
        for index, row in st.session_state.tarefas.iterrows():
            tarefa_concluida = st.checkbox(row["Tarefa"], value=row["Concluída"], key=index)
            if tarefa_concluida:
                st.session_state.tarefas.at[index, "Concluída"] = True
            else:
                st.session_state.tarefas.at[index, "Concluída"] = False
    else:
        st.write("Nenhuma tarefa registrada.")

    # Remoção de tarefas
    st.subheader("Remover Tarefa")
    remover_tarefa = st.selectbox("Escolha uma tarefa para remover", options=st.session_state.tarefas["Tarefa"].tolist() if not st.session_state.tarefas.empty else ["Nenhuma"])
    if st.button("Remover"):
        if remover_tarefa != "Nenhuma":
            st.session_state.tarefas = st.session_state.tarefas[st.session_state.tarefas["Tarefa"] != remover_tarefa]
            st.success(f"Tarefa '{remover_tarefa}' removida!")

    # Exibição da tabela de tarefas
    st.write(st.session_state.tarefas)
    
    # Controle de Despesas
    st.markdown("<h1 style='color:Chocolate;'>Controle de Despesas Domésticas:</h1>", unsafe_allow_html=True)
    st.write(':sparkles: Despesas')
    # Formulário para adicionar despesas
    with st.form(key='expense_form'):#botao
        categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Saúde","Contas agua","Conta de luz", "Aluguel","Internet","Gás"])
        valor = st.number_input("Valor", min_value=0.0, format="%.2f")
        data = st.date_input("Data",format="DD/MM/YYYY")
        submit_button = st.form_submit_button("Adicionar Despesa")

    # Armazenamento das despesas
    if 'despesas' not in st.session_state:
        st.session_state.despesas = pd.DataFrame(columns=["Data", "Categoria", "Valor"])

    if submit_button:
        nova_despesa = pd.DataFrame([[data, categoria, valor]], columns=["Data", "Categoria", "Valor"])
        st.session_state.despesas = pd.concat([st.session_state.despesas, nova_despesa], ignore_index=True)

    # Exibição das despesas
    st.markdown("<h1 style='color:Chocolate;'>Despesas Registradas</h1>", unsafe_allow_html=True)
    st.write(st.session_state.despesas)

    # Gráfico de despesas por categoria
    st.write(' Verificação das despesas novamente :white_check_mark:')
    st.write(st.session_state.despesas)

    # Cálculo e exibição do total
    total_despesas = st.session_state.despesas['Valor'].sum()
    st.write(f"Total de Despesas: R$ {total_despesas:.2f}")

    # Gráfico de despesas por categoria
    st.bar_chart(st.session_state.despesas.groupby('Categoria')['Valor'].sum())
    st.sidebar.subheader("Definir Orçamento Mensal")
    orçamento = st.sidebar.number_input("Orçamento Mensal", min_value=2000.0, format="%.2f")

    # Cálculo e comparação com o orçamento
    total_despesas = st.session_state.despesas['Valor'].sum()
    if total_despesas > orçamento:
        st.warning("Você excedeu seu orçamento mensal!")
    else:
        st.success("Você está dentro do orçamento!")

elif aba_selecionada == "Rastreador de Dívidas":
    st.markdown("<h1 style='color:Chocolate;'>Rastreador de Dívidas:</h1>", unsafe_allow_html=True)

    if 'dividas' not in st.session_state:
        st.session_state.dividas = []

    def adicionar_divida(descricao, valor, pago):
        st.session_state.dividas.append((descricao, valor, pago))

    with st.form(key='form_divida'):
        divida_descricao = st.text_input("Descrição da Dívida:")
        divida_valor = st.number_input("Valor da Dívida:", min_value=0.0, format="%.2f")
        pago = st.checkbox("Pago?")
        submit_divida = st.form_submit_button(label='Adicionar Dívida')
        if submit_divida and divida_descricao:
            adicionar_divida(divida_descricao, divida_valor, pago)
            st.success(f'Dívida "{divida_descricao}" adicionada!')

    # Resumo das Dívidas
    st.subheader("Dívidas:")
    if st.session_state.dividas:
        for descricao, valor, pago in st.session_state.dividas:
            status = "Pago" if pago else "Pendente"
            st.write(f"{descricao}: R${valor:.2f} - Status: {status}")
    else:
        st.write("Nenhuma dívida registrada.")

elif aba_selecionada == "Calculadora econômica":  
    st.markdown("<h1 style='color:Chocolate;'>Calculadora de Economia:</h1>", unsafe_allow_html=True)

    meta = st.number_input("Meta de Economia (R$):", min_value=0.0, format="%.2f")
    contribuicao_mensal = st.number_input("Contribuição Mensal (R$):", min_value=0.0, format="%.2f")

    if st.button('Calcular tempo necessário'):
        if contribuicao_mensal > 0:
            meses = meta / contribuicao_mensal
            st.success(f'Levará aproximadamente {meses:.2f} meses para atingir sua meta de R${meta:.2f}.')
        else:
            st.error("A contribuição mensal deve ser maior que zero.")

#
#
#
#
elif aba_selecionada == "Registro Final":
    st.markdown("<h1 style='color:Chocolate; text-align: center;'>Registro Final:</h1>", unsafe_allow_html=True)

    # Exibir entradas do diário
    st.subheader("Diário Pessoal:")
    if 'entradas' in st.session_state and not st.session_state.entradas.empty:
        for index, row in st.session_state.entradas.iterrows():
            st.write(f"{row['Entrada']}")
    else:
        st.write("Nenhuma entrada registrada no diário.")

    # Exibir tarefas domésticas
    st.subheader("Tarefas Domésticas:")
    if 'tarefas' in st.session_state and not st.session_state.tarefas.empty:
        st.write(st.session_state.tarefas)
    else:
        st.write("Nenhuma tarefa registrada.")

    # Exibir despesas
    st.subheader("Despesas Registradas:")
    if 'despesas' in st.session_state and not st.session_state.despesas.empty:
        st.write(st.session_state.despesas)
        total_despesas = st.session_state.despesas['Valor'].sum()
        st.write(f"Total de Despesas: R$ {total_despesas:.2f}")
    else:
        st.write("Nenhuma despesa registrada.")

    # Exibir dívidas
    st.subheader("Dívidas:")
    if 'dividas' in st.session_state and st.session_state.dividas:
        for descricao, valor, pago in st.session_state.dividas:
            status = "Pago" if pago else "Pendente"
            st.write(f"{descricao}: R${valor:.2f} - Status: {status}")
    else:
        st.write("Nenhuma dívida registrada.")
