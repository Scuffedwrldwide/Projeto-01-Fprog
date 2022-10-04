#1. Justificação de Texto

from calendar import c


def limpa_texto(cad):
    """Recebe cadeia de caracteres (cad) e devolve uma cadeia correspondente à
    remoção de caracteres ASCII brancos, substituidos pelo espaço (0x20)"""
    cad = cad.strip(' ')               #Remove espaços a cada lado do input
    cad = cad.replace('\t',' ')        #Devolve a cadeia fornecida trocando os caracteres definidos  pelo espaço ' '
    cad = cad.replace('\n',' ')
    cad = cad.replace('\v',' ')
    cad = cad.replace('\f',' ')
    cad = cad.replace('\r',' ')
    while int(cad.find('  ')) > 0:
        cad = cad.replace('  ',' ')    #Enquanto existirem sequencias de 2 ou mais espaços, substitui as sequências de 2 espaços por 1
    return cad.strip(' ') 

def corta_texto(cad,col):
    cut = cad
    uncut = ''
    if len(cad) > col:
        cut = cad[:col]  
        cut = cut[:cut.rfind(' ')].strip(' ')    #Limita a cadeia cortada até ao ultimo espaço eliminando palavras incompletas
        uncut = cad[len(cut):].strip(' ')        #A restante cadeia resume a após o ultimo caractér presente na cadeia cortada
    return cut, uncut      
def finaliza_espaços(cad ,col):
    """Adiciona espaços ao final de uma cadeia de caracteres"""
    while len(cad) < col:
            cad += (' ')
    return cad

def insere_espacos(cad, col):
    """Recebe cadeia de caracteres e um inteiro correspondente à largura da coluna"""
    if cad.find(' ') == False:                                 #Não encontrar espaços implica a existência de uma só palavra 
        finaliza_espaços(cad ,col)
    else:
        count = 1                                              # Número inicial de espaços
        while len(cad) <= col:
            cad = cad.replace(' '*count, ' '*(count+1))        #Aumenta ambas as instâncias de espaços
            count +=1                                          #Atualiza a dimensão atual das sequências de espaços
        while len(cad) > col:
            cad = cad.replace(' '*count, ' '*(count-1))        #Reduz todas as sequências em um espaço
            cad = cad.replace(' '*(count-1), ' '*(count), col-len(cad))   #permitindo que se aumente cada uma das sequencias por 1 espaço   
    return cad

def justifica_texto(cad, col):
    if type(cad) != str or type(col) != int or (cad.find(' ') == False and len(cad) > col):
        raise ValueError('argumentos invalidos')
    else:
        lines = len(cad)//col           #Prevê o número de linhas necessárias para a justificação
        next = limpa_texto(cad)         #Variavel que guarda o texto restante
        cad = []
        for i in range(lines-1):   
            cad = cad + [str(insere_espacos(corta_texto(next,col)[0], col))]
            next = str(corta_texto(next,col)[1])
            lines -= 1
        cad = cad + [finaliza_espaços(next,col)]                              
        return tuple(cad)

cad = ('Computers are incredibly  \n\tfast,     \n\t\taccurate'
            ' \n\t\t\tand  stupid.   \n    Human beings are incredibly  slow  '
            'inaccurate, and brilliant. \n     Together  they  are powerful   ' 
            'beyond imagination.')

print(justifica_texto(cad, 60))