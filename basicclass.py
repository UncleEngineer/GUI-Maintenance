class Employee:
    # fullname = 'Uncle Engineer'
    # position = 'Python Developer'
    # salary = 50000

    def __init__(self, fullname, position, salary):
        self.fullname = fullname
        self.position = position
        self.salary = salary

    def learn(self):
        print('ฉันกำลังเรียนเขียนโปรแกรม Python')

employee01 = Employee('สมชาย', 'Python Developer', 60000)
print(employee01.fullname)
print(employee01.position)
print(employee01.salary)
employee01.learn()
print('========================================')
employee02 = Employee('โรเบิร์ต', 'Mobile Developer', 100000)
print(employee02.fullname)
print(employee02.position)
print(employee02.salary)
employee02.learn()
print('========================================')
employee03 = Employee('สมศรี', 'Full-stack Developer', 120000)
print(employee03.fullname)
print(employee03.position)
print(employee03.salary)
employee03.learn()