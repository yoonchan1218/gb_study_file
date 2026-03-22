package staticTest;

// static
// 모든 객체가 공유하는 값
// 클래스당 1개만 만들어지기 때문에 객체가 아닌 클래스명으로 접근한다.
// 생성자가 아니라 컴파일러가 메모리에 가장 먼저 할당해준다.
class Data {
	int data;
	static int data_s = 10;
	
	public Data() {;}

	public Data(int data) {
		this.data = data;
	}
	
	void increase() {
		System.out.println(++data);
	}
	
	static void increase_s( ) {
		System.out.println(++data_s);
	}
	
}

public class StaticTest {
	public static void main(String[] args) {
		Data data1 = new Data(10);
		Data data2 = new Data();
		
		Data.increase_s();
		Data.increase_s();
		Data.increase_s();
		Data.increase_s();
		Data.increase_s();
		Data.increase_s();
		Data.increase_s();
		Data.increase_s();
		Data.increase_s();
		Data.increase_s();
		
		
//		data2.increase_s();
//		data2.increase_s();
//		data2.increase_s();
//		data2.increase_s();
//		data2.increase_s();
//		
//		data2 = new Data();
//		
//		data2.increase_s();
//		data2.increase_s();
//		data2.increase_s();
//		data2.increase_s();
//		data2.increase_s();
		
//		data1.increase();
//		data1.increase();
//		data1.increase();
//		data1.increase();
//		data1.increase();
//		
//		data1 = new Data(10);
//		
//		data1.increase();
//		data1.increase();
//		data1.increase();
//		data1.increase();
//		data1.increase();
	}
}















