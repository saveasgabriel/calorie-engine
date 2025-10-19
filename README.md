---

# Calculadora de Calorias e Metas Nutricionais

Uma aplicação web desenvolvida com **Streamlit** para ajudar usuários a entenderem seu gasto calórico diário e a definirem metas nutricionais realistas com base em seus objetivos.
A ferramenta utiliza fórmulas validadas e um modelo de projeção dinâmico para oferecer resultados precisos e personalizados.

---

## Funcionalidades Principais

A calculadora guia o usuário através de um processo de **5 passos simples e intuitivos**:

1. **Perfil do Usuário**
   Calcula a **Taxa Metabólica Basal (TMB)** a partir de dados básicos.

2. **Registro de Treinos**
   Adiciona o gasto calórico de atividades físicas planejadas usando o conceito de **MET**.

3. **Atividades do Dia a Dia**
   Estima o gasto calórico de atividades não planejadas (**NEAT**) com base na contagem de passos.

4. **Resultado Final**
   Consolida todas as informações para apresentar o **Gasto Energético Total Diário (GETD)**.

5. **Definição de Metas**
   Permite ao usuário definir um objetivo (perder, manter ou ganhar peso) e visualizar um **plano nutricional** com:

   * Distribuição de macronutrientes
   * Exemplos de alimentos
   * Projeção de peso realista

---

## Conceitos e Cálculos Explicados

A precisão da calculadora é baseada em metodologias e fórmulas consagradas na área da nutrição e fisiologia do exercício.

---

### 🔹 Passo 1: Taxa Metabólica Basal (TMB)

**O que é?**
A quantidade de energia (calorias) que seu corpo gasta em repouso absoluto para manter as funções vitais.

**Como é calculada?**
Fórmula de **Mifflin-St Jeor**:

* **Homens:**
  `TMB = 10 * peso(kg) + 6.25 * altura(cm) - 5 * idade + 5`

* **Mulheres:**
  `TMB = 10 * peso(kg) + 6.25 * altura(cm) - 5 * idade - 161`

---

### 🔹 Passo 2: Gasto com Atividades Físicas

**O que é?**
Gasto calórico adicional de treinos planejados como musculação, corrida, natação etc.

**Como é calculado?**
Usa o conceito de **MET (Equivalente Metabólico da Tarefa)**:

> `Gasto por Sessão (kcal) = MET * peso(kg) * duração(horas)`

---

### 🔹 Passo 3: Atividades do Dia a Dia (NEAT)

**O que é?**
**NEAT (Termogênese de Atividades Não-Exercício)** representa o gasto de atividades informais como caminhar, subir escadas, tarefas domésticas etc.

**Como é calculado?**

> `Gasto com Passos (kcal) = Passos Diários * peso(kg) * 0.0005`

---

### 🔹 Passo 4: Gasto Energético Total Diário (GETD)

**O que é?**
Soma de todos os gastos calóricos do dia. Quantidade de calorias para **manter o peso atual**.

**Como é calculado?**

> `GETD = TMB + (Gasto Semanal dos Treinos / 7) + Gasto com Passos`

---

### 🔹 Passo 5: Metas Calóricas e Projeção de Peso Dinâmica

**O que é?**
Baseado no GETD, o usuário define uma **meta calórica** para perder, manter ou ganhar peso.

**Como a projeção de peso é feita?**

A aplicação utiliza um **modelo dinâmico e realista**:

* **Perda de peso:**
  Conforme você perde peso, o corpo precisa de menos energia → o déficit diminui → a perda desacelera (efeito *platô*).

* **Ganho de peso:**
  Um corpo mais pesado gasta mais energia → o superávit diminui → o ganho desacelera.

**Referência usada:**

> `7700 kcal ≈ 1 kg de gordura corporal`

---

## Como Executar o Projeto

### Pré-requisitos

* Python 3.8 ou superior
* `pip` (gerenciador de pacotes do Python)

### Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/calorie-engine.git
cd calorie-engine
```

Crie e ative um ambiente virtual:

```bash
# Para Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Para Windows
python -m venv venv
.\venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

### Executando a Aplicação

Com as dependências instaladas, execute:

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador.

---

## Tecnologias Utilizadas

* **Python**: Linguagem principal
* **Streamlit**: Framework para criação da interface web interativa

---

## Autor

**Gabriel França**
Email: [saveasgabriel@gmail.com](mailto:saveasgabriel@gmail.com)
Instagram: [@saveasfranca](https://instagram.com/saveasfranca)

---

Se quiser, posso gerar também uma versão `.md` pronta para download. Deseja isso?

