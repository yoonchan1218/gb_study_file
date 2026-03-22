package classTask;

public class Market {
	String productName;
	int productPrice;
	int productStock;
	
	public Market() {;}

	public Market(String productName, int productPrice, int productStock) {
		this.productName = productName;
		this.productPrice = productPrice;
		this.productStock = productStock;
	}
	
	void sell(Customer customer) {
		customer.money -= productPrice * (1 - customer.discount / 100.0);
		productStock--;
	}
}


















