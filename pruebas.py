#Importamos las librerias necesarias
import openpyxl
import secrets

#Creamos la ruta a la base de datos
databasedir = "database.xlsx"

#Creamos la variable general del usuario activo y de administrador
activeuser = ""
admin = False

#Con esta función crearemos un usuario nuevo siempre y cuando no exista
#uno bajo el mismo dni, en dicho caso devolveremos el error por pantalla y 
#volveremos a la instancia principal.

def register():
    #Abrimos la base de datos
    databasexlsx = openpyxl.load_workbook(databasedir)
    database = databasexlsx["login"]
    print("====================================================")
    print("//                   ARTIBANK SL                  //")
    print("====================================================")

    #Pedimos el dni al usuario
    user = input("-Introduzca su dni:")

    #Comparamos el dni con la base de datos
    for dni in range(2, 1048576):
        #Si ya existe en nuestra base de datos activamos el bit de existencia
        if database.cell(row=dni, column=1).value == user:
            print("El dni introducido ya tiene una cuenta: ")
            dniexists = True
            break
        else:
            dniexists = False
    #Si no existia el dni en nuestra base de datos pedimos la contraseña
    if not dniexists:
        pwd1 = input("-Introduzca su contraseña:")
        pwd2 = input("-Vuelva a introducir su contraseña:")
        if pwd1 == pwd2:
            pwdmissmatch = False
            for dni in range(2, 1048576):
                if database.cell(row=dni, column=1).value == None:
                    database.cell(row=dni, column=1).value = user
                    database.cell(row=dni, column=2).value = pwd2
                    databasexlsx.save(databasedir) 
                    break
        else:
            print("Las contraseñas no coinciden.")
            pwdmissmatch = True
            
    if dniexists or pwdmissmatch:
        print("Ha habido un error registrando el usuario.")

def login():
    #Accedemos a las variables globales
    global activeuser
    global admin

    #Abrimos la base de datos
    databasexlsx = openpyxl.load_workbook(databasedir)
    database = databasexlsx["login"]
    print("====================================================")
    print("//                   ARTIBANK SL                  //")
    print("====================================================")

    #Pedimos el dni y la contraseña al usuario
    user = input("-Introduzca su dni:")
    pwd =  input("-Introduzca su contraseña:")

    #Comparamos los valores con los de la base de datos
    for dni in range(2, 1048576):
        if database.cell(row=dni, column=1).value == user:
            if database.cell(row=dni, column=2).value == pwd:
                #Si la contraseña hace match con ese user devolvemos success
                activeuser = user
                if database.cell(row=dni, column=3).value == 1:
                    admin = True
                print("success")
            else:
                #Si la contraseña no hace match con ese user devolvemos password para identificar el error
                print("wrong password")
    #Si recorremos toda la base de datos y no encontramos el dni devolvemos user para saber que no existe
    print("user doesn't exists")

def logout():
    #Accedemos a las variables globales
    global activeuser
    global admin

    activeuser = ""
    admin = False

    return  "logged out"

def createaccount():
    #Accedemos a las variables globales
    global activeuser
    global admin

    #Abrimos la base de datos
    databasexlsx = openpyxl.load_workbook(databasedir)
    database = databasexlsx["accounts"]
    users = databasexlsx["login"]

    print("====================================================")
    print("//                   ARTIBANK SL                  //")
    print("====================================================")
    
    if admin:
        user = input("A que usuario desea crearle una cuenta?: ")
        for usr in range(2, 1048576):
            #Comprobamos que exista ese usuario
            if users.cell(row=usr, column=1).value == user:
                for acc in range(2, 1048576):
                    if database.cell(row=acc, column=1).value == None:
                        database.cell(row=acc, column=1).value = secrets.token_hex(16)
                        database.cell(row=acc, column=2).value = int("0")
                        database.cell(row=acc, column=3).value = user
                        print(f"La nueva cuenta de {user} es: {database.cell(row=acc, column=1).value}")
                        databasexlsx.save(databasedir) 
                        break
    else:
        for acc in range(2, 1048576):
            if database.cell(row=acc, column=1).value == None:
                database.cell(row=acc, column=1).value = secrets.token_hex(16)
                database.cell(row=acc, column=2).value = int("0")
                database.cell(row=acc, column=3).value = activeuser
                print(f"Tu nueva cuenta es: {database.cell(row=acc, column=1).value}")
                databasexlsx.save(databasedir) 
                return 0
    print("No existe ese usuario.")

activeuser = "72193101B"
createaccount()