import random
from datetime import datetime
import math

class Account(object):
    num_accounts = 0    # this is not tied to any of the object and its value is shared among all the objects/instances of the class

    def __init__(self,name,balance):
        self.name = name
        self.balance = balance
        Account.num_accounts += 1

    def __del__(self):
        Account.num_accounts -= 1

    def deposit(self,amt):  # instance methods
        self.balance += amt     # classes do not create the scope for the names used inside the bodies of methods. #
        # Therefore, always use self.balance and not balance

    def withdraw(self,amt):     # instance methods
        balance = 100
        self.balance -= amt

    def inquiry(self):      # instance methods
        return self.balance


class Foo(object):
    def bar(self):
        print("Bar!!")

    def spam(self):
        self.bar()  # do not use bar() or bar(self) but self.bar() otherwise it will give NameError
        Foo.bar(self)   # this works also fine


'''Inheritance: Super class of EvilAccount is Account. Inheritance below is implemented with only slight enhancement of the dot operator
Specifically, if the search for an attribute does not find a match, then search moves on to the base class'''
class EvilAccount(Account):
    def inquiry(self):
        if random.randint(0,4) == 1:
            return self.balance * 1.10
        else:
            return self.balance

#create a few accounts
a = Account('Billy',10)     # invokes Account.__init__(a,'Billy',10)
b = Account('Bill',100)

a.deposit(100)
b.withdraw(50)
print(a.name)

'''explicit use of self is required because python does not provide a means to explicity declare a variable like C and C++. Without this there is no way to know
whether an to a variable in a method is supposed to be a local varible or if its supposed to be saved as an instance attribute. The explicit use of self fixes
this - all values stored on self are part of the instance and all other assignments are just local variables '''


c = EvilAccount("George",100)
c.deposit(10)   # this calla the method deposit() defined in the Account class
print(c.inquiry())

'''A subclass can also have __init__() method and add its own new attributes'''
'''sometime you want to call the method of the super class which has original implementation, for that, super().<MethodName>() can be used'''
class MoreEvilAccount(EvilAccount):
    def deposit(self,amount):
        self.withdraw(5)    # subtract convenience fee
        super().deposit(amount)


ex = MoreEvilAccount("heyo",100)
ex.deposit(1)
print(ex.inquiry())

'''static methods in the class can be defined using the decorator @staticmethod. It is an ordinary method which just happens to live inside the class namespace
A common use of the static method is in writing a class where you have many ways to create instances. Because you can not write more than one __init__() methods
for all those ways. In C++ you can define more than one ctor with dfferent arguments. Here its not possible So use static methods'''

class Date(object):
    def __init__(self,year,month,day):
        self.day = day
        self.month = month
        self.year = year

    @staticmethod
    def now():
        t = datetime.now()
        return Date(t.year,t.month,t.day)

    @staticmethod
    def tomorrow():
        t = datetime.now()
        return Date(t.year,t.month,t.day+1)

a_date = Date(1,10,100)
print(a_date.day,a_date.month,a_date.year)

a_date_now = Date.now()
print(a_date_now.day,a_date_now.month,a_date_now.year)

'''class methods are methods that operate on the class itself as an object. This can be defined using the @classmethod decorator'''

class Times(object):
    factor =1
    @classmethod
    def mul(cls,x):
        return cls.factor*x

class TwoTimes(Times):
    factor = 2

x = TwoTimes.mul(5)     # calls Times.mul(TwoTimes,5) -> 10 will be the answer
print(x)


class EuroDate(Date):
    def __str__(self):
        return "%02d/%02d/%04d" % (self.day,self.month,self.year)


euDate = EuroDate.now()
print(euDate)

# Because the class inherits from Date, it has all the same features. However, now() and tomorrow() will still return Date object instead of EuroDate object
# A classmethod can fix this
'''
class Date(object):
    ...
    @classmethod
    def now(cls):
        t = datetime.now()
        return cls(t.year,t.month,t.day)
        
class EuroDate(Date):
    ...

a = Date.now()  -> returns Date object
b = EuroDate.now() -> returns EuroDate object

'''


'''
Properties
A property is a special kind of attribute that computes its value when accessed 
'''

class Circle(object):
    def __init__(self,radius):
        self.radius = radius

    @property
    def area(self):
        return math.pi*self.radius**2

    @property
    def perimeter(self):
        return 2*math.pi*self.radius


c1 = Circle(4)
print("Radius:",c1.radius,"area:",c1.area,"perimeter:",c1.perimeter)
c1.radius = 6
# c1.area = 50 This will give error becase attribute can not be set. This is where the use of the object can get to know that its not a simple attribute of the class
# but a property and it can not be set

# properties can also intercept the operation of setting value and delete an attribute as shown below

class Square(object):
    def __init__(self,length):
        self.__sidelength = length

    @property
    def sidelength(self):
        return self.__sidelength

    @sidelength.setter
    def sidelength(self,value):
        if not isinstance(value,float):
            raise TypeError("Must be a float")
        self.__sidelength = value

    @sidelength.deleter
    def sidelength(self):
        raise TypeError("Cant delete the side length of square")


sq1 = Square(3)
print("Side length of square:",sq1.sidelength)
sq1.sidelength = 4.4    # any other value e.g. 4 will give an error
print("Side length of square:",sq1.sidelength)

# del sq1.sidelength will generate an error
'''in the above example, the name is defined as read only property using @property decorator and associated method. The @sidelength.setter and @sidelngth.deleter
decorators that follow are associating additional methods with set and deletion operations on the sidelength attribute
'''



'''With properties access to an attribute is controlled by a series of user-defined get,set and delete function. 
This sort of attribute can be generalized through the use of descriptor object.
'''
class TypedProperty(object):
    def __init__(self,name,type,default = None):
        self.name = "_" + name
        self.type = type
        self.default = default if default else type()

    def __get__(self,instance,cls):
        return getattr(instance,self.name,self.default)

    def __set__(self, instance, value):
        if not isinstance(value,self.type):
            raise TypeError("Must be %s" % self.type)
        setattr(instance,self.name,value)

    def __delete__(self,instance):
        raise AttributeError("Cant delete attribute")


class Mydata(object):
    name = TypedProperty("name",str)
    num = TypedProperty("num",int,42)

data1 = Mydata()
data1.name = "Ishan"
print("MyData:",data1.name,"Num:",data1.num)

# del data1.name This will give error from __delete__
'''Descriptors can only be allowed at class level. It is not legal to create descriptors per instance basis by creating descriptor object inside __init__ method

'''