if 1 == 1:
    
    #print('hello from PyNames comminuty')
    import sys, random, webbrowser
    from termcolor import colored

    dict_list = ['en', 'tr', 'fr', 'ar', 'es']
    gender_list = ['male', 'female']
    gender_list_langauge = ['en']
    names = []
    all_names = []
    suggestions = []

    def as_language(language, gender):
        if language == 'en':
            if gender == 'female':
                f = open("datasets/en_female.txt", 'r', encoding='utf-8')
            else:
                f = open("datasets/en_male.txt", 'r', encoding='utf-8')
        elif language == 'fr':
            f = open('datasets/fr.txt', 'r', encoding='utf-8')
        elif language == 'ar':
            f = open('datasets/ar.txt', 'r', encoding='utf-8')
        elif language == 'tr':
            f = open('datasets/tr.txt', 'r', encoding='utf-8')
        elif language == 'es':
            f = open('datasets/es.txt', 'r', encoding='utf-8')
        try:
            line  = f.readlines()
            for li in line:
                if li:
                    names.append(li.strip())
                else:
                    break
        except:
            print("Can not append name to names list!!!")

    def as_gender(language, gender):
        if language is not 'en':
            if gender == 'female':
                print(colored('the names can be wrong!', 'red'))
            else:
                pass
        else:
            pass

    def edit(name):
        newname = []
        num1 = 0
        num2 = 0
        for string in name:
            newname.append(string)
        for string in newname:
            num1 += 1
        name = ''
        for string in newname:
            if num2 == num1 - 1:
                break
            else:
                name = name + newname[num2]
            num2 += 1
        return name

    def generate_name(language = 'en', gender='male', size = 1, type='array'):
        global names
        as_language(language, gender)
        as_gender(language, gender)
        if language in dict_list:
            pass
        else:
            print('we dont support ' + language + ' we support these languages;' + str(dict_list) + 'the name will be generate in english')
            language = 'en'
        if type == 'array':
            output = []
            for name in range(size):
                name = random.choice(names)
                output.append(edit(name))
            return output
        elif type == 'string':
            for name in range(size):
                name = random.choice(names)
                return(edit(name))

    def check_name(name, language='en'):
        if language in dict_list:
            pass
        else:
            print('we dont support ' + language + ' we support these languages;' + str(dict_list) + 'the name will be generate in english')
            language = 'en'
        if language == 'en':
            f = open('pynamegenerator/datasets/en.txt', 'r')
        elif language == 'tr':
            f = open('pynamegenerator/datasets/tr.txt', 'r')
        elif language == 'fr':
            f = open('pynamegenerator/datasets/fr.txt', 'r')
        elif language == 'ar':
            f = open('pynamegenerator/datasets/ar.txt', 'r')
        elif language == 'es':
            f = open('pynamegenerator/datasets/es.txt', 'r')
        name = name + '\n'
        t = 0
        for line in f.readlines():
            if line:
                if name == line or name.upper() == line.upper() or name.lower() == line or name.lower() == line.lower():
                    t = 1
                    return True
                else:
                    continue
        if t == 0:
            return False
        else:
            pass

    def fit(arg1, arg2):
        arg1, arg2 = arg1.lower() + '\n', arg2.lower()
        arg1_a, arg2_a = [], []
        num = 0
        for e in arg1:
            arg1_a.append(e)
        for e2 in arg2:
            arg2_a.append(e2)
        if len(arg1) >= len(arg2) - 1:
            for el in arg1_a:
                for el2 in arg2_a:
                    if el == el2:
                        num += 1
            if num >= len(arg1_a) - 1:
                if arg1_a[0].lower() == arg2_a[0].lower():
                    if edit(arg2.lower()) in suggestions:
                        pass
                    else:
                        suggestions.append(edit(arg2))
        return suggestions

    def suggest(name, language='en'):
        if language in dict_list:
            pass
        else:
            print('we dont support ' + language + ' we support these languages;' + str(dict_list) + 'the name will be generate in english')
            language = 'en'
        if language == 'en':
            f = open('pynamegenerator/datasets/en.txt', 'r')
        elif language == 'tr':
            f = open('pynamegenerator/datasets/tr.txt', 'r')
        elif language == 'fr':
            f = open('pynamegenerator/datasets/fr.txt', 'r')
        elif language == 'ar':
            f = open('pynamegenerator/datasets/ar.txt', 'r')
        elif language == 'es':
            f = open('pynamegenerator/datasets/es.txt', 'r')
        for line in f.readlines():
            fit(name, line)
        return suggestions

    def get_info():
        en = open('pynamegenerator/datasets/en.txt', 'r')
        tr = open('pynamegenerator/datasets/tr.txt', 'r')
        fr = open('pynamegenerator/datasets/fr.txt', 'r')
        ar = open('pynamegenerator/datasets/ar.txt', 'r')
        es = open('pynamegenerator/datasets/es.txt', 'r')
        for line in en.readlines():
            line = edit(line)
            all_names.append(line)
        for line in tr.readlines():
            line = edit(line)
            all_names.append(line)
        for line in fr.readlines():
            line = edit(line)
            all_names.append(line)
        for line in ar.readlines():
            line = edit(line)
            all_names.append(line)
        for line in es.readlines():
            line = edit(line)
            all_names.append(line)
        return print(str(len(all_names)) + ' names, ' + str(len(dict_list)) + ' languages ')

    def help():
        print(colored('please check out the README.md file on the repository', 'green'))
        webbrowser.open('https://github.com/kerem700916/pynamegenerator.git')

else:
    pass
