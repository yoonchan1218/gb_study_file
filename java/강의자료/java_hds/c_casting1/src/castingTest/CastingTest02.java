package castingTest;

public class CastingTest02 {
	public static void main(String[] args) {
		System.out.println("" + 3 + 8);
		
//		위의 결과가 11이 나오도록 수정한다, 결과는 문자열이여야 한다.
		System.out.println(3 + 8 + "");
		
//		"1 + 3 = 4"
//		위 문자열에서 4를 변수에 담고 사용한다.
		String data = "1 + 3 = ";
		int number = 4;
		String result = data + number;
		
		System.out.println(result);
		
	}
}











