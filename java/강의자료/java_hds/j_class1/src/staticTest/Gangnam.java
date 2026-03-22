package staticTest;

public class Gangnam {
	public static void main(String[] args) {
		Company 한동석 = new Company("한동석", 1000);
		Company 김민환 = new Company("김민환", 3000);
		
		Company.totalIncome += 한동석.income;
		Company.totalIncome += 김민환.income;
		
//		객체로 접근하는 것은 의미가 없다.
//		한동석.totalIncome -= 1000;
		
		System.out.println(Company.totalIncome);
	}
}











