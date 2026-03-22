package classTask;

public class Company {
	static long seq;
	long id;
	
	String name;
	int total;
	double average;
	
	Department[] arDepartment;
	
//	static 블록
//	최초 1번만 실행
	static {
		seq = 0;
	}
	
//	초기화 블록
//	생성자가 호출될 때마다 실행
	{
		id = ++seq;
	}
	
	
	public Company() {;}


	public Company(String name, Department[] arDepartment) {
		this.name = name;
		this.arDepartment = arDepartment;
		
		for (int i = 0; i < arDepartment.length; i++) {
			total += arDepartment[i].income;
		}
		
		average = (double)total / arDepartment.length;
	}
	
}















