# Controle_Estoque

# 📦 Sistema de Controle de Estoque

Sistema web desenvolvido em **Python** para controle básico de estoque, permitindo o cadastro e acompanhamento de produtos, movimentações de entrada e saída, controle de estoque mínimo e gerenciamento de usuários.

O projeto foi desenvolvido como parte das atividades acadêmicas do curso de **Análise e Desenvolvimento de Sistemas (ADS)**.

---

## 🎯 Objetivo

O objetivo do sistema é disponibilizar uma aplicação simples para auxiliar no controle de produtos e suas movimentações, permitindo visualizar o estoque atual e identificar produtos que estejam abaixo ou no nível mínimo definido.

O sistema também possui controle de acesso por perfil de usuário, diferenciando as permissões entre **Administrador** e **Usuário Comum**.

---

## ⚙️ Funcionalidades

### 🔐 Autenticação

* Login de usuários.
* Validação de login e senha.
* Controle de sessão.
* Logout.
* Senhas armazenadas utilizando hash.
* Perfis de acesso:

  * Administrador
  * Usuário Comum

### 👤 Usuários

O Administrador pode:

* Cadastrar novos usuários.
* Definir o perfil do usuário.
* Visualizar os usuários cadastrados.

Usuários comuns não possuem acesso ao gerenciamento de usuários.

### 📦 Produtos

O sistema permite:

* Cadastrar produtos.
* Editar produtos.
* Consultar produtos cadastrados.
* Visualizar a quantidade atual em estoque.
* Definir estoque mínimo.
* Identificar produtos com estoque baixo.

### 🔄 Movimentações

É possível registrar:

* Entrada de produtos.
* Saída de produtos.
* Quantidade movimentada.
* Usuário responsável pela movimentação.

O sistema atualiza automaticamente a quantidade disponível em estoque.

Também existe uma validação que impede uma saída maior que a quantidade disponível.

### 📋 Histórico

O sistema mantém um histórico das movimentações contendo:

* Produto.
* Tipo da movimentação.
* Quantidade.
* Usuário responsável.
* Data e hora.

---

## 🛡️ Validações e segurança

O projeto possui algumas medidas para garantir a integridade dos dados:

* Validação dos campos obrigatórios.
* Bloqueio de valores negativos.
* Validação de quantidade nas movimentações.
* Bloqueio de saída superior ao estoque disponível.
* Restrição de acesso às funcionalidades administrativas.
* Controle de sessão para acesso às áreas internas.
* Senhas armazenadas com hash.
* Chaves estrangeiras no banco de dados.
* Restrições de valores permitidos para perfis e tipos de movimentação.

Informações sensíveis de configuração do banco de dados não são armazenadas no repositório público do projeto.

---

## 🧰 Tecnologias utilizadas

* **Python**
* **Flask**
* **MySQL**
* **HTML5**
* **CSS3**
* **MySQL Connector/Python**
* **Git e GitHub**

---

## 📁 Estrutura do projeto

```text
App_Controle_Estoque/
│
├── app.py
├── config.example.py
├── .gitignore
├── README.md
│
├── database/
│   └── connection.py
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── produtos.html
│   ├── produto_form.html
│   ├── produto_editar.html
│   ├── movimentacao.html
│   ├── historico.html
│   ├── usuarios.html
│   └── sucesso.html
│
├── static/
│   └── css/
│       └── style.css
│
└── sql/
    └── database.sql
```

---

## 🗄️ Banco de dados

O sistema utiliza **MySQL**.

O banco possui três entidades principais:

### Usuário

Armazena os usuários responsáveis pelo acesso ao sistema.

### Produto

Armazena os produtos e as informações relacionadas ao estoque atual e ao estoque mínimo.

### Movimentação

Registra as entradas e saídas de produtos e relaciona cada movimentação ao produto e ao usuário responsável.

### Relacionamentos

```text
USUARIO 1 ─────────── N MOVIMENTACAO N ─────────── 1 PRODUTO
```

Uma movimentação pertence a um usuário e a um produto.

---

## 🚀 Como executar o projeto

### 1. Pré-requisitos

É necessário ter instalado:

* Python 3.x
* MySQL
* Git

---

### 2. Clonar o projeto

```bash
git clone https://github.com/LeonardoShimazaki/Controle_Estoque.git
```

Depois entre na pasta:

```bash
cd Controle_Estoque
```

---

### 3. Criar o ambiente virtual

No Windows:

```bash
python -m venv venv
```

Ative o ambiente virtual:

```bash
venv\Scripts\activate
```

---

### 4. Instalar as dependências

```bash
pip install Flask mysql-connector-python
```

---

### 5. Configurar o banco de dados

Execute o arquivo:

```text
sql/database.sql
```

no MySQL para criar o banco e suas tabelas.

---

### 6. Configurar a conexão

O arquivo `config.py` não é disponibilizado no repositório porque pode conter informações sensíveis.

Utilize o arquivo:

```text
config.example.py
```

como modelo.

Copie o arquivo e renomeie para:

```text
config.py
```

Depois informe a senha do seu usuário MySQL:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "SUA_SENHA_DO_MYSQL",
    "database": "controle_estoque"
}
```

---

### 7. Executar a aplicação

Com o ambiente virtual ativado:

```bash
python app.py
```

Depois acesse no navegador o endereço exibido pelo Flask, normalmente:

```text
http://127.0.0.1:5000
```

---

## 👥 Usuários de demonstração

O banco utilizado no projeto possui usuários para demonstração dos diferentes perfis de acesso.

| Perfil        | Login   | Senha    |
| ------------- | ------- | -------- |
| Administrador | `admin` | `123456` |
| Usuário Comum | `comum` | `123456` |

> As credenciais acima são destinadas exclusivamente à demonstração acadêmica do sistema.

---

## 📌 Regras principais

* Apenas Administradores podem cadastrar usuários.
* Usuários autenticados podem consultar produtos.
* Usuários autenticados podem realizar movimentações.
* Entradas aumentam o estoque.
* Saídas reduzem o estoque.
* Não é permitido realizar uma saída maior que o estoque disponível.
* Quantidades de movimentação devem ser maiores que zero.
* Produtos com quantidade menor ou igual ao estoque mínimo são identificados como estoque baixo.

---

## 🎓 Projeto acadêmico

Projeto desenvolvido para a disciplina de **Desenvolvimento com Python**, no curso de **Análise e Desenvolvimento de Sistemas (ADS)**.

O sistema foi desenvolvido com foco na aplicação prática de conceitos de:

* Programação em Python.
* Desenvolvimento web.
* Banco de dados relacional.
* Modelagem de dados.
* Autenticação.
* Controle de acesso.
* Validação de dados.
* Operações de estoque.
* Integração entre aplicação e banco de dados.

---

## 👨‍💻 Autor

**Leonardo Shimazaki**

Projeto acadêmico — 2026.
