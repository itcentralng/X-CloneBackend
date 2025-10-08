
# class test:
truemail : str
passwordglo: str
glousername: str


def check_mail(email: str):
    check : bool

    if len(email) > 13:
        print("Email is more than 13 characters")
        if "@" in email and ".com" in email:
            truemail = email
            check = True
        else :
            check = False
        

        if check:
            print("The email is a valid one" )
        elif not check:
            print("This is not a valid mail")

        try:
            print(truemail)
        except Exception as e:
            print(f"{e} this is the reason")
            return ""
    else:
        print("This is email is less than < 13 characters")
        return ""
    


def username(username: str):
    if len(username) > 4:
        print("This is a valid user")
        glousername = username
        print(glousername)
    else:
        print("This is not a valid username!")
        return 
    

def passwordcheck(password: str):
    if len(password) > 8:
        print("This is a valid password")
        passwordglo = password
    else:
        print("Password must be 8char long!")
        return
    

    print(passwordglo)

check_mail("checing@gmail.com")
username("willy")
passwordcheck("emmanuel89")

