import sys
import copy

ifile = sys.argv[1]
gofile = 'ATH_GO_GOSLIM.txt'

goi = []

with open(ifile) as infile:
    for lines in infile:
        lines = lines.rstrip()
        goi.append(lines)
        
goont = {}
allnames = {}

with open('go.obo') as infile:
    for lines in infile:
        lines = lines.rstrip()
        if lines.startswith('id'):
            curid = lines.split(' ')[-1]
        if lines.startswith('name:'):
            curname = lines.split('name: ')[1]
            allnames[curid] = curname
        if lines.startswith('is_a'):
            curis = lines.split(' ')[1]
            if curid in goont:
                goont[curid].add(curis)
            else:
                goont[curid] = {curis}
        if ('GO:' in lines) and ('!' in lines):
            if ('relationship' in lines) or ('is_a' in lines) or ('part_of' in lines):
                goterms = lines.split('GO:')
                for g in goterms[1:]:
                    curis = 'GO:' + g.split(' ')[0]
                    if curid in goont:
                        goont[curid].add(curis)
                    else:
                        goont[curid] = {curis}
                
                
formgoont = set()

while (goont != formgoont):
    formgoont = copy.deepcopy(goont)
    for g in list(goont):
        for g2 in list(goont[g]):
            if g2 in goont:
                goont[g].update(goont[g2])

goteez = {}


with open(gofile) as infile:
    for lines in infile:
        if lines.startswith('!'):
            continue
        lines = lines.rstrip()
        values = lines.split('\t')
        genename = values[0]
        godesc = values[4]
        goid = values[5]
        gotype = values[7]
        if goid not in goteez:
            goteez[goid] = [godesc,gotype,{genename}]
        else:
            goteez[goid][2].add(genename)
        if goid in goont:
            for othergos in goont[goid]:
                if othergos not in goteez:
                    goteez[othergos] = [allnames[othergos],gotype,{genename}]
                else:
                    goteez[othergos][2].add(genename)
            
    
print('GO ID\tGO Description\tGO Type\tGenes in Module Annotated to GO Term')

for g in goteez:
    genez = []
    genelist = list(set(goteez[g][2]))
    for g2 in goi:
        if g2 in genelist:
            genez.append(g2)
    if (len(genez) < 1):
        continue
    else:
        print(g + '\t' + goteez[g][0]  + '\t' + goteez[g][1] + '\t' + '|'.join(genez))
