package labmdaTest;

public class LambdaTest {
	public static void main(String[] args) {
//		LambdaInter lambdaInter = new LambdaInter() {
//			
//			@Override
//			public boolean checkMutipleOf10(int number) {
//				return number % 10 == 0;
//			}
//		};
		
//		(1)
//		LambdaInter lambdaInter = (number) -> number % 10 == 0;
//		(2)
//		LambdaInter lambdaInter = (number) -> {return number % 10 == 0;};
//		(3)
//		LambdaInter lambdaInter = number -> number % 10 == 0;
//		(4)
		LambdaInter lambdaInter = number -> {return number % 10 == 0;};
		
		boolean result = lambdaInter.checkMutipleOf10(21);
		System.out.println(result);
	}
}

















