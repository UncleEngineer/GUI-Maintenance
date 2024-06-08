def hello():
    print('Hello, My name is Loong.')

# hello()

def hellofriend(name):
    print(f'Hello, My name is {name}.')

# hellofriend('Somchai')

def checkNameAge(name, age=80):
    print(f'Hello, My name is {name}.')
    print(f'I am {age} years old.')

# checkNameAge('Somsak', 50)
# checkNameAge(age=70, name='Robert')
# checkNameAge('Somsri', 100)

def addNumber(x, y):
    return x + y

sum = addNumber(10, 20)
print(sum)

# Leap Year
# - หาร 4 ลงตัว หรือ หาร 100 ไม่ลงตัว
# - หาร 400 ลงตัว
# year = int(input('ปี ค.ศ. : '))
# if year % 4 == 0 and year % 400 == 0 or year % 100 != 0:
#     print(f'ค.ศ. {year} เป็น Leap year')
# else:
#     print(f'ค.ศ. {year} ไม่เป็น Leap year')

color = ['red', 'green', 'blue']
# print(color[0])
# print(color[1])
# print(color[2])
# print(color[-1])
color.append('yellow')

for c in color:
    print(c)