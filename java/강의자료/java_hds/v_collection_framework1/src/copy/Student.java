package copy;

public class Student {
	private long id;
	private String name;
	private int age;
	private Address address;
	
	public Student() {;}
	
	public Student(Student student) {
		this(student.getId(), student.getName(), student.getAge(), new Address(student.getAddress()));
	}
	
	public Student(long id, String name, int age, Address address) {
		super();
		this.id = id;
		this.name = name;
		this.age = age;
		this.address = address;
	}


//	public Student(Student student) {
//		this(student.getId(), student.getName(), student.getAge());
//	}
//
//	public Student(long id, String name, int age) {
//		super();
//		this.id = id;
//		this.name = name;
//		this.age = age;
//	}
	
	public long getId() {
		return id;
	}

	public Address getAddress() {
		return address;
	}

	public void setAddress(Address address) {
		this.address = address;
	}

	public void setId(long id) {
		this.id = id;
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

	@Override
	public String toString() {
		return "Student [id=" + id + ", name=" + name + ", age=" + age + ", address=" + address + "]";
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Student other = (Student) obj;
		return id == other.id;
	}
}
