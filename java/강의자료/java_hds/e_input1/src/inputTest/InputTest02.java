package inputTest;

import java.util.Scanner;

public class InputTest02 {
	public static void main(String[] args) {
//		반려동물 이름을 입력받고 출력하기
		String message = "반려동물 이름: ";
		Scanner sc = new Scanner(System.in);
		String name = null;
		
		System.out.print(message);
		name = sc.next();
		System.out.println(name);
		
		
		
	}
}
