def monogram(nev):
    lista = [i for i in nev.split()]
    szo = ""
    for i in lista:
        szo += szo.join(i[0].upper())
    return f'{".".join(szo)}{"."}'
    
print(monogram("Edward Hamilton"))
