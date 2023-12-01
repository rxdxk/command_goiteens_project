from googletrans import Translator
transl=Translator()

def translate_eng(text):
    outstr = transl.translate(text, src='en', dest='uk')
    print(outstr)
    data=outstr.extra_data
    out = data['translation'][0][0]
    return out
    
def translate_ukr(text):
    outstr = transl.translate(text, src='uk', dest='en')
    print(outstr)
    data=outstr.extra_data
    out = data['translation'][0][0]
    return out
