package apiTest;

import s_api.Math;

public class MathTest {
	public static void main(String[] args) {
		Math math = new Math();
		int result = math.multiple(3, 5);
		System.out.println(result);
	}
}
