package inputTest;

import java.util.Scanner;

public class InputTest03 {
	public static void main(String[] args) {
//		3개의 정수를 한 번에 입력받은 후 덧셈 결과 출력
		
//		1. 3개의 정수를 담을 변수를 선언한다.
		int number1 = 0;
		int number2 = 0;
		int number3 = 0;
		
		
//		2. 사용자에게 출력할 메세지를 담는다.
		String message = "3개의 정수를 입력하세요.";
		String example = "예) 3 2 4";
		
//		3. 3개의 정수를 더한 결과를 담을 변수를 선언한다.
		int result = 0;
		
//		4. 입력할 준비를 한다(Scanner)
		Scanner sc = new Scanner(System.in);
		
//		5. 사용자에게 메세지를 출력한다.
		System.out.println(message);
		System.out.println(example);
		
//		6. 정수 3개를 입력받는다.
		number1 = Integer.parseInt(sc.next());
		number2 = Integer.parseInt(sc.next());
		number3 = Integer.parseInt(sc.next());
		
//		7. 모든 정수를 더한 뒤 결과를 변수에 담는다.
		result = number1 + number2 + number3;
		
//		8. 결과를 출력한다.
		System.out.println(result);
	}
}








