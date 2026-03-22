package staticTest;

public class Company {
	String name;
	int income;
	static int totalIncome;
	
	public Company() {;}

	public Company(String name, int income) {
		this.name = name;
		this.income = income;
	}
}
