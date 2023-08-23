import PySimpleGUI as sg
import sqlite3

# Função para atualizar a tabela
def atualizar_tabela(window, data):
    table_data = [
        [item['nome'], item['dia'], item['investimento'], item['retorno'], item['faturamento']]
        for item in data
    ]
    window['table'].update(values=table_data)

def calcular_faturamento_liquido(faturamento_bruto, taxa):
    return faturamento_bruto - taxa

def salvar_dados(data, nome_arquivo):
    conn = sqlite3.connect(nome_arquivo)
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS investimentos (nome TEXT, dia INTEGER, investimento REAL, retorno REAL, faturamento REAL)')

    for item in data:
        cursor.execute('INSERT INTO investimentos VALUES (?, ?, ?, ?, ?)', (item['nome'], item['dia'], item['investimento'], item['retorno'], item['faturamento']))

    conn.commit()
    conn.close()

def carregar_dados(nome_arquivo):
    try:
        conn = sqlite3.connect(nome_arquivo)
        cursor = conn.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS investimentos (nome TEXT, dia INTEGER, investimento REAL, retorno REAL, faturamento REAL)')  # Criar tabela se não existir

        cursor.execute('SELECT * FROM investimentos')
        data = []
        for row in cursor.fetchall():
            if len(row) == 5:
                data.append({'nome': row[0], 'dia': row[1], 'investimento': row[2], 'retorno': row[3], 'faturamento': row[4]})

        conn.close()
        return data
    except sqlite3.OperationalError as e:
        sg.popup_error(f"Erro ao abrir o banco de dados: {e}")
        return []

sg.theme('DarkGrey5')  # Aplicando o tema escuro

# Layout da interface gráfica
layout = [
    [sg.Text('Fluxo de Caixa', font=('Helvetica', 16))],
    [sg.Button('Abrir Tabela', button_color=('white', '#007BFF')), sg.Button('Salvar Tabela', button_color=('white', '#28A745'))],
    [sg.Text('Nome da Tabela:'), sg.InputText(key='nome_arquivo'), sg.FileSaveAs(target='nome_arquivo')],
    [sg.HorizontalSeparator()],
    [sg.Text('Investimento Diário:'), sg.InputText(key='investimento')],
    [sg.Text('Retorno Diário:'), sg.InputText(key='retorno')],
    [sg.Button('Adicionar Registro', button_color=('white', '#007BFF'))],
    [sg.Text('Histórico de Investimentos', font=('Helvetica', 12))],
    [sg.Table(values=[], headings=['Nome', 'Dia', 'Investimento', 'Retorno', 'Faturamento'], key='table', num_rows=10, justification='right')],
    [sg.HorizontalSeparator()],
    [sg.Text('Calcular Faturamento Líquido', font=('Helvetica', 12))],
    [sg.Button('Kiwify', button_color=('white', '#343A40')), sg.InputText(key='taxa_manual', size=(10,1)), sg.Button('Calcular', button_color=('white', '#28A745'))],
    [sg.Text('Faturamento Bruto: '), sg.Text('', size=(10,1), key='faturamento_bruto')],
    [sg.Text('Taxa: '), sg.Text('', size=(10,1), key='taxa')],
    [sg.Text('Faturamento Líquido: '), sg.Text('', size=(10,1), key='faturamento_liquido')],
]

window = sg.Window('Fluxo de Caixa', layout, background_color='#282C35')  # Cor de fundo escura

data = []  # Inicializa a lista vazia de dados
faturamento_acumulado = 0

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Adicionar Registro':
        investimento = float(values['investimento']) if values['investimento'] else 0
        retorno = float(values['retorno']) if values['retorno'] else 0

        if investimento > 0 and retorno == 0:
            faturamento_acumulado -= investimento
        elif investimento !=0 and retorno !=0:
            faturamento_acumulado = faturamento_acumulado - investimento + retorno
        elif retorno > 0:
            faturamento_acumulado += retorno

        nome_arquivo = values['nome_arquivo']
        if nome_arquivo.endswith('.db'):
            nome_arquivo = nome_arquivo[:-3]  # Remove a extensão .db se presente

        data.append({
            'nome': nome_arquivo,
            'dia': len(data) + 1,
            'investimento': investimento,
            'retorno': retorno,
            'faturamento': faturamento_acumulado
        })

        atualizar_tabela(window, data)
        window['investimento'].update('')
        window['retorno'].update('')
        window['nome_arquivo'].update('')

    elif event == 'Salvar Tabela':
        salvar_dados(data, f'{values["nome_arquivo"]}.db')

    elif event == 'Abrir Tabela':
        arquivo_selecionado = sg.popup_get_file('Selecione um arquivo', file_types=(('Bancos de Dados', '*.db'),))
        if arquivo_selecionado:
            data = carregar_dados(arquivo_selecionado)
            faturamento_acumulado = data[-1]['faturamento'] if data else 0
            atualizar_tabela(window, data)

    elif event == 'Kiwify':
        taxa_kiwify = 2.49 + (0.0899 * faturamento_acumulado)
        window['taxa_manual'].update(taxa_kiwify)

    elif event == 'Calcular':
        taxa_manual = float(values['taxa_manual']) if values['taxa_manual'] else 0
        faturamento_bruto = faturamento_acumulado
        taxa_total = taxa_manual + faturamento_acumulado * 0.0899  # Adiciona a taxa percentual
        faturamento_liquido = calcular_faturamento_liquido(faturamento_bruto, taxa_total)

        window['faturamento_bruto'].update(f'{faturamento_bruto:.2f}')
        window['taxa'].update(f'{taxa_total:.2f}')
        window['faturamento_liquido'].update(f'{faturamento_liquido:.2f}')

window.close()
