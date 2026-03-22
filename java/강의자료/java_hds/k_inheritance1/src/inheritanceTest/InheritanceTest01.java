package inheritanceTest;

class A {
	String name;
	int age;
	
	public A() {
		System.out.println("부모 생성자 호출됨");
	}
	
	public A(String name, int age) {
		this.name = name;
		this.age = age;
	}
}

class B extends A {
	String gender;
	
	public B() {
		System.out.println("자식 생성자 호출됨");
	}

	public B(String name, int age, String gender) {
		super(name, age);
		this.gender = gender;
	}
}

public class InheritanceTest01 {
	public static void main(String[] args) {
		B b = new B();
		
//		b.age = 20;
//		b.name = "홍길동";
		
//		B b = new B("홍길동", 20, "선택안함");
		System.out.println(b.age);
		System.out.println(b.name);
	}
}















