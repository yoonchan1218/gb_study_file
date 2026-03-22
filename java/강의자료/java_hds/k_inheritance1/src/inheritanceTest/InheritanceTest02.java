package inheritanceTest;

class Animal {
	String name;
	int age;
	String feed;
	
	public Animal() {;}

	public Animal(String name, int age, String feed) {
		super();
		this.name = name;
		this.age = age;
		this.feed = feed;
	}

//	메소드 앞에 final을 붙이면, 자식에서는 재정의할 수 없다.
//	즉, 부모에서 구현한 그대로 사용하라는 뜻이다.
	final void walk() {
		System.out.println("걷기");
	}
	
	void run() {
		System.out.println("뛰기");
	}
	
	void eat() {
		System.out.println("먹기");
	}
}

class Lion extends Animal {
	int group;
	
	public Lion(String name, int age, String feed, int group) {
		super(name, age, feed);
		this.group = group;
	}
	
//	@Override
//	void walk() {
//		System.out.print("네 발로 ");
//		super.walk();
//	}
	
//	@Override
//	void walk() {
//		System.out.println("네 발로 걷기");
//	}

	void hunt() {
		System.out.println("사냥하기");
	}
}


public class InheritanceTest02 {
	public static void main(String[] args) {
		Lion 심바 = new Lion("심바", 5, "염소", 3);
		
		심바.walk();
	}
}






















