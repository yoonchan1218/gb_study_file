package thread.test;

public class Thread1 extends Thread {
	private String data;
	
	public Thread1() {;}

	public Thread1(String data) {
		super();
		this.data = data;
	}

	public String getData() {
		return data;
	}

	public void setData(String data) {
		this.data = data;
	}

	@Override
	public String toString() {
		return "Thread1 [data=" + data + "]";
	}
	
	@Override
	public void run() {
//		쓰레드가 접근하는 자원
		for (int i = 0; i < 10; i++) {
			System.out.println(data);
			try {sleep(1000);} catch (InterruptedException e) {;}
		}
	}
}




















