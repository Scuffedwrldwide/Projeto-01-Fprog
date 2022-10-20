##########################
#1. Justificação de Texto#
##########################

def limpa_texto(cad):
    """Recebe cadeia de caracteres (cad) e devolve uma cadeia correspondente à
    remoção de caracteres ASCII brancos, substituidos pelo espaço (0x20)
    eliminando ainda sequências contínuas de espaços"""
    cad = cad.strip(' ')                # Remove espaços a cada lado do input
    toreplace = {0x09 : ' ',            # Devolve a cadeia fornecida trocando os caracteres definidos  pelo espaço ' '
                0x0a : ' ', 
                0x0b : ' ',
                0x0c : ' ',
                0x0d : ' ',
                }            
    cad = cad.translate(toreplace)
    while int(cad.find('  ')) >= 0:
        cad = cad.replace('  ',' ')     # Enquanto existirem sequencias de 2 ou mais espaços, substitui as sequências de 2 espaços por 1
    return cad.strip(' ') 

def corta_texto(cad, col):
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
            count += 1                                         # Atualiza a dimensão atual das sequências de espaços
        while len(cad) > col:
            cad = cad.replace(' '*count, ' '*(count-1))                   # Reduz todas as sequências em um espaço
            cad = cad.replace(' '*(count-1), ' '*(count), col-len(cad))   # permitindo que se aumente cada uma das sequencias por 1 espaço   
    return cad                                                            # da esquerda para a direita

def justifica_texto(cad, col):
    """Recebe cadeia de caracteres e um inteiro correspondente à largura da coluna.
    Aceita tuplos."""
    if type(cad) != str or type(col) != int or col < 1 or ((not col >= cad.find(' ') > -1) and len(cad)>col) or len(cad) == 0:
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
        
        if len(next) >= col:                                                   # Caso a ultíma linha exceda o comprimento pedido
            cad.append(str(insere_espacos(corta_texto(next,col)[0], col)))     
            next = str(corta_texto(next,col)[1])    
        
        cad.append(next.ljust(col,' '))                                        # A ultima porção de cada texto é unicamente justificada à esquerda
        return tuple(cad)

####################
#2. Método de Hondt#
####################

def aux_check_arg(arg,typ):
    """Recebe um argumento de qualquer tipo, bem como o tipo (type) experado,
    efetua a verificação de argumentos, não retornando qualquer valor"""
    if (type(arg) == dict and arg == {}) or (type(arg) == list and arg == ()) or (type(arg) == int and arg < 0) or (type(arg) == tuple and arg ==()):
        raise ValueError('obtem_resultado_eleicoes: argumento invalido')
    if type(arg) != typ:
        raise ValueError('obtem_resultado_eleicoes: argumento invalido')

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

def aux_sorter(
    lst, par, index):
    """Compara e ordena arrays de uma lista com base num critério presente num dado index """
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
            if not isinstance(votes[parties[i]], int): raise ValueError('obtem_resultado_eleicoes: argumento invalido')    
            quo.append(votes[parties[i]]/d)  # Adiciona o quociente dos votos do partido a ser trabalhado ao fim da lista
        results.update({parties[i]: quo})    # Atualiza a entrada do respetivo partido com os resultados apurados
    return results

def atribui_mandatos(votes, seats):
    """Aceita um dicionário partidos:n. de votos e um inteiro e devolve uma lista
    contendo a lista ordenada dos partidos que obtiveram deputados,
    por ordem de obtenção"""
    if not isinstance(seats, int) or seats <= 0: raise ValueError('obtem_resultado_eleicoes: argumento invalido')
    quo = calcula_quocientes(votes, seats)      # necessária para garantir a correta atribuição em caso de empate
    parties = []
    for i in aux_sorter([(p,v) for p,v in votes.items()],1,1)[0]:
        if not isinstance(i[1],int) or i[1] <= 0: raise ValueError('obtem_resultado_eleicoes: argumento invalido')
        parties.insert(0, i[0])                 # Ordem crescente por votos de uma lista de tuplos partido:votos
    results = list(quo.values())                   
    place = list()
    for i in quo:
        results.extend(results[0])              # adiciona à lista 'results' os valores obtidos pelo método de hondt
        results.pop(0)
    results.sort(reverse = True)                  # Ordena a lista por ordem decrescente de quocientes
    for i in range(0, len(results)):            # Compara cada quociente da lista 'results'
        for p in range(0, len(parties)):        # aos quocientes de cada partido segundo a lista 'quo'
            if results[i] in quo.get(parties[p]):
                place.append(parties[p])        # Adiciona os partidos à lista place por ordem de eleição de deputados
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

    if not isinstance(info, dict) or info == {}: raise ValueError('obtem_resultado_eleicoes: argumento invalido')
    parties = obtem_partidos(info)                      # Lista alfabética dos partidos
    if not isinstance(parties, list) or parties == []: raise ValueError('obtem_resultado_eleicoes: argumento invalido')
    circles = aux_obtem_partido_votos(info)             # Lista dos vários resultados por circulo
    if not isinstance(circles, list) or circles == []: raise ValueError('obtem_resultado_eleicoes: argumento invalido')
    dep = aux_obtem_partido_votos(info, 1)              # Lista correspondente aos deputados por circulo
    if not isinstance(dep, list) or dep == []: raise ValueError('obtem_resultado_eleicoes: argumento invalido')
    seats = 0
    results = []
    par = 0                                             # Variável usada na ordenação de resultados
    
    for p in parties:
        if not isinstance(p, str) or p == '': raise ValueError('obtem_resultado_eleicoes: argumento invalido') # Verificação dos argumentos referentes ao partido
        count = 0
        seats = 0
        c = 0
        for r in circles:                               # A avaliação dos quocientes e dos votos é feita circulo a circulo
            if (not isinstance(r, dict)) or r == {} or type(dep[c]) != int or dep[c] <= 0 or (isinstance(r.get(p), int) and r.get(p) <= 0): 
                raise ValueError('obtem_resultado_eleicoes: argumento invalido') # Um partido constante na lista não pode ter 0 votos
            seats += (atribui_mandatos(r,dep[c])).count(p)
            c += 1
            if r.get(p) is not None:                    # Evita TypeError exceptions caso o partido não exista no circulo a availar
                count += int(r.get(p))
        if count <= 0: raise ValueError('obtem_resultado_eleicoes: argumento invalido') # Um circulo não pode ter tido 0 votos
        results.append((p,seats,count))
    
    while par < (len(results) - 1):                     # Ordena os túplos do resultado, comparando pares iterativamente
        if (results[par])[1] == (results[par + 1])[1]:  # Caso haja empates de deputados
            if (aux_sorter(results, par, 2))[1] == 1:   # Evita um loop infinito graças à condição failsafe da função
                break
            results = aux_sorter(results, par, 2)[0]
        elif (results[par])[1] > (results[par + 1])[1]: # Caso o par comparado esteja devidamente ordenado
            par += 1                                    # compara-se o par seguinte
        else:
            if (aux_sorter(results, par, 1))[1] == 1:
                break
            results = aux_sorter(results, par, 1)[0]    # Caso o par comparado esteja desordenado
            par = 0                                     # Salvaguarda contra ignorar comparações de nº de votos
    return results

