package stream.task;

import java.util.Objects;

public class Animal {
	private String name;
	private int age;
	private String gender;
	
	public Animal() {;}
	
	public Animal(String name) {
		super();
		this.name = name;
	}

	public Animal(String name, int age) {
		super();
		this.name = name;
		this.age = age;
	}

	public Animal(String name, int age, String gender) {
		super();
		this.name = name;
		this.age = age;
		this.gender = gender;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public int getAge() {
		return age;
	}

	public void setAge(int age) {
		this.age = age;
	}

	public String getGender() {
		return gender;
	}

	public void setGender(String gender) {
		this.gender = gender;
	}

	@Override
	public String toString() {
		return "Animal [name=" + name + ", age=" + age + ", gender=" + gender + "]";
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Animal other = (Animal) obj;
		return Objects.equals(name, other.name);
	}
}
