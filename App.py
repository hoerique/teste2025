import toml
import gspread
from google.oauth2.service_account import Credentials

# Carregar credenciais do arquivo TOML
with open("config.toml", "r") as f:
    config = toml.load(f)

# Extraindo informações do TOML
spreadsheet_id = config["google_sheets"]["spreadsheet_id"]
service_account_info = config["service_account"]

# Criar credenciais do Google
creds = Credentials.from_service_account_info(service_account_info, scopes=["https://www.googleapis.com/auth/spreadsheets"])
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
    print("✅ Produto cadastrado com sucesso!")

# Função para listar produtos
def listar_produtos():
    dados = sheet.get_all_values()
    if len(dados) <= 1:
        print("⚠️ Nenhum produto cadastrado!")
        return
    
    print("\n📦 Lista de Produtos:")
    for row in dados[1:]:
        print(f"ID: {row[0]} | Nome: {row[1]} | Preço: R${row[2]} | Qtd: {row[3]} | Categoria: {row[4]}")

# Menu interativo
while True:
    print("\n1️⃣ Cadastrar Produto\n2️⃣ Listar Produtos\n3️⃣ Sair")
    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        nome = input("Nome do Produto: ")
        preco = input("Preço do Produto: ")
        quantidade = input("Quantidade: ")
        categoria = input("Categoria: ")
        cadastrar_produto(nome, preco, quantidade, categoria)
    
    elif escolha == "2":
        listar_produtos()
    
    elif escolha == "3":
        print("👋 Saindo...")
        break
    
    else:
        print("❌ Opção inválida!")
