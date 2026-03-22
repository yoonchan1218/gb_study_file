package classTask;

// 동물이 3마리 있다.
// 모든 동물은 이름, 나이, 성별이 있다.
// 3마리 동물은 각자 자기소개를 할 수 있다.
// 클래스를 활용하여 3마리 동물이 자기소개할 수 있도록 구현한다.
class Animal {
	String name;
	int age;
	String gender;
	
	public Animal() {;}

	public Animal(String name, int age, String gender) {
		this.name = name;
		this.age = age;
		this.gender = gender;
	}
	
	void introduce() {
		System.out.println("이름: " + this.name);
		System.out.println("나이: " + this.age + "살");
		System.out.println("성별: " + this.gender);
	}
}

public class ClassTask01 {
	public static void main(String[] args) {
		Animal[] arAnimal = {
				new Animal("바둑이", 5, "수컷"),
				new Animal("호범이", 8, "암컷"),
				new Animal("꿀돼지", 2, "암컷")
		};
		
		for (int i = 0; i < arAnimal.length; i++) {
			arAnimal[i].introduce();
		}
	}
}








