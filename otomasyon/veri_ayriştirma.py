# Kullanıcı ayıklamada kullandığım kodlar.
# -
# 
def user_control():
    user_counts = {}  

    with open('data.txt', 'r', encoding='utf-8') as control:
        for line in control:
            username = ' '.join(line.strip().split())  
            username = username.split(" -- ")[0]  

            if username in user_counts:
                user_counts[username] += 1
            else:
                user_counts[username] = 1

    for username, count in user_counts.items():
        print(f"{username}: {count}")


# Dosya içerisindeki eşsiz kullanıcıları bulmak için script.
# -
# 
def uniq_user():
    unique_users = set()
    with open('user.txt', 'r', encoding='utf-8') as control:
        for line in control:
            user = line.strip()  
            unique_users.add(user)
    for user in unique_users:
        print(user)


if __name__ == "__main__":
    user_control()
    #uniq_user()
