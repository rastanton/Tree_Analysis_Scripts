from Bio import Phylo

def Tree_Distance(ID1, ID2, tree_file):
    tree = Phylo.read(tree_file, 'newick')
    Distance = tree.distance(ID1, ID2)
    return Distance

def Tree_Names(input_tree):
    """Extracts a list of tree names"""
    tree = Phylo.read(input_tree, 'newick')
    All = []
    for leaf in tree.get_terminals():
        Name = (leaf.name)
        All.append(Name)
    return All

def Max_Distance(input_tree, basis):
    IDs = Tree_Names(input_tree)
    Max = 0
    Best = basis
    tree = Phylo.read(input_tree, 'newick')
    for ID in IDs:
        Distance = tree.distance(ID, basis)
        if Distance > Max:
            Best = ID
            Max = Distance
    return [Best, Max]

def Matrix_Maker(input_tree, output_matrix):
    tree = Phylo.read(input_tree, 'newick')
    Names = Tree_Names(input_tree)
    Out = open(output_matrix, 'w')
    Name_Line = '\t'.join(Names)
    Out.write('\t' + Name_Line + '\n')
    for entry in Names:
        Line = entry + '\t'
        Distances = []
        for entry2 in Names:
            distance = tree.distance(entry, entry2)
            Distances.append(distance)
        for entry3 in Distance:
            Line += str(entry3) + '\t'
        Out.write(Line[0:-1] + '\n')
    Out.close()

def Min_Distance(input_tree, input_ID):
    IDs = Tree_Names(input_tree)
    Min = 1000
    Best = ''
    tree = Phylo.read(input_tree, 'newick')
    for ID in IDs:
        if ID == input_ID:
            continue
        else:
            Distance = tree.distance(ID, input_ID)
            if Distance < Min:
                Best = ID
                Min = Distance
    return [Best, Min]

                  
