package thread.test;

public class ThreadTest {
	public static void main(String[] args) {
//		Thread1 thread1 = new Thread1("♥");
//		Thread1 thread2 = new Thread1("★");
		
//		thread1.run();
//		thread2.run();
		
//		thread1.start();
//		thread2.start();
		
		Runnable resource1 = new Thread2();
		Runnable resource2 = new Thread2();
		
		Thread thread1 = new Thread(resource1, "?");
		Thread thread2 = new Thread(resource2, "!");
		
		thread1.start();
		thread2.start();
		
	}
}


















