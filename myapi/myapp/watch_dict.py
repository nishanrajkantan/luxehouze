import re

pp_models    = {'5164a': ['5164a'],
                '5164r': ['5164r'], 
                '5711/1a' : ['5711/1a'],
                '5711/1r' : ['5711/1r', '5711r', '5711 / 1r'], 
                '6102r': ['6102r', '6102 r'],  
                '6102p': ['6102p'], 
                '5110g': ['5110g'], 
                '5110p': ['5110p'],
                '5968g': ['5968g'], 
                '5968a': ['5968a'], 
                '5968/1a': ['5968/1a'],
                '5980r': ['5980r'], 
                '5980/1a': ['5980/1a'], 
                '5990/1a': ['5990/1a', '5990 1a'], 
                '5712r': ['5712r'], 
                '5712/1a': ['5712/1a'],
                '5930p': ['5930p'], 
                '5930g': ['5930g'], 
                '5905/1a': ['5905/1a', '5905 '], 
                '5905r': ['5905r'], 
                '5905p': ['5905p'],
                '7118/1200a': ['7118/1200a'], 
                '7118/1200r': ['7118/1200r'], 
                '7118/1a': ['7118/1a'], 
                '7118/1r': ['7118/1r'], 
                '5269/200r': ['5269/200r']}

rolex_models = {'126710blro jub': ['126710blro jub'],
                '126710blro oys': ['126710blro oys'], 
                '126710blnr jub': ['126710blnr jub','126710blnr,jub'], 
                '126710blnr oys': ['126710blnr oys', '126710 blnr oys'], 
                '116619lb': ['116619lb', '116619 '], 
                '268622': ['268622'], 
                '279171g choc jub': ['279171g choc jub', '279171g choco jubilee'], 
                '279171g green jub': ['279171g green jub'], 
                '279171g purple jub': ['279171g purple jub'], 
                '116508 green': ['116508 green', '116508green', '116508gr', '116508g'], 
                '116508 black': ['116508 black', '116508 blk']}

rm_models    = {'rm055': ['rm055']}

ap_models    = {'26240st': ['26240st']}


text = '5990 1a 1/2022 new'

def forloops(text):
    """ Nested for loops. """
    # model1 = ''
    for model_name, name_variations in pp_models.items():
        for index in name_variations:
            if re.findall(index, text) != []:
                print('----')
                print(model_name)
                print('----')
                model1 = model_name
                brand = 'Patek Philippe'
            else:
                pass

    print(model1)
    print(brand)

    return model1

print(forloops(text))

import re

text = '5164r 1/2022 new'
re.findall('5164r', text)