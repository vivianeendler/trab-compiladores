class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.ast = []
        self.erros_sintaticos = 0

        self.tabela = {
            'Programa': {
                'QUANDO': ['Automacao', 'ProgramaL']
            },
            'ProgramaL': {
                'QUANDO': ['Automacao', 'ProgramaL'],
                'EOF': []
            },
            'Automacao': {
                'QUANDO': ['@START_AUTO', 'QUANDO', 'Gatilho', 'CondicaoOpt', 'AcoesL', 'FIM', '@END_AUTO']
            },
            'Gatilho': {
                'ENTITY_ID': ['ENTITY_ID', '@GATILHO_ID', 'OpGatilho', 'TempoOpt']
            },
            'OpGatilho': {
                'ESTADO': ['ESTADO', 'STRING', '@GATILHO_ESTADO'],
                'OPERADOR': ['OPERADOR', '@GATILHO_OP', 'STRING', '@GATILHO_ESTADO_NUM']
            },
            'CondicaoOpt': {
                'E': ['@START_COND', 'E', 'SE', 'ENTITY_ID', '@COND_ID', 'OpCondicao'],
                'FACA': [],
                'FIM': []
            },
            'OpCondicao': {
                'ESTADO': ['ESTADO', 'STRING', '@COND_ESTADO'],
                'OPERADOR': ['OPERADOR', '@COND_OP', 'STRING', '@COND_ESTADO_NUM']
            },
            'TempoOpt': {
                'POR': ['POR', 'TEMPO', '@TEMPO'],
                'E': [],
                'FACA': [],
                'FIM': []
            },
            'AcoesL': {
                'FACA': ['FACA', 'Acao', 'AcoesL'],
                'FIM': []
            },
            'Acao': {
                'ENTITY_ID': ['ENTITY_ID', '@ACAO_ID', 'COMANDO', '@ACAO_CMD']
            }
        }

    def get_coluna(self, token):
        if token['tipo'] == 'PALAVRA_CHAVE':
            return token['valor']
        return token['tipo']

    def erro_sintatico(self, esperado, token):
        print(f"[ERRO SINTÁTICO] Linha {token['linha']}: Esperava o símbolo '{esperado}', mas encontrou '{token['valor']}'")
        self.erros_sintaticos += 1

    def modo_panico(self, pilha):
        while self.pos < len(self.tokens) and self.tokens[self.pos]['valor'] != 'FIM' and self.tokens[self.pos]['tipo'] != 'EOF':
            self.pos += 1
        if self.pos < len(self.tokens) and self.tokens[self.pos]['valor'] == 'FIM':
            self.pos += 1
        while len(pilha) > 0 and pilha[-1] not in ['ProgramaL', 'EOF']:
            pilha.pop()

    def parse(self):
        pilha = ['EOF', 'Programa']
        current_auto = None
        current_acao = None
        last_token = None
        
        while len(pilha) > 0:
            topo = pilha[-1]
            token = self.tokens[self.pos]
            coluna = self.get_coluna(token)
            
            if topo.startswith('@'):
                pilha.pop()
                if topo == '@START_AUTO':
                    current_auto = {'gatilho': {'tempo': None, 'operador': '=='}, 'condicao': None, 'acoes': []}
                elif topo == '@GATILHO_ID':
                    current_auto['gatilho']['entity_id'] = last_token['valor']
                    current_auto['gatilho']['linha'] = last_token['linha']
                elif topo == '@GATILHO_ESTADO':
                    current_auto['gatilho']['estado'] = last_token['valor'].replace('"', '')
                elif topo == '@GATILHO_OP':
                    current_auto['gatilho']['operador'] = last_token['valor']
                elif topo == '@GATILHO_ESTADO_NUM':
                    current_auto['gatilho']['estado'] = last_token['valor'].replace('"', '')
                elif topo == '@TEMPO':
                    current_auto['gatilho']['tempo'] = last_token['valor']
                elif topo == '@START_COND':
                    current_auto['condicao'] = {'operador': '=='}
                elif topo == '@COND_ID':
                    current_auto['condicao']['entity_id'] = last_token['valor']
                    current_auto['condicao']['linha'] = last_token['linha']
                elif topo == '@COND_ESTADO':
                    current_auto['condicao']['estado'] = last_token['valor'].replace('"', '')
                elif topo == '@COND_OP':
                    current_auto['condicao']['operador'] = last_token['valor']
                elif topo == '@COND_ESTADO_NUM':
                    current_auto['condicao']['estado'] = last_token['valor'].replace('"', '')
                elif topo == '@ACAO_ID':
                    current_acao = {'entity_id': last_token['valor'], 'linha': last_token['linha']}
                elif topo == '@ACAO_CMD':
                    current_acao['comando'] = last_token['valor']
                    current_auto['acoes'].append(current_acao)
                elif topo == '@END_AUTO':
                    if len(current_auto['acoes']) > 0:
                        self.ast.append(current_auto)
                continue
                
            if topo in self.tabela:
                if coluna in self.tabela[topo]:
                    pilha.pop()
                    producao = self.tabela[topo][coluna]
                    for simbolo in reversed(producao):
                        pilha.append(simbolo)
                else:
                    self.erro_sintatico(topo, token)
                    self.modo_panico(pilha)
            else:
                if topo == coluna:
                    last_token = token
                    pilha.pop()
                    self.pos += 1
                else:
                    self.erro_sintatico(topo, token)
                    self.modo_panico(pilha)
                    
        return self.ast