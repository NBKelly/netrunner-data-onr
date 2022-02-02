import fileinput
import string
import ast
import re
import functools
import os

import sys

subtypes = {}
card_num = 0

#dict of card id : artist, link to art
art = {}

def to_file_name(title):
    return "onr_out/cards/" + strip_str(title_to_id(title)) + ".edn"

def strip_str(str):
    return normalize(str.replace("\r", "").replace("\t", ""))

def strength(str):
    if str == "*" or str == "x" or str == "X":
        return "0"
    return str

def normalize(str):
    str = str.replace("ä", "a")
    str = str.replace("è", "e")
    str = str.replace("é", "e")
    str = str.replace("π", "pi")
    str = str.replace("\317\200", "pi")
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

def escape_title(str):
    str = str.replace("\"", "\\\"")
    return str

def escape_lines(str):
    str = str.replace("\n", "\\n")
    return strip_str(str)

def strip_title(str):
    str = re.sub(r'[^\w\s]','',str)
    return str

def quote(str):
    return '"' + str + '"'

def pre_title(str):
    return "ONR " + str

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
    output += "\n :agenda-points " + str(card["agendapoints"])
    output += "\n :deck-limit 99"
    output += "\n :faction :onr-corp"
    output += "\n :id " + quote(title_to_id(str(card["title"])))
    output += "\n :side :corp"

    ## check for subtypes
    if "subtypes" in card:
        output += "\n :subtype " + process_subtypes(card["subtypes"])
    
    output += "\n :stripped-text " + quote(strip_text(replace_credits(card["text"])))
    output += "\n :stripped-title " + quote(pre_title(strip_title(card["title"])))
    output += "\n :text " + quote(escape_lines(replace_credits(card["text"])))
    output += "\n :title " + quote(pre_title(card["title"]))
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
    output += "\n :stripped-title " + quote(pre_title(strip_title(card["title"])))
 
    ## check for subtypes                                                                            
    if "subtypes" in card:
        output += "\n :subtype " + process_subtypes(card["subtypes"])
        
    output += "\n :text " + quote(escape_lines(replace_credits(card["text"])))
    output += "\n :title " + quote(pre_title(card["title"]))
    output += "\n :trash-cost " + str(card["trashcost"])
    output += "\n :type :asset"
    if "subtypes" in card and re.match("Unique", card["subtypes"]):
        output += "\n :uniqueness true}"
    else:
        output += "\n :uniqueness false}"        

    write_file(str(card["title"]), output)            

def convert_upgrade(card):
    ## ANR Upgrade:
    ## {:cost 1
    ##  :deck-limit 3
    ##  :faction :haas-bioroid
    ##  :id "jinja-city-grid"
    ##  :influence-cost 2
    ##  :side :corp
    ##  :stripped-text "Whenever you draw a piece of ice, you may reveal it and install it protecting this server, paying 4 credits less. Limit 1 region per server."
    ##  :stripped-title "Jinja City Grid"
    ##  :subtype [:region]
    ##  :text "Whenever you draw a piece of ice, you may reveal it and install it protecting this server, paying 4[credit] less.\nLimit 1 <strong>region</strong> per server."
    ##  :title "Jinja City Grid"
    ##  :trash-cost 5
    ##  :type :upgrade
    ##  :uniqueness false}

    output = "{:cost " + card["cost"]
    output += "\n :deck-limit 99"
    output += "\n :faction :onr-corp"
    output += "\n :id " + quote(title_to_id(card["title"]))
    output += "\n :influence-cost 1"
    output += "\n :side :corp"
    output += "\n :stripped-text " + quote(strip_text(replace_credits(str(card["text"]))))
    output += "\n :stripped-title " + quote(pre_title(strip_title(card["title"])))
 
    ## check for subtypes                                                                            
    if "subtypes" in card:
        output += "\n :subtype " + process_subtypes(card["subtypes"])
        
    output += "\n :text " + quote(escape_lines(replace_credits(card["text"])))
    output += "\n :title " + quote(pre_title(card["title"]))
    if "trashcost" in card:
        output += "\n :trash-cost " + str(card["trashcost"])
    output += "\n :type :upgrade"
    if "subtypes" in card and re.match("Unique", card["subtypes"]):
        output += "\n :uniqueness true}"
    else:
        output += "\n :uniqueness false}"        

    write_file(str(card["title"]), output)            

    
