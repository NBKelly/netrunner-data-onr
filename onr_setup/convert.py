import fileinput
import string
import ast
import re
import functools
import os

subtypes = {}
card_num = 0

def to_file_name(title):
    return "onr_out/cards/" + title_to_id(title) + ".edn"

def strip_str(str):
    return normalize(str.replace("\r", "").replace("\t", ""))

def normalize(str):
    str = str.replace("ä", "a")
    str = str.replace("\"", "\\\"")
    return str

def title_to_id(str):
    str = normalize(re.sub(r'[^\w\s]','',str))
    return "onr-" + str.lower().replace(" ", "-")

def replace_credits(str):
    str = re.sub("\[", "", str)
    str = re.sub("\]", " [credit]", str)
    return str

def strip_text(str):
    str = re.sub("\[|\]", "", str)    
    str = str.replace("\n", " ")
    return strip_str(str)

def escape_lines(str):
    str = str.replace("\n", "\\n")
    return strip_str(str)

def strip_title(str):
    str = re.sub(r'[^\w\s]','',str)
    return str

def quote(str):
    return '"' + str + '"'

def process_subtype(str):
    #{:id :advertisement
    # :name "Advertisement"}
    subtype_title = ":" + title_to_id(str)
    if subtype_title in subtypes:
        return subtype_title

    st = "{:id " + subtype_title + "\n :name " + quote(str) + "}"
    
    subtypes[subtype_title] = st
    return subtype_title

#converts a set of subtypes like Asset - Ambush to a
#set of processed subtypes like [:asset :ambush]
#also creates associations in subtypes dictionary if none already exist
def process_subtypes(str):
    split = str.split(" - ")
    split = list(map(process_subtype, split))
    res = "[" + functools.reduce(lambda a, b: a + " " + b, split, "")[1:] + "]"
    return res    

def write_file(title, card):
    filename = to_file_name(title)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(card)

def convert_agenda(card):
    ## ONR AGENDA:
    ##  title, image, side, type, subtypes,
    ##  set, rarity, difficulty, agendapoints, text
    ##
    ## ANR AGENDA:
    ##  {:advancement-requirement x
    ##   :agenda-points x
    ##   :deck-limit x (use 99 for ONR cards?)
    ##   :faction :onr-corp
    ##   :id "title-id"
    ##   :side :corp
    ##   :stripped-text "blah blah blah"
    ##   :stripped-title "title"
    ##   :text "blah"
    ##   :title "blah"
    ##   :type :agenda
    ##   :uniqueness false}
    output = "{:advancement-requirement " + str(card["difficulty"])
    output += "\n :agenda-points " + str(card["difficulty"])
    output += "\n :deck-limit 99"
    output += "\n :faction :onr-corp"
    output += "\n :id " + quote(title_to_id(str(card["title"])))
    output += "\n :side :corp"

    ## check for subtypes
    if "subtypes" in card:
        output += "\n :subtype " + process_subtypes(card["subtypes"])
    
    output += "\n :stripped-text " + quote(strip_text(replace_credits(str(card["text"]))))
    output += "\n :stripped-title " + quote(strip_title(card["title"]))
    output += "\n :text " + quote(escape_lines(replace_credits(card["text"])))
    output += "\n :title " + quote(card["title"])
    output += "\n :type :agenda"
    output += "\n :uniqueness false}"
    output += "\n"

    write_file(str(card["title"]), output)            

#note: ANR asset = ONR node
def convert_asset(card):
    ## ANR Asset:
    ##  {:cost 2
    ##   :deck-limit 3
    ##   :faction :haas-bioroid
    ##   :id "marilyn-campaign"
    ##   :influence-cost 1
    ##   :side :corp     
    ##   :stripped-text "blah"
    ##   :stripped-title "blah"
    ##   :subtype [:advertisement]    
    ##   :title "blah"
    ##   :trash-cost 3
    ##   :type :asset
    ##   :uniqueness false}
    output = "{:cost " + card["cost"]
    output += "\n :deck-limit 99"
    output += "\n :faction :onr-corp"
    output += "\n :id " + quote(title_to_id(card["title"]))
    output += "\n :influence-cost 1"
    output += "\n :side :corp"
    output += "\n :stripped-text " + quote(strip_text(replace_credits(str(card["text"]))))
    output += "\n :stripped-title " + quote(strip_title(card["title"]))

    ## check for subtypes                                                                            
    if "subtypes" in card:
        output += "\n :subtype " + process_subtypes(card["subtypes"])
        
    output += "\n :text " + quote(escape_lines(replace_credits(card["text"])))
    output += "\n :title " + quote(card["title"])
    output += "\n :trash-cost " + str(card["trashcost"])
    output += "\n :type :asset"
    if "subtypes" in card and re.match("Unique", card["subtypes"]):
        output += "\n :uniqueness true}"
    else:
        output += "\n :uniqueness false}"        

    write_file(str(card["title"]), output)            
    
def convert(card):
    if card['type'] == 'Agenda':
        convert_agenda(card)
    if card['type'] == 'Node':
        convert_asset(card)

## convert every input card
for line in fileinput.input():
    card = ast.literal_eval(line.replace("\r", ""))
    convert(card)

## print out all the subtypes that have been gathered
for key in subtypes:
    print(key)
    print(subtypes[key])
    
