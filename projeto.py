#1. Justificação de Texto

def limpa_texto(cad):
    """Recebe cadeia de caracteres (cad) e devolve uma cadeia correspondente à
    remoção de caracteres ASCII brancos, substituidos pelo espaço (0x20)"""
    cad = cad.strip(' ')                #Remove espaços a cada lado do input
    cad = cad.replace('\t',' ')         #Devolve a cadeia fornecida trocando os caracteres definidos  pelo espaço ' '
    cad = cad.replace('\n',' ')
    cad = cad.replace('\v',' ')
    cad = cad.replace('\f',' ')
    cad = cad.replace('\r',' ')
    while int(cad.find('  ')) > 0:
        cad = cad.replace('  ',' ')       #Enquanto existirem sequencias de 2 ou mais espaços, substitui as sequências de 2 espaços por 1
    return cad.strip(' ') 

def corta_texto(cad,col):
    cad[0:col].lstrip().rstrip()
    cad[col]

def insere_espacos(cad, col):
    """Recebe cadeia de caracteres e um inteiro correspondente à largura da coluna"""
    if cad.find(' ') == False:          #Não encontrar espaços implica a existência de uma só palavra 
        while len(cad) < col:
            cad.append(' ')

    else:       
        while len(cad) < col:
            for i in cad.index(' '):    #A cada ocorrência de espaço na string fornecida, inserir um espaço, até alcançar a largura desejada
                cad.insert(' ')

def justifica_texto(cad, col):
    if type(cad) != str or type(col) != int or (cad.find(' ') == False and len(cad) > col):
        raise ValueError('argumentos invalidos')
    else:
        insere_espacos(    insere_espacos(    corta_texto(limpa_texto(cad),col),    col)    ,col)

