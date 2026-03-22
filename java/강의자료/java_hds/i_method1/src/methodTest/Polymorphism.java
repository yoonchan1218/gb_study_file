package methodTest;

public class Polymorphism {
	int add(int number1, int number2) {
		System.out.println("두 정수의 덧셈");
		return number1 + number2;
	}
	
	int add(int number1, int number2, int number3) {
		System.out.println("세 정수의 덧셈");
		return number1 + number2 + number3;
	}
	
	double add(double number1, double number2) {
		System.out.println("두 실수의 덧셈");
		return number1 + number2;
	}
	
	int add(int... numbers) {
		System.out.println("여러 정수의 총 합");
		int total = 0;
		for (int i = 0; i < numbers.length; i++) {
			total += numbers[i];
		}
		return total;
	}
	
	public static void main(String[] args) {
		int result = new Polymorphism().add(1, 2, 3, 4, 5);
		System.out.println(result);
	}	
}




