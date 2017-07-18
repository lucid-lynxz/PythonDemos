# 类功能介绍
# 定义一个程序员类
class Programmer(object):
    hobby = 'Computer science'  # 类属性
    __slots__ = ('name', 'age') # 用tuple定义允许绑定的属性名称

    # 创建类实例的时候会先调用 __new__ 然后才是 __init__
    def __new__(cls, *args, **kwargs):
        print("Programmer __new__ called")
        # 重写object子类的__new__方法时,只要传入cls参数即可,后两个参数不要传,不然报错: TypeError: object() takes no parameters
        return super(Programmer, cls).__new__(cls)

    def __init__(self, name, age, weight):
        self.name = name  # 对象变量,可以直接访问,类似public
        self._age = age  # 避免直接访问, 类似private
        self.__weight = weight  # 类似private

    # 该注解表明本方法返回对象属性,使用时不要添加括号,测试加括号的话会报错: TypeError: 'int' object is not callable
    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self,value):
        if not isinstance(value,int):
            raise ValueError('weight must be an integer!')
        if value < 0 or value > 400:
            raise ValueError('weight must between 0-400')
        self.__weight = value

    # 该注解表明本方法为类方法
    @classmethod
    def get_hobby(cls):
        return cls.hobby

    # 判断两个对象是否相等
    def __eq__(self, other):
        if isinstance(other, Programmer):
            if self._age == other._age:
                return True
            else:
                return False
        else:
            raise Exception("The type of object must be Programmer")

    # 重写方法,用于将对象转换为字符串输出信息
    # python 中有三个可以输出对象的函数 __str__ , __repr__ , __unicode__
    def __str__(self):
        return '%s is %s years old' % (self.name, self._age)


# 后端程序员类
class BackProgrammer(Programmer):
    def __new__(cls, *args, **kwargs):
        print("BackProgrammer __new__ called")
        # 普通类的子类,__new__方法需要传入所有参数
        return super(BackProgrammer, cls).__new__(cls, *args, **kwargs)

    def __init__(self, name, age, weight, language):
        # 使用父类方法, super关键字
        super(BackProgrammer, self).__init__(name, age, weight)
        self.language = language


if __name__ == '__main__':
    programmer = BackProgrammer('lynxz', 30, 75, 'Python')
    # print(dir(programer))  # 打印所有属性
    print(Programmer.get_hobby())  # 类方法,使用类名来调用即可
    print(programmer.weight)  # 已添加注解 @property ,调用时不要加括号
    print(programmer.__dict__)  # 打印对象变量
    print("%s %s %s" % (programmer.name, programmer.weight, programmer._Programmer__weight))  # 字符串模板
    print(type(programmer))  # 打印对象类型 => <class '__main__.BackProgrammer'>
    print(isinstance(programmer, Programmer))  # 判断对象是否是某个类型的实例
    print(programmer.__str__())