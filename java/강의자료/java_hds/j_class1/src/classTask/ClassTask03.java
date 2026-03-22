package classTask;

// 동물 클래스 선언

// 변수
// 이름, 나이, 체력, 먹이 개수, 먹이 종류

// 메소드
// 먹기, 산책하기

// 먹기
// 체력 1 증가, 먹이 개수 1 감소

// 산책
// 체력 1 감소
class Pet {
	String name;
	int age;
	int hp;
	int feedCount;
	String feedName;
	
//	Ctrl + Space bar, 확인하고 엔터
	public Pet() {;}
	
//	Alt + Shift + s, o, 확인하고 엔터
	public Pet(String name, int age, int hp, int feedCount, String feedName) {
		this.name = name;
		this.age = age;
		this.hp = hp;
		this.feedCount = feedCount;
		this.feedName = feedName;
	}
	
	void eat() {
		hp++;
		feedCount--;
	}
	
	void walk() {
		hp--;
	}
	
}

public class ClassTask03 {

}














