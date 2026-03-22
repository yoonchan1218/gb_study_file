package classTask;

// 상품 클래스
// 상품명
// 상품 가격
// 상품 재고

// 주문 클래스
// 주문 번호
// 상품들

// 주문에서 결제할 총 금액을 계산할 수 있다.
public class ClassTask06 {
	public static void main(String[] args) {
		//	화면
		Product[] arProduct = {
			new Product("키보드", 39000, 100),	
			new Product("핸드폰", 898000, 1)	
		};
		
		Order order = null;
		boolean check = false;
		
		for (int i = 0; i < arProduct.length; i++) {
			if(arProduct[i].stock <= 0) {
				check = true;
				break;
			}
		}
		
		if(!check) {
			order = new Order(1, arProduct);
			System.out.println(order.totalPrice);
			
			for (int i = 0; i < arProduct.length; i++) {
				System.out.println(arProduct[i].stock);
			}
		}else {
			System.out.println("재고가 부족한 상품이 있습니다.");
		}
	}
}

















