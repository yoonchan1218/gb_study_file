package controlStatementTest;

import java.util.Scanner;

public class IfTest {
	public static void main(String[] args) {
//		두 정수 입력받기
		int number1 = 0, number2 = 0;
		String message = "두 정수를 입력해주세요.";
		String example = "예) 2 3";
		String result = null;
		Scanner scanner = new Scanner(System.in);
		
		System.out.println(message);
		System.out.println(example);
		
		number1 = scanner.nextInt();
		number2 = scanner.nextInt();
		
		if(number1 > number2) {
			result = "더 큰 값: " + number1;
			
		}else if(number2 > number1) {
			result = "더 큰 값: " + number2;
			
		}else {
			result = "두 수가 같습니다.";
		}

		System.out.println(result);
	}
}












