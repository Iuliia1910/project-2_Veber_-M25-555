import prompt


def welcome():
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")
    command = ""
    while command != "exit":
        command = prompt.string("Введите команду: ")
        if command == "help":
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
        elif command == "exit":
            print("До свидания!")
        else:
            print(f"Вы ввели: {command}")

