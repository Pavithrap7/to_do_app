import requests

base_url="http://127.0.0.1:8000"


def task(mail):
    while True:
        print("1.Create Task\t2.Show Tasks\t3.Remove Tasks\t4.Back")
        ans=int(input())
        if ans==1:
            title=input("Enter Name of the Task:")
            description=input("Enter description of the Task:")
            payload={"mail":mail,"task_name":title,"description":description}
            response=requests.post(f"{base_url}/create_task",json=payload)
            if response.status_code==200:
                print("Task added successfully")
            else:
                print("================ERROR==============",response.json())
        if ans==4:
            break


def register():
    name=input("Enter Name:")
    mail_id=input("Enter Mailid:")
    password=input("Enter New Password:")
    repeat_password=input("Repeat Password:")
    if password!=repeat_password:
        print("Please check the password")
        return
    payload={"name":name,"mail_id":mail_id,"password":repeat_password}
    response=requests.post(f"{base_url}/register",json=payload)
    if response.status_code==201:
        print("user registered successfully")
    else:
        print(f"=============ERROR==============\n",response.json())




def login():
    mail=input("Enter Mail_id:")
    password=input("Enter password:")
    payload={"mail_id":mail,"password":password}
    response=requests.post(f"{base_url}/login",json=payload)
    if response.status_code==200:
        print("login successfull")
    else:
        print("================ERROR=============",response.json())
    task(mail)



while True:
    print("========WELCOME TO TODO LIST==========")
    print("1.Register\n2.Login\n3.Exit")
    ans=int(input())
    if ans==1:
        register()
    elif ans==2:
        login()
    elif ans==3:
        break
    
