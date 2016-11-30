
 
public class Demo{
public static void main(String[] args) {
Dog myDog = new Dog("行行圈");
myDog.say(); // 子类的实例调用子类中的方法
Animal myAnmial = new Animal("行行圈在线");
myAnmial.say(); // 父类的实例调用父类中的方法
}
}

class Animal{
String name;
public Animal(String name){
this.name = name;
}
public void say(){
System.out.println("我是一只小动物，我的名字叫" + name + "，我会发出叫声");
}
}

class Dog extends Animal{
// 构造方法不能被继承，通过super()调用
public Dog(String name){
super(name);
}
// 覆盖say() 方法
public void say(){
System.out.println("我是一只小狗，我的名字叫" + name + "，我会发出汪汪的叫声");
}
}
 