import time

class GeradorYAML:
    def __init__(self, ast):
        self.ast = ast

    def mapear_comando(self, comando):
        mapa = {'LIGAR': 'turn_on', 'DESLIGAR': 'turn_off', 'ALTERNAR': 'toggle'}
        return mapa.get(comando, 'turn_on')

    def gerar(self):
        yaml_output = ""
        for i, automacao in enumerate(self.ast):
            gatilho = automacao['gatilho']
            condicao = automacao['condicao']
            acoes = automacao['acoes']
            
            timestamp_id = str(int(time.time() * 1000) + i)
            yaml_output += f"- id: '{timestamp_id}'\n"
            yaml_output += f"  alias: Automacao Homi {i+1}\n"
            yaml_output += "  triggers:\n"
            
            if gatilho['operador'] == '==':
                yaml_output += "  - trigger: state\n"
                yaml_output += f"    entity_id:\n    - {gatilho['entity_id']}\n"
                yaml_output += f"    to: '{gatilho['estado']}'\n"
            else:
                yaml_output += "  - trigger: numeric_state\n"
                yaml_output += f"    entity_id:\n    - {gatilho['entity_id']}\n"
                if '>' in gatilho['operador']:
                    yaml_output += f"    above: {gatilho['estado']}\n"
                elif '<' in gatilho['operador']:
                    yaml_output += f"    below: {gatilho['estado']}\n"
            
            if gatilho['tempo']:
                segundos = gatilho['tempo'].replace('s', '').replace('min', '')
                yaml_output += "    for:\n"
                yaml_output += f"      seconds: {segundos if 's' in gatilho['tempo'] else int(segundos)*60}\n"
                
            yaml_output += "  conditions:\n"
            if condicao:
                if condicao['operador'] == '==':
                    yaml_output += "  - condition: state\n"
                    yaml_output += f"    entity_id: {condicao['entity_id']}\n"
                    yaml_output += f"    state: '{condicao['estado']}'\n"
                else:
                    yaml_output += "  - condition: numeric_state\n"
                    yaml_output += f"    entity_id: {condicao['entity_id']}\n"
                    if '>' in condicao['operador']:
                        yaml_output += f"    above: {condicao['estado']}\n"
                    elif '<' in condicao['operador']:
                        yaml_output += f"    below: {condicao['estado']}\n"
            else:
                yaml_output += "  []\n"
                
            yaml_output += "  actions:\n"
            for acao in acoes:
                dominio = acao['entity_id'].split('.')[0]
                servico = f"{dominio}.{self.mapear_comando(acao['comando'])}"
                yaml_output += f"  - action: {servico}\n"
                yaml_output += "    target:\n"
                yaml_output += f"      entity_id: {acao['entity_id']}\n"
            
            yaml_output += "  mode: single\n\n"
            
        return yaml_output