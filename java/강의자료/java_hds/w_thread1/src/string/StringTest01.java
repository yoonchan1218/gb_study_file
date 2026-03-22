package string;

public class StringTest01 {
	public static void main(String[] args) {
//		문자열은 Constant Pool에 할당된다.
//		만약 동일한 문자열값이 있다면, 해당 필드의 주소를 공유한다.
		String data1 = "ABC";
		String data2 = "ABC";
		
//		직접 객체화를 하게 되면 Heap 메모리에 할당된다.
		String data3 = new String("ABC");
		
		System.out.println(data1 == data2);
		
//		Heap 메모리에 할당된 객체에 intern()을 사용하면,
//		Constant Pool에 가서 있으면 그 주소를 가져오고,
//		없으면 Constant Pool에 등록하고 그 주소를 가져와준다.
		System.out.println(data1 == data3.intern());
	}
}















