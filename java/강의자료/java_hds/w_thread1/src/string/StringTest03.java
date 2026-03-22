package string;

public class StringTest03 {
	public static void main(String[] args) {
		StringBuilder stringBuilder = new StringBuilder();
		
		stringBuilder.append("이름: ");
		stringBuilder.append("한동석");
		
		System.out.println(stringBuilder.toString());
	}
}
