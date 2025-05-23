from Bio import Phylo
import glob
import shutil

def Replace_All(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def Replace_All_File(text_file, dic):
    import fileinput
    for line in fileinput.input(text_file, inplace=True):
        line = Replace_All(line, dic)
        print(line, end="")##This prints each line w/o adding an extra "\n|, keeping original spacing.

def File_Changer(old_name, new_name, dic):
    shutil.copyfile(old_name, new_name)
    Replace_All_File(new_name, dic)

def Dictionary_Maker(input_file):
    d = {}
    with open(input_file) as f:
        for line in f:
            (key, val) = line.split()
            d[key] = val
    return d

def File_Changer_Dic(old_name, new_name, dic_file):
    dic = Dictionary_Maker(dic_file)
    shutil.copyfile(old_name, new_name)
    Replace_All_File(new_name, dic)

def Before_Underscore(input_string):
    Out = ''
    for entry in input_string:
        if entry == '_':
            break
        else:
            Out = Out + entry
    return Out

def Underscore_Remover(input_file, output_file):
    Out = open(output_file, 'w')
    f = open(input_file, 'r')
    for line in f:
        List1 = line.split()
        Out_List = []
        for entry in List1:
            Info = Before_Underscore(entry)
            Out_List.append(Info)
        Out_Line = '\t'.join(Out_List)
        Out.write(Out_Line + '\n')
    Out.close()
    f.close()

def Column_Remover(input_file, output_file, column_index):
    f = open(input_file, 'r')
    Out = open(output_file, 'w')
    for line in f:
        List1 = line.split()
        Out_List = []
        for entry in range(len(List1)):
            if entry != column_index:
                Out_List.append(List1[entry])
        Out_Line = '\t'.join(Out_List)
        Out.write(Out_Line + '\n')
    f.close()
    Out.close()

def Tree_Last_Split(input_tree, output_tree):
    """Renames the leaves of a tree based on the last split()"""
    tree = Phylo.read(input_tree, 'newick')
    for leaf in tree.get_terminals():
        Name = (leaf.name).split()[-1]
        leaf.name = Name
    Out = open(output_tree, 'w')
    Phylo.write(tree, Out, 'newick')
    Out.close()

def Dictionary_Maker_PD(input_PD_file):
    """Makes a dictionary from an input PD file"""
    d = {}
    f = open(input_PD_file, 'r')
    String1 = f.readline()
    List1 = String1.split('\t')
    ID = List1.index('Isolate identifiers')
    Location = List1.index('Location')
    PDID = List1.index('Isolate')
    for line in f:
        List1 = line.split('\t')
        Name = List1[ID].split(',')[0]
        Place = List1[Location]
        if Place == '':
            Place = 'unknown'
        Name = Name + '_' + Place
        (key, val) = [List1[PDID], Name]
        d[key] = val
    return d

def Quote_Remover_Line(input_line):
    """Removes the quotes from a line"""
    Out = ''
    for character in input_line:
        if character != '\"' and character != "\'":
            Out = Out + character
    return Out

def Quote_Remover_File(input_file):
    """Removes the quotes from a file"""
    f = open(input_file, 'r')
    List1 = []
    for line in f:
        List1.append(line)
    f.close()
    Out = open(input_file, 'w')
    for line in List1:
        New = Quote_Remover_Line(line)
        Out.write(New)
    Out.close()

def NCBI_Tree_Renamer(input_tree, output_tree, PD_file):
    """Renames the leaves an NCBI tree using a Pathogen Detection TSV"""
    Tree_Last_Split(input_tree, output_tree)
    mydic = Dictionary_Maker_PD(PD_file)
    Replace_All_File(output_tree, mydic)
    Quote_Remover_File(output_tree)
