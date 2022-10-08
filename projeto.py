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

def dict_sorter(unsort):
    """Recebe um dicionário arbitráriamente ordenado e devolve 
    um dicionário ordenado segundo os valores presentes, em ordem crescente"""
    count = 0                                # Contador de vezes em que nenhuma operação é necessária
    unsort = list(unsort.items())            # Lista contendo tuplos ('partido','votos')
    sort = {}
    while count < len(unsort):               # Se toda a lista for avaliada sem operações, considera-se ordenada               
        if count+1 < len(unsort) and (unsort[count])[1] > (unsort[count+1])[1]: # Compara o valor númerico presente num dado
            unsort.append(unsort[count])                                        # tuplo com o valor numérico do tuplo seguinte
            unsort.remove(unsort[count])
            count = 0                        # Os tuplos de valores maiores são sucessivamente 'transportados' para o fim da lista
        else:
            count += 1
    for i in range(len(unsort)):             # Converte a lista de tuplos num dicionário
        sort.update({(unsort[i])[0]:(unsort[i])[1]})
    return sort

def atribui_mandatos(votes, seats):
    """Aceita um dicionário partidos : no de votos e devolve uma lista
    contendo a lista ordenada dos partidos que obtiveram deputados,
    por ordem de obtenção"""
    quo = calcula_quocientes(dict_sorter(votes), seats) # necessária para garantir a correta atribuição em caso de empate
    parties = list(quo.keys())
    results = list(quo.values())                           
    place = list()
    for i in quo:
        results.extend(results[0])              # adiciona à lista 'results' os valores obtidos pelo método de hondt
        results.pop(0)
    results.sort(reverse=True)                  # Ordena a lista por ordem decrescente de quocientes
    for i in range(0, len(results)):            # Compara cada quociente da lista 'results'
        for p in parties:                       # aos quocientes de cada partido segundo a lista 'quo'
            if results[i] in quo.get(p):
                place.append(p)                 # Adiciona os partidos à lista place por ordem de eleição de deputados
    return place[0:seats]                       # Limita a lista ao número de deputados pedido

def obtem_partidos(votes):
    """Aceita um dicionário cujos valores são dicionários, que por sua vez
    é constituido por dicionários e devolve a lista alfabéticamente ordenada das chaves"""
    circles = list(votes.values())              # Lista dos dicionários-resultado dos vários circulos
    results = []
    parties = []
    p = 0                                       # Variável contadora
    for c in circles:                           # Em cada resultado de um circulo eleitoral, encontrar 
        results.append(c.get('votos'))          # o dicionário partido:votos 

    for i in results:                           # por cada dicionário partido:votos
        parties.extend(list(i.keys()))          # adicionar os partidos encontrados à lista
    
    parties.sort()
    for i in parties:
        for l in range(parties.count(i)-1):     # Se existe mais do que uma instância de um partido i
            parties.remove(i)                   # removem-se as instâncias sobrantes
    return parties


print(obtem_partidos({
            'Endor':   {'deputados': 7, 
                        'votos': {'A':12000, 'B':7500, 'C':5250, 'D':3000}},
            'Hoth':    {'deputados': 6, 
                        'votos': {'A':9000, 'B':11500, 'D':1500, 'E':5000}},
            'Tatooine': {'deputados': 3, 
                        'votos': {'A':3000, 'B':1900}}}))
            
#3. Solução de Sistemas de Equações