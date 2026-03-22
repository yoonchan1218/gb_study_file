package objectTest;

public class EqaulsTest {
	public static void main(String[] args) {
		Customer customer = new Customer(1, "한동석");
		boolean isSame = customer.equals(new Customer(1, "한동석"));
		
		System.out.println(isSame);
	}
}
