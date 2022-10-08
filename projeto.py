#1. Justificação de Texto
def limpa_texto(cad):
    """Recebe cadeia de caracteres (cad) e devolve uma cadeia correspondente à
    remoção de caracteres ASCII brancos, substituidos pelo espaço (0x20)
    eliminando ainda sequências contínuas de espaços"""
    cad = cad.strip(' ')               # Remove espaços a cada lado do input
    cad = cad.replace('\t',' ')        # Devolve a cadeia fornecida trocando os caracteres definidos  pelo espaço ' '
    cad = cad.replace('\n',' ')
    cad = cad.replace('\v',' ')
    cad = cad.replace('\f',' ')
    cad = cad.replace('\r',' ')
    cad = cad.replace('  ',' ')
    while int(cad.find('  ')) > 0:
        cad = cad.replace('  ',' ')    # Enquanto existirem sequencias de 2 ou mais espaços, substitui as sequências de 2 espaços por 1
    return cad.strip(' ') 

def corta_texto(cad,col):
    """Limita cadeias de caracteres de acordo com a largura fornecida.
    Devolve duas cadeias, a cadeia cortada e a sobrante cadeia inalterada"""
    cut = cad[:col]  
    if len(cad) > col and cut.rfind(' ') != -1:                # condição evita funcionalidade indesejável do método .rfind
        cut = cut[:cut.rfind(' ')].strip(' ')                  # Limita a cadeia cortada até ao ultimo espaço eliminando palavras incompletas
    uncut = cad[len(cut):].strip(' ')                          # A restante cadeia começa a após o ultimo caractér presente na cadeia cortada
    return cut, uncut      

def insere_espacos(cad, col):
    """Recebe cadeia de caracteres e um inteiro correspondente à largura da coluna"""
    if cad.find(' ') == -1:                                    # Não encontrar espaços implica a existência de uma só palavra 
        return cad.ljust(col,' ')                                     
    else:
        count = 1                                              # Número inicial de espaços
        while len(cad) <= col:
            cad = cad.replace(' '*count, ' '*(count+1))        # Aumenta todas as instâncias de espaços (pode resultar em len(cad)>col)
            count +=1                                          # Atualiza a dimensão atual das sequências de espaços
        while len(cad) > col:
            cad = cad.replace(' '*count, ' '*(count-1))                   # Reduz todas as sequências em um espaço
            cad = cad.replace(' '*(count-1), ' '*(count), col-len(cad))   # permitindo que se aumente cada uma das sequencias por 1 espaço   
    return cad                                                            # da esquerda para a direita

def justifica_texto(cad, col):
    """Recebe cadeia de caracteres e um inteiro correspondente à largura da coluna.
    Aceita tuplos."""
    if type(cad) != str or type(col) != int or col < 1 or ((not col>= cad.find(' ')> -1) and len(cad)>col) or len(cad) == 0:
        raise ValueError('justifica_texto: argumentos invalidos')              
    else:
        lines = len(cad)//col                                                  # Prevê o número de linhas necessárias para a justificação
        next = limpa_texto(cad)                                                # Variavel que guarda o texto restante     
        if len(cad) > col and lines == 1:                                      # Previne caso raro no qual uma unica linha resulta num output
            lines += 1                                                         # que excede a largura definida. eg. justifica_texto('123456 789', 6)
        cad = []  
        for i in range(lines-1):                                               # Itera sobre cada linha exceto a ultima
            cad.append(str(insere_espacos(corta_texto(next,col)[0], col)))     # Adiciona à lista a cadeia cortada e espaçada
            next = str(corta_texto(next,col)[1])                               # Prepara a cadeia inalterada para o proximo ciclo
        cad.append(next.ljust(col,' '))                                        # A ultima linha de cada texto é unicamente justificada à esquerda
        return tuple(cad)

#2. Método de Hondt
def calcula_quocientes(votes, seats):        
    """"Aceita um dicionário partidos : no. de votos e devolve um dicionário 
    distinto do original com os quocientes dos resultados
    desses partidos, segundo o método de Hondt"""
    results = dict(votes)                    # Cria um dicionário-alvo para os quocientes
    parties = list(votes.keys())
    for i in range(0,len(parties)):          # Itera sobre todas as entradas ou "partidos"
        quo = list()                         # Cria uma lista-destino para os quocientes a serem calculados
        for d in range(1,seats):             # Para cada divisão
            quo.append(votes[parties[i]]/d)  # Adiciona o quociente dos votos do partido a ser trabalhado ao fim da lista
        results.update({parties[i]: quo})    # Atualiza a entrada do respetivo partido com os resultados apurados
    return results

def atribui_mandatos():
    
            
#3. Solução de Sistemas de Equações