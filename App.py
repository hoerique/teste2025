import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Carregar informações de configuração e credenciais do st.secrets
spreadsheet_id = st.secrets["google_sheets"]["spreadsheet_id"]
service_account_info = st.secrets["service_account"]

# Criar credenciais do Google
creds = Credentials.from_service_account_info(service_account_info)
client = gspread.authorize(creds)

# Abrir a planilha e acessar a aba "Produtos"
spreadsheet = client.open_by_key(spreadsheet_id)
try:
    sheet = spreadsheet.worksheet("Produtos")
except gspread.exceptions.WorksheetNotFound:
    sheet = spreadsheet.add_worksheet(title="Produtos", rows="100", cols="5")
    sheet.append_row(["ID", "Nome", "Preço", "Quantidade", "Categoria"])

# Função para cadastrar produto
def cadastrar_produto(nome, preco, quantidade, categoria):
    dados = sheet.get_all_values()
    novo_id = len(dados)  # Criar ID sequencial
    sheet.append_row([novo_id, nome, preco, quantidade, categoria])
    st.success("✅ Produto cadastrado com sucesso!")

# Função para listar produtos
def listar_produtos():
    dados = sheet.get_all_values()
    if len(dados) <= 1:
        st.warning("⚠️ Nenhum produto cadastrado!")
        return
    
    st.subheader("📦 Lista de Produtos:")
    for row in dados[1:]:
        st.write(f"ID: {row[0]} | Nome: {row[1]} | Preço: R${row[2]} | Qtd: {row[3]} | Categoria: {row[4]}")

# Interface do usuário com Streamlit
st.title("Gerenciamento de Produtos")

menu = ["Cadastrar Produto", "Listar Produtos"]
escolha = st.sidebar.selectbox("Menu", menu)

if escolha == "Cadastrar Produto":
    st.subheader("Cadastrar Novo Produto")
    with st.form(key="form_cadastro"):
        nome = st.text_input("Nome do Produto")
        preco = st.text_input("Preço do Produto")
        quantidade = st.text_input("Quantidade")
        categoria = st.text_input("Categoria")
        submit_button = st.form_submit_button("Cadastrar")
    
    if submit_button:
        cadastrar_produto(nome, preco, quantidade, categoria)

elif escolha == "Listar Produtos":
    listar_produtos()
