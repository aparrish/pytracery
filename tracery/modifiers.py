def replace(text, *params):
    return text.replace(params[0], params[1])


def capitalizeAll(text, *params):
    return text.title()


def capitalize_(text, *params):
    return text[0].upper() + text[1:]


def a(text, *params):
    if len(text) > 0:
        if text[0] in "uU":
            if len(text) > 2:
                if text[2] in "iI":
                    return "a " + text
        if text[0] in "aeiouAEIOU":
            return "an " + text
    return "a " + text


def firstS(text, *params):
    text2 = text.split(" ")
    return " ".join([s(text2[0])] + text2[1:])


def s(text, *params):
    if text[-1] in "shxSHX":
        return text + "es"
    elif text[-1] in "yY":
        if text[-2] not in "aeiouAEIOU":
            return text[:-1] + "ies"
        else:
            return text + "s"
    else:
        return text + "s"


def ed(text, *params):
    if text[-1] in "eE":
        return text + "d"
    elif text[-1] in "yY":
        if text[-2] not in "aeiouAEIOU":
            return text[:-1] + "ied"
    else:
        return text + "ed"


def uppercase(text, *params):
    return text.upper()


def lowercase(text, *params):
    return text.lower()


base_english = {
    'replace': replace,
    'capitalizeAll': capitalizeAll,
    'capitalize': capitalize_,
    'a': a,
    'firstS': firstS,
    's': s,
    'ed': ed,
    'uppercase': uppercase,
    'lowercase': lowercase
}


#----
#inflect.py modifiers
#Mappings based on https://github.com/pwdyson/inflect.py

import inflect
p = inflect.engine()


def ordinal(text, *params):
    return p.ordinal(text)

def number_to_words(text, *params):
    kwargs=dict(param.split('=') for param in params)
    try:
        resp = p.number_to_words(text, **kwargs)
    except:
        resp = "no recorded"
    return resp
    

def plural(text, *params):
    if params: return p.plural(text, params[0])
    return p.plural(text)

def plural_noun(text, *params):
    if params: return p.plural_noun(text, params[0])
    return p.plural_noun(text)

def plural_verb(text, *params):
    if params: return p.plural_verb(text, params[0])
    return p.plural_verb(text)

def plural_adj(text, *params):
    if len(params): return p.plural_adj(text, params[0])
    return p.plural_adj(text)
    
def singular_noun(text, *params):
    return p.singular_noun(text)
    
def no(text, *params):
    return p.no(text)
    
def num(text, *params):
    return p.num(text)
    
def compare(text, *params):
    return p.compare(text, params[0])
    
def compare_nouns(text, *params):
    return p.compare_nouns(text,params[0])

def compare_adjs(text, *params):
    return p.compare_adjs(text,params[0])

def a(text, *params):
    return p.a(text)

def an(text, *params):
    return p.an(text)

def present_participle(text, *params):
    return p.present_participle(text)

def classical(text, *params):
    kwargs=dict(param.split('=') for param in params)
    return p.classical(text, **kwargs)
    
def gender(text, *params):
    return p.gender(text)
    
def defnoun(text, *params):
    return p.defnoun(text)
    
def defverb(text, *params):
    return p.defverb(text)
    
def defadj(text, *params):
    return p.defadj(text)
    
def defa(text, *params):
    return p.defa(text)

def defan(text, *params):
    return p.defan(text)
    
# join  


def int_to_words(text, *params):
    try:
        text=int(float(text))
    except: pass
    kwargs=dict(param.split('=') for param in params)
    return p.number_to_words(text, **kwargs)


#--

inflect_english = {
    'compare':compare,
    'compare_nouns':compare_nouns,
    'compare_adjs':compare_adjs,
    'a':a,
    'a2':a,
    'an':an,
    'ordinal': ordinal,
    'number_to_words': number_to_words, 
    'plural':plural,
    'plural_noun':plural_noun,
    'plural_verb':plural_verb,
    'plural_adj':plural_adj,
    'singular_noun':singular_noun,
    'no':no,
    'num':num,
    'present_participle':present_participle,
    'classical':classical,
    'gender':gender,
    'defnoun':defnoun,
    'defverb':defverb,
    'defadj':defadj,
    'defa':defa,
    'defan':defan,
    #
    'int_to_words': int_to_words, 
}