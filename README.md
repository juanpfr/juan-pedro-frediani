# SAEP - Sistema de Gestão de Estoque

Um sistema simples de gestão de estoque desenvolvido em **Python (Flask)** com banco de dados **PostgreSQL**.

---

## 🚀 Como usar

1. **Crie o banco de dados** utilizando:
   ```
   sql/saep_db_init.sql
   ```

2. **Acesse o diretório do sistema**:
   ```
   cd sistema/
   ```

3. **Configure a variável de ambiente**:
   ```
   DATABASE_URL=postgresql://<user>:<password>@<host>/<dbname>
   ```

4. **Ajuste a URL de conexão no app.py**, se necessário.

5. **Instale as dependências**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

6. **Execute**:
   ```
   python app.py
   ```

---

## 📦 O que está incluído

- Código-fonte (Flask)
- Scripts SQL
- Documentações:
  - Requisitos funcionais
  - Requisitos de infraestrutura
  - Casos de teste

---

## 🛠 Requisitos

- **PostgreSQL:** 18+
- **Python:** 3.10+
- **Dependências:** Flask, SQLAlchemy, psycopg2
- **SO:** Windows 11 ou compatível

---

## 🔍 Funcionalidades

- Login
- Dashboard com alertas
- CRUD de produtos
- Movimentações de estoque
- Auditoria e histórico

---

## 🧪 Casos de Teste (resumo)

- Login válido e inválido
- Cadastro de produto
- Movimentações
- Estoque mínimo

---

## 📄 Documentos relacionados

- requisitos_funcionais.docx  
- casos_de_teste.docx  
- requisitos_infraestrutura.docx  

---

## 👨‍💻 Autor

Projeto desenvolvido para **Prova SAEP**.
