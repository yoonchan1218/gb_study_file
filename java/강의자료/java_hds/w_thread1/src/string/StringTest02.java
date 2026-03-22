package string;

public class StringTest02 {
	public static void main(String[] args) {
		long start = 0L, end = 0L;
		
		StringBuilder stringBuilder = new StringBuilder();
		start = System.nanoTime();
		for (int i = 0; i < 1_000_000; i++) {
			stringBuilder.append("안녕");
		}
		end = System.nanoTime();
		System.out.println("StringBuilder: " + (end - start) + "ns");
		
		StringBuffer stringBuffer = new StringBuffer();
		start = System.nanoTime();
		for (int i = 0; i < 1_000_000; i++) {
			stringBuffer.append("안녕");
		}
		end = System.nanoTime();
		System.out.println("StringBuffer: " + (end - start) + "ns");
		
	}
}