## note: ANR event = ONR prep
def convert_event(card):
    ## ANR Event
    ##  {:cost 5
    ##   :deck-limit 3
    ##   :faction :neutral-runner
    ##   :id "sure-gamble"
    ##   :influence-cost 0
    ##   :side :runner
    ##   :stripped-text "Gain 9 credits."
    ##   :stripped-title "Sure Gamble"
    ##   :text "Gain 9[credit]."
    ##   :title "Sure Gamble"
    ##   :type :event
    ##    :uniqueness false}
    output = "{:cost " + card["cost"]
    output += "\n :deck-limit 99"
    output += "\n :faction :onr-runner"
    output += "\n :id " + quote(title_to_id(card["title"]))
    output += "\n :influence-cost 1"
    output += "\n :side :runner"
    output += "\n :stripped-text " + quote(strip_text(replace_credits(card["text"])))
    output += "\n :stripped-title " + quote(pre_title(strip_title(card["title"])))
    ## check for subtypes                                                                            
    if "subtypes" in card:
        output += "\n :subtype " + process_subtypes(card["subtypes"])        
    output += "\n :text " + quote(escape_lines(replace_credits(card["text"])))
    output += "\n :title " + quote(pre_title(card["title"]))
    output += "\n :type :event"
    output += "\n :uniqueness false}"        
    #write to file
    write_file(str(card["title"]), output)

def convert_resource(card):
    ##{:cost 2
    ## :deck-limit 3
    ## :faction :neutral-runner
    ## :id "kati-jones"
    ## :influence-cost 0
    ## :side :runner
    ## :stripped-text "blah."
    ## :stripped-title "Kati Jones"
    ## :subtype [:connection]
    ## :text "blah."
    ## :title "Kati Jones"
    ## :type :resource
    ## :uniqueness true}
    output = "{:cost " + card["cost"]
    output += "\n :deck-limit 99"
    output += "\n :faction :onr-runner"
    output += "\n :id " + quote(title_to_id(card["title"]))
    output += "\n :influence-cost 1"
    output += "\n :side :runner"
    output += "\n :stripped-text " + quote(strip_text(replace_credits(str(card["text"]))))
    output += "\n :stripped-title " + quote(pre_title(strip_title(card["title"])))
 
    ## check for subtypes                                                                            
    if "subtypes" in card:
        output += "\n :subtype " + process_subtypes(card["subtypes"])
        
    output += "\n :text " + quote(escape_lines(replace_credits(card["text"])))
    output += "\n :title " + quote(pre_title(card["title"]))
    output += "\n :type :resource"
    if "subtypes" in card and re.match("Unique", card["subtypes"]):
        output += "\n :uniqueness true}"
    else:
        output += "\n :uniqueness false}"        

    write_file(str(card["title"]), output)            

def convert_hardware(card):
    ## {:cost 1
    ##  :deck-limit 3
    ##  :faction :shaper
    ##  :id "akamatsu-mem-chip"
    ##  :influence-cost 1
    ##  :side :runner
    ##  :stripped-text "+1 mu"
    ##  :stripped-title "Akamatsu Mem Chip"
    ##  :subtype [:chip]
    ##  :text "+1[mu]"
    ##  :title "Akamatsu Mem Chip"
    ##  :type :hardware
    ##  :uniqueness false}
    output = "{:cost " + card["cost"]
    output += "\n :deck-limit 99"
    output += "\n :faction :onr-runner"
    output += "\n :id " + quote(title_to_id(card["title"]))
    output += "\n :influence-cost 1"
    output += "\n :side :runner"
    output += "\n :stripped-text " + quote(strip_text(replace_credits(str(card["text"]))))
    output += "\n :stripped-title " + quote(pre_title(strip_title(card["title"])))
 
    ## check for subtypes                                                                            
    if "subtypes" in card:
        output += "\n :subtype " + process_subtypes(card["subtypes"])
        
    output += "\n :text " + quote(escape_lines(replace_credits(card["text"])))
    output += "\n :title " + quote(pre_title(escape_title(card["title"])))
    output += "\n :type :hardware"
    if "subtypes" in card and re.match("Unique", card["subtypes"]):
        output += "\n :uniqueness true}"
    else:
        output += "\n :uniqueness false}"        

    write_file(str(card["title"]), output)

def convert_program(card):
    ## {:cost 5
    ##  :deck-limit 3
    ##  :faction :shaper
    ##  :id "adept"
    ##  :influence-cost 3
    ##  :memory-cost 2
    ##  :side :runner
    ##  :strength 2
    ##  :stripped-text "This program gets +1 strength for each unused MU. Interface -> 2 credits: Break 1 sentry or barrier subroutine."
    ##  :stripped-title "Adept"
    ##  :subtype [:icebreaker :fracter :killer]
    ##  :text "This program gets +1 strength for each unused MU.\nInterface → <strong>2[credit]:</strong> Break 1 <strong>sentry</strong> or <strong>barrier</strong> subroutine."
    ##  :title "Adept"
    ##  :type :program
    ##  :uniqueness false}
    output = "{:cost " + card["cost"]
    output += "\n :deck-limit 99"
    output += "\n :faction :onr-runner"
    output += "\n :id " + quote(title_to_id(card["title"]))
    output += "\n :influence-cost 1"

    if "memory" in card:
        output += "\n :memory-cost " + str(card["memory"])
    
    output += "\n :side :runner"

    if "strength" in card:
        output += "\n :strength " + strength(str(card["strength"]))
        
    output += "\n :stripped-text " + quote(strip_text(replace_credits(str(card["text"]))))
    output += "\n :stripped-title " + quote(pre_title(strip_title(card["title"])))
 
    ## check for subtypes                                                                            
    if "subtypes" in card:
        output += "\n :subtype " + process_subtypes(card["subtypes"])
        
    output += "\n :text " + quote(escape_lines(replace_credits(card["text"])))
    output += "\n :title " + quote(pre_title(escape_title(card["title"])))
    output += "\n :type :program"
    if "subtypes" in card and re.match("Unique", card["subtypes"]):
        output += "\n :uniqueness true}"
    else:
        output += "\n :uniqueness false}"        

    write_file(str(card["title"]), output)
    