####################################
#3. Solução de Sistemas de Equações#
####################################

def aux_abssum_array(arg):
    """Retorna a soma dos valores absolutos de uma lista ou tuplo"""
    sum = 0
    for i in arg: 
        if type(i) in [float, int]:
            sum += abs(i)
    return sum

def produto_interno(left,right):
    """Recebe dois tuplos de igual tamanho constituido por inteiros ou reais e
    representando e vetores; devolve um valor float correspondente 
    ao produto interno desses vetores"""
    res = 0
    if len(left) != len(right): raise ValueError('resolve_sistema: argumentos invalidos')
    for i, n  in zip(left, right):
    ### DUVIDA: TORNAR VERIFICAÇÃO MAIS COMPACTA??###
        if (type(i) not in [int, float]) or (type(n) not in [int, float]):
            raise ValueError('resolve_sistema: argumentos invalidos')
        res += i*n
    return float(res)

def verifica_convergencia(
        matrix, const, sol, 
        acc):
    """Recebe uma matriz na forma de um tuplo contendo tuplos, um tuplo de constantes,
    um tuplo de soluções e um numero real correspondente à percisão pretendida"""
    for line, c in zip(matrix, const): 
        if abs(produto_interno(line,sol) - c) >= acc: return False
    return True

def retira_zeros_diagonal(matrix, const):
    """Recebe um tuplo de tuplos representando as linhas de uma matriz, e um tuplo
    de constantes"""
    matrix, const = list(matrix), list(const)

    for l in range(0, len(matrix)):
            for n in range(0, len(matrix)):
                if not isinstance(matrix[l], tuple) or matrix[l] == (): raise ValueError('resolve_sistema: argumentos invalidos')
                if not type(matrix[l][l]) in [int, float]: raise ValueError('resolve_sistema: argumentos invalidos')
                if  matrix[l][l] == 0 and matrix[n][l] != 0 and matrix[l][n] != 0:
                    matrix[l], matrix[n] = matrix[n], matrix[l]
                    const[l], const[n] = const[n], const[l]
                    break
    return tuple(matrix), tuple(const)
   
def eh_diagonal_dominante(matrix):
    """Recebe um tuplo de tuplos correspondente a uma matriz, verifica que o módulo do valor
    constante na diagonal é superior à soma dos módulos dos restantes """
    for line in matrix:
        #for i in line:
            #if not type(i) in [int, float]: raise ValueError('resolve_sistema: argumentos invalidos')

        if abs(line[matrix.index(line)]) < aux_abssum_array(line) - abs(line[matrix.index(line)]):
            return False
    return True

def resolve_sistema(
        matrix, const, 
        acc):
    """Recebe um tuplo constituido por tuplos de números representando uma matriz, 
    um tuplo de constantes (float ou int) e uma constante correspondente à percisão"""

    if type(acc) not in [int, float] or acc <= 0: raise ValueError('resolve_sistema: argumentos invalidos')
    if not isinstance(const, tuple) or not len(const) >= 1: raise ValueError('resolve_sistema: argumentos invalidos') 
    if not isinstance(matrix, tuple) or not len(matrix) >= 1: raise ValueError('resolve_sistema: argumentos invalidos') 
    
    matrix, const = retira_zeros_diagonal(matrix, const)
    sol = [0 for i in range(len(const))]
    #k = 0       # Contador de iterações

    if not eh_diagonal_dominante(matrix):
        raise ValueError('resolve_sistema: matriz nao diagonal dominante')
    while verifica_convergencia(matrix,const,sol,acc) != True:
        for i in range(0, len(sol)):
            if len(matrix) != len(const) or len(const) == 0: raise ValueError('resolve_sistema: argumentos invalidos')
            if len(matrix[i]) != len(matrix[0]) or len(matrix[i]) != len(const) or len(matrix[i]) != len(matrix):
                raise ValueError('resolve_sistema: argumentos invalidos')
            if type(const[i]) not in [int, float]: raise ValueError('resolve_sistema: argumentos invalidos')
            #sol[i] = sol[i]*k
            sol[i] = (sol[i]) + (const[i]-produto_interno(matrix[i], sol))/matrix[i][i]
            #k += 1
    return tuple(sol)
