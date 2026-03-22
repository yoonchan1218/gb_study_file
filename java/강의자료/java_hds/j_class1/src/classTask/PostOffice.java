package classTask;

public class PostOffice {
	final static int PRICE = 1000;
	
	int delivery(Box[] arBox) {
		int total = 0;
		for (int i = 0; i < arBox.length; i++) {
			total += arBox[i].kg * PRICE;
		}
		
		return total;
	}
}