def convert_ice(card):
    ## {:cost 1
    ##  :deck-limit 3
    ##   :faction :weyland-consortium
    ##   :id "ice-wall"
    ##   :influence-cost 1
    ##   :side :corp
    ##   :strength 1
    ##   :stripped-text "You can advance this ice. It gets +1 strength for each hosted advancement counter. Subroutine End the run."
    ##   :stripped-title "Ice Wall"
    ##   :subtype [:barrier]
    ##   :text "You can advance this ice. It gets +1 strength for each hosted advancement counter.\n[subroutine] End the run."
    ##   :title "Ice Wall"
    ##   :type :ice
    ##   :uniqueness false}

    output = "{:cost " + card["cost"]
    output += "\n :deck-limit 99"
    output += "\n :faction :onr-corp"
    output += "\n :id " + quote(title_to_id(card["title"]))
    output += "\n :influence-cost 1"
    output += "\n :side :corp"
    output += "\n :strength " + strength(str(card["strength"]))
    output += "\n :stripped-text " + quote(strip_text(replace_credits(str(card["text"]))))
    output += "\n :stripped-title " + quote(pre_title(strip_title(card["title"])))
    ## check for subtypes                                                                            
    if "subtypes" in card:
        output += "\n :subtype " + process_subtypes(card["subtypes"])        
    output += "\n :text " + quote(escape_lines(replace_credits(card["text"])))
    output += "\n :title " + quote(pre_title(card["title"]))
    output += "\n :type :ice"
    if "subtypes" in card and re.match("Unique", card["subtypes"]):
        output += "\n :uniqueness true}"
    else:
        output += "\n :uniqueness false}"        

    #write to file
    write_file(str(card["title"]), output)
    
def convert_operation(card):
    ## ANR Operation
    ##  {:cost 5
    ##   :deck-limit 3
    ##   :faction :neutral-corp
    ##   :id "hedge-fund"
    ##   :influence-cost 0
    ##   :side :corp
    ##   :stripped-text "Gain 9 credits."
    ##   :stripped-title "Hedge Fund"
    ##   :subtype [:transaction]
    ##   :text "Gain 9[credit]."
    ##   :title "Hedge Fund"
    ##   :type :operation
    ##   :uniqueness false}
    output = "{:cost " + card["cost"]
    output += "\n :deck-limit 99"
    output += "\n :faction :onr-corp"
    output += "\n :id " + quote(title_to_id(card["title"]))
    output += "\n :influence-cost 1"
    output += "\n :side :corp"
    output += "\n :stripped-text " + quote(strip_text(replace_credits(str(card["text"]))))
    output += "\n :stripped-title " + quote(pre_title(strip_title(card["title"])))
    ## check for subtypes                                                                            
    if "subtypes" in card:
        output += "\n :subtype " + process_subtypes(card["subtypes"])        
    output += "\n :text " + quote(escape_lines(replace_credits(card["text"])))
    output += "\n :title " + quote(pre_title(card["title"]))
    output += "\n :type :operation"
    output += "\n :uniqueness false}"        
    #write to file
    write_file(str(card["title"]), output)
    
def convert(card):
    if card['type'] == 'Agenda':
        convert_agenda(card)
    if card['type'] == 'Node':
        convert_asset(card)
    if card['type'] == 'Operation':
        convert_operation(card)
    if card['type'] == 'Ice':
        convert_ice(card)
    if card['type'] == 'Upgrade':
        convert_upgrade(card)
    if card['type'] == 'Prep':
        convert_event(card)
    if card['type'] == 'Resource':
        convert_resource(card)
    if card['type'] == 'Hardware':
        convert_hardware(card)
    if card['type'] == 'Program':
        convert_program(card)

    #dict of card id : artist, link to art
    #art = {}
    #get id of card
    _dict_key = title_to_id(card["title"])
    #get artist
    _dict_artist = card["artist"]
    #get link
    _dict_image = card["image"]
    art[_dict_key] = [_dict_artist, _dict_image]
    


## convert every input card
for line in fileinput.input():
    card = ast.literal_eval(line.replace("\r", ""))
    convert(card)

## print all art information to a seperate file
filename = "onr_out/art_inter.txt"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as f:
    f.write(str(art))

## print out all the subtypes that have been gathered
for key in subtypes:
#    print(key)
    print(subtypes[key])
    
