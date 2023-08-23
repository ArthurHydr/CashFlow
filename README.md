# Cash Flow Management App

This is a simple Python application that helps you manage your cash flow by tracking daily investments, returns, and calculating net revenue.

## Features

- Add daily investment and return records.
- Save and load data from a SQLite database file.
- Calculate faturamento líquido (net revenue) considering a manual tax or the calculated Kiwify tax.

## Prerequisites

- Python 3.x
- PySimpleGUI library
- SQLite3 library

## Getting Started

1. Clone this repository to your local machine.
2. Install the required libraries:

```bash
pip install PySimpleGUI
```

3. Run the cash_flow_app.py script:

```bash
python cash_flow_app.py
```
## Usage

1. Launch the application and interact with the graphical user interface.
2. Click the "Abrir Tabela" button to load an existing table from a database file or create a new one.
3. Add daily investment and return records using the provided input fields and buttons.
4. Click the "Salvar Tabela" button to save the data to a database file.
5. Calculate the net revenue by entering a manual tax or using the Kiwify tax, then click the "Calcular" button.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- This application was developed using the [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/) library.
- SQLite3 was used for data storage.
