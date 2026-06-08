class TabelaDeSimbolos:
    def __init__(self):
        self.simbolos = {}

    def adicionar(self, nome, tipo, escopo='global'):
        if nome not in self.simbolos:
            self.simbolos[nome] = {'tipo': tipo, 'escopo': escopo}

    def obter(self, nome):
        return self.simbolos.get(nome)


class AnalisadorSemantico:
    def __init__(self, ast):
        self.ast = ast
        self.erros_semanticos = 0
        self.tabela = TabelaDeSimbolos()
        
        self.dominios_atuadores = ['light', 'switch', 'fan', 'climate', 'input_boolean', 'media_player', 'notify']
        self.dominios_leitura = ['sensor', 'binary_sensor', 'sun', 'weather', 'person', 'timer', 'alarm_control_panel']
        self.dominios_numericos = ['sensor', 'climate', 'input_number']

    def popular_tabela(self):
        for automacao in self.ast:
            gatilho_id = automacao['gatilho']['entity_id']
            self.tabela.adicionar(gatilho_id, gatilho_id.split('.')[0])
            if automacao['condicao']:
                cond_id = automacao['condicao']['entity_id']
                self.tabela.adicionar(cond_id, cond_id.split('.')[0])
            for acao in automacao['acoes']:
                acao_id = acao['entity_id']
                self.tabela.adicionar(acao_id, acao_id.split('.')[0])

    def verificar_consistencia(self):
        for automacao in self.ast:
            g_id = automacao['gatilho']['entity_id']
            g_op = automacao['gatilho']['operador']
            simb_g = self.tabela.obter(g_id)
            if simb_g and g_op in ['>', '<', '>=', '<=']:
                if simb_g['tipo'] not in self.dominios_numericos:
                    print(f"[ERRO SEMÂNTICO] Linha {automacao['gatilho']['linha']}: Operador relacional '{g_op}' não pode ser aplicado à entidade '{g_id}' do tipo '{simb_g['tipo']}'.")
                    self.erros_semanticos += 1

            if automacao['condicao']:
                c_id = automacao['condicao']['entity_id']
                c_op = automacao['condicao']['operador']
                simb_c = self.tabela.obter(c_id)
                if simb_c and c_op in ['>', '<', '>=', '<=']:
                    if simb_c['tipo'] not in self.dominios_numericos:
                        print(f"[ERRO SEMÂNTICO] Linha {automacao['condicao']['linha']}: Operador relacional '{c_op}' não pode ser aplicado à entidade '{c_id}'.")
                        self.erros_semanticos += 1

            for acao in automacao['acoes']:
                entity_id = acao['entity_id']
                comando = acao['comando']
                linha = acao['linha']

                simbolo = self.tabela.obter(entity_id)
                if simbolo:
                    tipo_entidade = simbolo['tipo']
                    if tipo_entidade in self.dominios_leitura and tipo_entidade not in self.dominios_atuadores:
                        print(f"[ERRO SEMÂNTICO] Linha {linha}: O tipo '{tipo_entidade}' é estritamente de leitura. Operação '{comando}' inválida em '{entity_id}'.")
                        self.erros_semanticos += 1
                else:
                    print(f"[ERRO SEMÂNTICO] Linha {linha}: Identificador '{entity_id}' não declarado.")
                    self.erros_semanticos += 1

    def analisar(self):
        self.popular_tabela()
        self.verificar_consistencia()
        return self.erros_semanticos == 0