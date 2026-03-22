package operTest;

import java.util.Scanner;

public class OperTest02 {
	public static void main(String[] args) {
//		두 정수 입력받기
		int number1 = 0, number2 = 0;
		String message = "두 정수를 입력해주세요.";
		String example = "예) 2 3";
//		int result = 0;
		String result = null;
		Scanner scanner = new Scanner(System.in);
		
		System.out.println(message);
		System.out.println(example);
		
		number1 = scanner.nextInt();
		number2 = scanner.nextInt();
		
//		더 큰 값을 출력
//		두 수가 같으면 "두 수가 같습니다" 출력
		result = number1 < number2 ? "더 큰 값: " + number2 
				: number1 == number2 ? "두 수가 같습니다." : "더 큰 값: " + number1;
		System.out.println(result);
		
	}
}















