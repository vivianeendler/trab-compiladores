import sys
from lexer import Lexer
from sintatico import Parser
from semantico import AnalisadorSemantico
from gerador import GeradorYAML

def compilar(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            codigo_fonte = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return

    tokens = Lexer(codigo_fonte).analisar()
    parser = Parser(tokens)
    ast = parser.parse()
    
    if parser.erros_sintaticos > 0:
        print("FALHA: Erros sintáticos encontrados.")
        return

    semantico = AnalisadorSemantico(ast)
    if not semantico.analisar():
        print("FALHA: Erros semânticos encontrados.")
        return
        
    print(GeradorYAML(ast).gerar())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: make run (ou python main.py <arquivo.homi>)")
    else:
        compilar(sys.argv[1])