package classTask;

public class ClassTask11 {
//	우체국 택배(PostOffice)
//	kg당 가격
	
//	박스(Box)
//	kg
	
//	우체국의 택배서비스를 이용하고자 할 때
//	전달한 모든 박스의 가격을 구한다.
	public static void main(String[] args) {
//		화면
		Box[] arBox = {
				new Box(3),
				new Box(8),
				new Box(2)
		};
		
		PostOffice postOffice = new PostOffice();
		
		int totalPrice = postOffice.delivery(arBox);
		
		System.out.println(totalPrice);
		
		
	}
}











