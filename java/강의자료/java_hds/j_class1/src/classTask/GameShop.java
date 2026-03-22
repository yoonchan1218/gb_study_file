package classTask;

public class GameShop {
//	아이템이름
//	가격
//	재고
	String name;
	int price;
	int stock;
	
	public GameShop() {;}

	public GameShop(String name, int price, int stock) {
		this.name = name;
		this.price = price;
		this.stock = stock;
	}
	
//	개별 주문
	void sell(Player player) {
		player.money -= price * (1 - player.discount / 100.0);
		stock--;
	}
	
//	단체 주문
	void sell(Player[] arPlayer) {
		for (int i = 0; i < arPlayer.length; i++) {
			arPlayer[i].money -= price * (1 - arPlayer[i].discount / 100.0);
			stock--;
		}
	}
	
}












