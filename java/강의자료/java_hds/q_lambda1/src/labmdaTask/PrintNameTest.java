package labmdaTask;

public class PrintNameTest {
	void printFullName(PrintName printName, String firstName, String lastName) {
		System.out.println(printName.getFullName(firstName, lastName));
	}
	
	public static void main(String[] args) {
		PrintNameTest printNameTest = new PrintNameTest();
		printNameTest.printFullName((f, l) -> l + f, "동석", "한");
	}
}














