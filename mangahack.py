import requests
import pyfiglet
titulo = "MangaHack"
ascii_art = pyfiglet.figlet_format(titulo)
print(ascii_art)


idusuario = int(input('ID do usuário: '))
senha = str(input('Senha: '))
idescola = int(input('ID da escola: '))

data = {
    "studentId": idusuario,
    "password": senha,
    "schoolId": idescola
}

login = requests.post('https://api.mangahigh.com/auth', json=data)
token = login.json()["id"]
uid = login.json()["userId"]

if login.status_code == 200 or login.status_code == 201:

    # Login

    print(f"Retornou: {login.status_code} (Sucesso)")
    print("Login bem-sucedido!")
    print(f'Token da sessão: {token}')
    print(f'UserID: {uid}')

    # Informações das questões
  
    question = requests.get(f'https://api.mangahigh.com/user/{uid}/student-activity-challenge', cookies={"session": token})
    questionname = requests.get(f'https://api.mangahigh.com/objective/{question}', cookies={"session": token})

    #Listagem de questões e formatação
  
    listaquestoes = []
    for c in range(len(question.json()["collection"])):
      az = question.json()["collection"][c]["id"]["objectiveId"]
      listaquestoes.append(az)
      a = print('Questão nº', az, '- ', end='')
      ab = f'https://api.mangahigh.com/objective/{az}'
      b = requests.get(f'{ab}', cookies={"session": token})
      print(b.json()["name"], '\n')
  
    opcao = int(input('\nQual questão gostaria de ganhar medalha?: '))
  
    while opcao not in listaquestoes:
      opcao = int(input('\033[1;31mDigite uma questão listada!:\033[m '))

    medalha = int(input('[ 1 ] \033[1;35m★ Bronze\n\033[m[ 2 ] \033[1;37m★ Prata\n\033[m[ 3 ] \033[1;33m★ Ouro'))

    atividade = requests.get(f'https://api.mangahigh.com/objective/{opcao}', cookies={"session": token})
    activityid = atividade.json()["activityId"]
    print(activityid)
    
    questoesi = requests.get(f'https://campus.mangahigh.com/participate/lesson/{activityid}', cookies={"session": token})
    listaquestoesi = []
    listaquestoesi.append(questoesi.json()["questions"]["X"][0]["itemId"])
    hashquestoesstr = questoesi.json()["questions"]["X"][0]["itemId"]
    hashquestoesstr2 = f'{hashquestoesstr}' * 10
    print(hashquestoesstr2)
    print(listaquestoesi)
    data2 = '{{"lessonId":"{}","locale":"pt-br","challengeId":null,"startLevel":"X","endLevel":"X","timerEnabled":false,"questionsList":[{{"itemId":{},"locale":"pt_br","score":400,"correct":true,"hintTaken":false,"timeTaken":16,"solutionTaken":false,"passTaken":false,"level":"X"}},{{"itemId":{},"locale":"pt_br","score":800,"correct":true,"hintTaken":false,"timeTaken":7,"solutionTaken":false,"passTaken":false,"level":"X"}},{{"itemId":{},"locale":"pt_br","score":1600,"correct":true,"hintTaken":false,"timeTaken":27,"solutionTaken":false,"passTaken":false,"level":"X"}},{{"itemId":{},"locale":"pt_br","score":1600,"correct":true,"hintTaken":false,"timeTaken":6,"solutionTaken":false,"passTaken":false,"level":"X"}},{{"itemId":{},"locale":"pt_br","score":1600,"correct":true,"hintTaken":false,"timeTaken":10,"solutionTaken":false,"passTaken":false,"level":"X"}},{{"itemId":{},"locale":"pt_br","score":1600,"correct":true,"hintTaken":false,"timeTaken":24,"solutionTaken":false,"passTaken":false,"level":"X"}},{{"itemId":{},"locale":"pt_br","score":1600,"correct":true,"hintTaken":false,"timeTaken":22,"solutionTaken":false,"passTaken":false,"level":"X"}},{{"itemId":{},"locale":"pt_br","score":1600,"correct":true,"hintTaken":false,"timeTaken":13,"solutionTaken":false,"passTaken":false,"level":"X"}},{{"itemId":{},"locale":"pt_br","score":1600,"correct":true,"hintTaken":false,"timeTaken":37,"solutionTaken":false,"passTaken":false,"level":"X"}},{{"itemId":{},"locale":"pt_br","score":1600,"correct":true,"hintTaken":false,"timeTaken":18,"solutionTaken":false,"passTaken":false,"level":"X"}}],"securityHash":""}}'.format(activityid, listaquestoesi[0], listaquestoesi[0], listaquestoesi[0], listaquestoesi[0], listaquestoesi[0], listaquestoesi[0], listaquestoesi[0], listaquestoesi[0], listaquestoesi[0], listaquestoesi[0])
    correcttrue = requests.post(f'https://campus.mangahigh.com/user/{uid}/prodigi/{activityid}/participate', data=data2, cookies={"session": token})
    print(correcttrue)
    print(correcttrue.json())

    # Falha no login

else:
    print("Falha no login.")
    print(login.status_code)
