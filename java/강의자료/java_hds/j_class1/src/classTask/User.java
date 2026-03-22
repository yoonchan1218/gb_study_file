package classTask;
//회원번호
//이름
//나이
public class User {
	long id;
	String name;
	int age;
	
	Excercise[] arExcercise;
	
	int totalCal;
	
	public User() {;}

	public User(long id, String name, int age, Excercise[] arExcercise) {
		super();
		this.id = id;
		this.name = name;
		this.age = age;
		this.arExcercise = arExcercise;
		
		for (int i = 0; i < arExcercise.length; i++) {
			totalCal += arExcercise[i].calorie;
		}
	}
}


















