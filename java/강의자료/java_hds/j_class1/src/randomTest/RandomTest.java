package randomTest;

import java.util.Random;

public class RandomTest {
	public static void main(String[] args) {
		Random random = new Random();
		String str = "abcdefghizklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890";
		String code = "";
//		0 ~ 9 중 1개의 난수 발생
//		System.out.println(random.nextInt(10));
		
		for (int i = 0; i < 10; i++) {
			code += str.charAt(random.nextInt(str.length()));
		}
		
		System.out.println(code);
	}
}

















