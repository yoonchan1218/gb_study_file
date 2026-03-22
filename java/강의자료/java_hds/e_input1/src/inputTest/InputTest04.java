package inputTest;

import java.util.Scanner;

public class InputTest04 {
	public static void main(String[] args) {
//		나이와 이름 입력받고 출력하기
		int age = 0;
		String name = null;
		String nameMessage = "이름: ";
		String ageMessage = "나이: ";
		Scanner sc = new Scanner(System.in);
		String nameResultMessage = "저의 이름은 ";
		String ageResultMessage = "저의 나이는 ";
		
		System.out.print(nameMessage);
		name = sc.next();
		
		System.out.println(ageMessage);
		age = Integer.parseInt(sc.next());
		
		System.out.println(nameResultMessage + name);
		System.out.println(ageResultMessage + age);
		
	}
}













