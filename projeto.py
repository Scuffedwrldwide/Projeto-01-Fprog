##########################
#1. Justificação de Texto#
##########################

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

####################
#2. Método de Hondt#
####################

def aux_check_arg(arg,typ):

    if (type(arg) == dict and arg == {}) or (type(arg) == list and arg == ()) or (type(arg) == int and arg < 0) or (type(arg) == tuple and arg ==()):
        raise ValueError('obtem_resultado_eleicoes: argumento invalido')
    if type(arg) != typ:
        raise ValueError('obtem_resultado_eleicoes: argumento invalido')

def aux_dict_sorter(unsort):
    """Recebe um dicionário arbitráriamente ordenado e devolve 
    um dicionário ordenado segundo os valores presentes, em ordem crescente"""
    count = 0                                # Contador de vezes em que nenhuma operação é necessária
    unsort = list(unsort.items())            # Lista contendo tuplos ('partido','votos')
    sort = {}
    for i in range(0, len(unsort)):
        if type(unsort[i][1]) == str or unsort[i][1]<= 0: raise ValueError('obtem_resultado_eleicoes: argumento invalido')
        aux_check_arg(unsort[i][1], int)     # Numero de votos de um partido constante na lista não pode ser 0s
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

def aux_obtem_partido_votos(info, dep=0):
    """Dado um dicionário contendo os resultados de vários circlos eleitorais
    devolve uma lista de dicionários contendo a informação partido:votos
    ou, opcionalmente, a lista do número de deputados a serem eleitos por circulo"""
    circles = list(info.values())                # Lista dos dicionários-resultado dos vários circulos
    results = []
    for c in circles:  
        aux_check_arg(c, dict)                        
        if dep == 1:                             # (opcional) Em cada resultado de um circulo eleitoral, encontrar 
            results.append(c.get('deputados'))   # o dicionário deputados:'int'
        else:                                    # Em cada resultado de um circulo eleitoral, encontrar 
            results.append(c.get('votos'))       # o dicionário partido:votos
    return results

def aux_sorter(lst, par, index):
    """Compara e ordena tuplos de uma lista com base num critério arbitrário"""
    breaker = 0                                  # Failsafe contra IndexErrors
    for i in range(len(lst)):
        aux_check_arg((lst[par-1])[index],int)   # Número de votos deve ser inteiro
        aux_check_arg((lst[par])[index],int)
        if (lst[par-1])[index] < (lst[par])[index]:
                    lst.append(lst[par-1])
                    lst.remove(lst[par-1])
                    par = 1
        elif par == len(lst) - 1:                # Evita que 'par' exceda o indice máximo da lista                 
            breaker = 1
        else:
            par += 1                             # Caso não haja operação a efetuar, avança-se para o par seguinte
    return (lst, breaker)

def calcula_quocientes(votes, seats):        
    """"Aceita um dicionário partidos : no. de votos e devolve um dicionário 
    distinto do original com os quocientes dos resultados
    desses partidos, segundo o método de Hondt"""
    results = dict(votes)                    # Cria um dicionário-alvo para os quocientes
    parties = list(votes.keys())
    for i in range(0,len(parties)):          # Itera sobre todas as entradas ou "partidos"
        quo = list()                         # Cria uma lista-destino para os quocientes a serem calculados
        for d in range(1,seats+1):           
            quo.append(votes[parties[i]]/d)  # Adiciona o quociente dos votos do partido a ser trabalhado ao fim da lista
        results.update({parties[i]: quo})    # Atualiza a entrada do respetivo partido com os resultados apurados
    return results

def atribui_mandatos(votes, seats):
    """Aceita um dicionário partidos : no de votos e devolve uma lista
    contendo a lista ordenada dos partidos que obtiveram deputados,
    por ordem de obtenção"""
    quo = calcula_quocientes(aux_dict_sorter(votes), seats) # necessária para garantir a correta atribuição em caso de empate
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

