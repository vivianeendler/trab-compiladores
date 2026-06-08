import re

class Lexer:
    def __init__(self, codigo):
        self.codigo = codigo
        self.tokens = []
        self.linha_atual = 1
        
        self.token_regex = [
            ('PALAVRA_CHAVE', r'\b(QUANDO|ESTADO|FACA|POR|FIM|E|SE)\b'),
            ('TEMPO', r'\b\d+(s|min|h)\b'),
            ('OPERADOR', r'(==|!=|>=|<=|>|<)'),
            ('ENTITY_ID', r'\b[a-z_]+\.[a-z0-9_]+\b'),
            ('STRING', r'"[^"]*"'),
            ('COMANDO', r'\b(LIGAR|DESLIGAR|ALTERNAR)\b'),
            ('COMENTARIO', r'#.*'),
            ('NOVA_LINHA', r'\n'),
            ('ESPACO', r'[ \t]+'),
            ('ERRO', r'.')
        ]

    def analisar(self):
        regex_completa = '|'.join(f'(?P<{nome}>{padrao})' for nome, padrao in self.token_regex)
        
        for match in re.finditer(regex_completa, self.codigo):
            tipo = match.lastgroup
            valor = match.group(tipo)
            
            if tipo == 'NOVA_LINHA':
                self.linha_atual += 1
            elif tipo in ['COMENTARIO', 'ESPACO']:
                continue
            elif tipo == 'ERRO':
                print(f"[ERRO LÉXICO] Linha {self.linha_atual}: Caractere inválido '{valor}'")
            else:
                self.tokens.append({'tipo': tipo, 'valor': valor, 'linha': self.linha_atual})
                
        self.tokens.append({'tipo': 'EOF', 'valor': '', 'linha': self.linha_atual})
        return self.tokens