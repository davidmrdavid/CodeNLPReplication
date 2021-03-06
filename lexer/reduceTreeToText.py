import csv
import argparse

#Set of tags used in stanford parser, thanks to:
#https://gist.github.com/nlothian/9240750
tag_set = ["ROOT","S", "SBAR", "SBARQ", "SINV", "SQ", "ADJP", "ADVP", "CONJP", "FRAG", "INTJ", "LST", "NAC", "NP", "NX", "PP",
           "PRN", "PRT", "QP", "RRC", "UCP", "VP", "WHADJP", "WHAVP", "WHNP", "WHPP", "X", "CC", "CD", "DT", "EX", "FW", "IN",
           "JJ", "JJR", "JJS", "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "SYM",
           "TO", "UH", "VB", "VBN", "VBD", "VBG", "VBP", "VBZ", "WDT", "WP", "WP$", "WP$", "WRB","ADV", "NOM","DTV", "LGS", "PRD", "PUT",
           "SBJ", "TPC", "VOC","BNF", "DIR","EXT", "LOC","MNR", "PRP", "TMP", "CLR", "SBAR-PRP","CLF", "HLN", "TTL","-LRB", "-RRB",
           "-NONE","*", "0", "T", "NUL", "-NONE-", "-LRB-", "-RRB-", "PRT|ADVP", "ADVP|PRT","#","NN|SYM","VBG|NN","RB|VBG","CD|RB",
           "VBP|TO","PRP|VBP","IN|RP","NN|NNS","JJ|VBG","RB|RP","NN|VBG","JJ|RB","TYPO","NEG","AUX","VBD|VBN","EDITED","WHADVP"]

punct = [",", ".", "\"", ",\"","'",";", ".\"", "-", "?", "--", ":", "!\"", "?\"", "!", "?--", ".--", "!--", "\'" ,"\'\'", "``", "`", "(", ")", "/", "&","<QUOTE>", "<", ">","$", "#"]


def tagJavaElement(item, last_type, last_token, stopwords):
    item = item.strip()
    if(item == "(" or item == ")"):
        return "PAREN"
    elif(last_type == ""):
        return "TAG"
    elif(last_type == "PAREN"):
        return "TAG"
    elif(last_type == "TAG" and last_token.strip() == "#PunctTerminal"):
        return "PUNCT"
    elif(item in stopwords):
        return "STOPWORD"
    else:
        return "WORD"


#Give a parse tree item one of 4 tags:
#PAREN, TAG, WORD, PUNCT
def tagEngElement(item, last,stopwords):
    item = item.strip()
    if(item == "(" or item == ")"):
        return "PAREN"
    elif(item in tag_set):
        if(last == "PAREN"):
            return "TAG"
        elif(item in stopwords):
            return "STOPWORD"
        else:
            return "WORD"
    elif(item in punct):
        if(last == "PAREN"):
            return "TAG"
        else:
            return "PUNCT"
    else:
        if(item in stopwords):
            return "STOPWORD"
        else:
            return "WORD"

#For a given lexed file, create a csv file with the following:
#Header: token, token_type, token_location
#Note: Token_type will be one of 3 things: PAREN, TAG, WORD
# def createMetaDataFile(lexed_tree, metadata_filename,stopwords):
#     i = 0
#     with open(metadata_filename, 'w') as f:
#         f.write("token,token_type,token_location\n")
#         tag = "PAREN" #Always starts with a '(' - though we removed it.
#         for item in lexed_tree.split():
#             tag = tagElement(item, tag,stopwords)
#             f.write(",".join(["\"" + item + "\"", tag, str(i), "\n"]))
#             i += 1

parser = argparse.ArgumentParser(description="Script to pull terminal nodes from a tree")
parser.add_argument("input_file",help = "Location of the file to simplify.", 
                    action="store", type=str)
parser.add_argument("stopword_file", help = "Location of the stopword file.")
parser.add_argument("--java_code", help = "Is this a java ast instead of an "+
                    "english parse tree.", action = "store_true")
parser.add_argument("output_file", help = "Location of the new csv file.",
                    action = "store", type = str)
parser.add_argument("--drop_stopwords", action = "store_true")

args = parser.parse_args()

stopwords = []

with open(args.stopword_file, 'r') as f:
    for line in f:
        stopwords.append(line.lower().strip())

with open(args.input_file, "r") as f:
    with open(args.output_file, 'w') as f2:
        token_type = "" #Nothing to start
        last_token = ""
        for line in f:
            for token in line.split():
                if(args.java_code == False):
                    token_type = tagEngElement(token, token_type, stopwords)
                else:
                    token_type = tagJavaElement(token, token_type, last_token, stopwords)
                last_token = token
                if(args.drop_stopwords):
                    if(token_type == "WORD"):
                        f2.write(" " + token)
                else:
                    if(token_type == "WORD" or token_type == "STOPWORD" or token_type == "PUNCT"):
                        f2.write(" " + token)
                
            f2.write("\n")

