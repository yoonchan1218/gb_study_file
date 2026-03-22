package classTask;
//주문 번호
//상품들
public class Order {
	long id;
	Product[] arProduct;
	int totalPrice;
	
	public Order() {;}

	public Order(long id, Product[] arProduct) {
		this.id = id;
		this.arProduct = arProduct;
		
		for (int i = 0; i < arProduct.length; i++) {
			totalPrice += arProduct[i].price;
			arProduct[i].stock --;
		}
	}
	
	
}












