
'''scoping rules in the functions in python'''
import foo as methods

a = 42
b = 10
def foo():
    a = 30

foo()
print("a:",a)   # the value of a does not change here


def foo_1():
    global a    # 'a' is in global namespace now
    a = 30
    b = 20      # the value of b will not change as its not in the global namespace

foo_1()
print("a:",a)

# python supports nested functions definitions

def countdown(start):
    n = start
    def display():
        print("T-minus %d",n)
    def decreament():
        nonlocal n      # bind to outer n, only available in python 3
        global a
        a = 1000
        n -= 1
    while(n>0):
        display()
        decreament()

countdown(10)
print("a",a)


'''function as objects and closures'''
x = 4321

def helloworld():
    return "hello world, val of x:%d" % x

'''n the above case, the helloworld function uses the value of x that is defined in the same environment as where helloworld
function is defined. Although variable 'x' with same name is define in the module where this function is being called, #
that is not used. When the statements that make up a functions are packaged together with the environment in which they execute, the 
resulting object is known as closure 
'''

print(methods.callf(helloworld))
print(helloworld.__globals__)   # in this one can see the

'''when nested functions are used, closure capture the entire environment needed for the inner function to execute'''

def bar():
    x = 13;
    def helloworld():
        return "hello world, val of x:%d" % x

    print(methods.callf(helloworld))

bar()

'''closure is highly effective way to  preserve state across a series of function calls'''
def countdown_1(start):
    def next():
        nonlocal start
        r = start
        start -= 1
        return r
    return next


next = countdown_1(10)
while True:
    v = next()
    print(v)
    if not v: break


'''Decorators is a function whose primary purpose is t wrap another function or class'''

enable_tracing = True
if enable_tracing:
    debug_log = open("debug.log",'w')

def trace(func):
    if enable_tracing:
        def callf(*args,**kwargs):
            debug_log.write("Calling %s: %s, %s \n" % (func.__name__,args,kwargs))
            r = func(*args,**kwargs)
            debug_log.write(" %s returned %s \n" % (func.__name__,r))
            return r
        return callf
    else:
        return func

@trace
def square(x):
    return x*x

print(square(5))


'''Generators and yield: If a function uses the "yield" keyword, it defines the object known as generator
A generator is a function which uses a sequence of values for use in iteration'''
def countdown_2(n):
    print("Counting down from: %d" % n)
    while n > 0:
        yield n
        n -= 1

#print(countdown_2(5).__next__())
for n in countdown_2(10):
    print(n)
    if n == 4:
        break


'''coroutine'''
def receiver():
    print("Ready to receive")
    while True:
        n = (yield)
        print("Got %s" % n)

r = receiver()
r.__next__()
r.send(1)
r.send(2)
r.send('hello')

'''in the above coroutine, the calling of __next__ is necessary and it can be easily overlooked, for that one can write
a decorator'''
def coroutine(func):
    def start(*args,**kwargs):
        g = func(*args,**kwargs)
        g.__next__()
        return g
    return start

@coroutine
def receiver_1():
    print("Ready to receive")
    while True:
        n = (yield)
        print("Got %s" % n)

#example use
r1 = receiver_1()
r1.send("helloooooo")

'''coroutines will run indefinitely unless it is explicitly shut down or it exist on its own. To close the stream of input values, 
use close()
'''
r1.close()
## r1.send(4)   this will generate StopIteration exception

'''close function raises GeneratorExit inside the coroutine'''

@coroutine
def receiver_2():
    print("Ready to receive")
    try:
        while True:
            n = (yield)
            print("Got %s" % n)
    except GeneratorExit:
        print("Receiver Done")

r2 = receiver_2()
r2.send("python")
r2.send("learning")
r2.close()
#r2.send("learning")     # this will throw an StopIteration exception


'''coroutine can simultaneously receive and emit return values using yield if values are supplied in the yield expression'''

def line_splitter(delimiter = None):
    print("ready to split")
    result = None
    while True:
        print("here")
        line = (yield result)
        print("received:",line,result)
        result = line.split(delimiter)  # in this case, coroutine yields the same result as before, but now send() also produces results

'''the first next() call advances the coroutine to (yield result), which returns None, the initial value of result.
On the next send() call, the received value is placed in line, and split into result. The value returned by 
send() is the value passed to the next yield statement. In other words, the value returned by send() comes from the next
yield statement , not the one responsible for receiving the value passed by send()
'''
print("--------------------------------------------------------------------------------------------------------------")
s = line_splitter(",")
print("calling next")
s.__next__()
print("send()")
print(s.send("A,B,C"))
print("send()")
print(s.send("A1,B2,C3"))