def obtem_partidos(info):
    ### DUVIDA, POSSO VERIFICAR ARGUMENTOS NESTA FUNÇÃO ###
    """Aceita um dicionário cujos valores são dicionários, que por sua vez
    é constituido por dicionários e devolve a lista alfabéticamente ordenada das chaves
    destes ultimos, evitando repetições"""
    results = aux_obtem_partido_votos(info)
    parties = []
    for i in results:                           # por cada dicionário partido:votos
        aux_check_arg(i,dict)
        parties.extend(list(i.keys()))          # adicionar os partidos encontrados à lista de assentos
    for p in range(0, len(parties)):
        aux_check_arg(parties[p], str)          # Nome de partido deve ser uma string
    for p in parties.copy():
        for l in range(parties.count(p)-1):     # Se existe mais do que uma instância de um partido i
            parties.remove(p)                   # removem-se as instâncias sobrantes
    parties.sort()
    return parties

def obtem_resultado_eleicoes(info):
    """Aceita um dicionário com várias parcelas de informação (Circulo, Deputados, Votos, Partidos), 
    por sua vez contida em dicionários (Deputados, Votos), e devolve uma lista de tuplos
    com a relevante informação devidamente analizada (Partido, Deputados, Votos)"""

    aux_check_arg(info,dict)
    parties = obtem_partidos(info)                      # Lista alfabética dos partidos
    aux_check_arg(parties,list)
    circles = aux_obtem_partido_votos(info)             # Lista dos vários resultados por circulo
    aux_check_arg(circles,list)
    dep = aux_obtem_partido_votos(info, 1)              # Lista correspondente aos deputados por circulo
    aux_check_arg(dep,list)
    seats = 0
    results = []
    par = 0                                             # Variável usada na ordenação de resultados
    
    for i in parties:
        aux_check_arg(i,str)                            # Verificação dos argumentos referentes ao partido
        count = 0
        seats = 0
        c = 0
        for r in circles:                               # A avaliação dos quocientes e dos votos é feita circulo a circulo
            if type(dep[c]) != int or dep[c] <= 0: raise ValueError('obtem_resultado_eleicoes: argumento invalido')
            aux_check_arg(r,dict)
            if type(r.get(i)) == int:
                aux_check_arg(r.get(i),int)             # Um partido constante na lista não pode ter 0 votos
            seats += (atribui_mandatos(r,dep[c])).count(i)
            c += 1
            if r.get(i) != None:                        # Evita TypeError exceptions caso o partido não exista no circulo a availar
                count += int(r.get(i))
        aux_check_arg(count,int)                        # Um circulo não pode ter tido 0 votos
        results.append((i,seats,count))
    
    while par < (len(results) - 1):                     # Ordena os túplos do resultado, comparando pares iterativamente
        if (results[par])[1] == (results[par + 1])[1]:  # Caso haja empates de deputados
            if (aux_sorter(results, par, 2))[1] == 1:   # Evita um loop infinito graças à condição failsafe da função
                break
            results = aux_sorter(results, par, 2)[0]
        elif (results[par])[1] > (results[par + 1])[1]: # Caso o par comparado esteja devidamente ordenado
            par +=1                                     # compara-se o par seguinte
        else:
            if (aux_sorter(results, par, 1))[1] == 1:
                break
            results = aux_sorter(results, par, 1)[0]    # Caso o par comparado esteja desordenado
            par = 0                                     # Salvaguarda contra ignorar comparações de nº de votos
    return results

####################################
#3. Solução de Sistemas de Equações#
####################################

def produto_interno(left,right):
    """Recebe dois tuplos de igual tamanho constituido por inteiros ou reais e
    representando e vetores; devolve o produto interno desses vetores"""
    res = 0
    for i, n  in zip(left, right):
    ### DUVIDA: TORNAR VERIFICAÇÃO MAIS COMPACTA??###
        if (type(i) not in [int, float]) or (type(n) not in [int, float]):
            raise ValueError
        res += i*n
    return res

def verifica_convergencia(matrix,const,sol,per):
    """Recebe uma matriz na forma de um tuplo contendo tuplos, um tuplo de constantes,
    um tuplo de soluções e um numero real correspondente à percisão pretendida"""
    for line, c in zip(matrix, const): 
        if abs(produto_interno(line,sol) - c) >= per: return False
    return True

print(verifica_convergencia(
            ((1, -0.5), (-1, 2)), (-0.4, 1.9), (0.1001, 1), 0.001))