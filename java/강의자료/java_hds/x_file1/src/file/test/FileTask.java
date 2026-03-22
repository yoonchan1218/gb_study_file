package file.test;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class FileTask {
	public static void main(String[] args) throws IOException{
//		생선 종류를 작성한 뒤
//		전체 생선 종류를 콘솔에 출력한다.
//		생선은 최대 3개까지만 작성한다.
//		파일 이름: fish.txt
//		경로: ./
		BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter("./fish.txt", true));
		bufferedWriter.write("광어\n");
		bufferedWriter.write("방어\n");
		bufferedWriter.write("감성돔\n");
		bufferedWriter.close();
		
		BufferedReader bufferedReader = null; 
		
		try {
			bufferedReader = new BufferedReader(new FileReader("./fish.txt"));
			String line = null;
			
			while((line = bufferedReader.readLine()) != null) {
				System.out.println(line);
			}
			
			
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
		bufferedReader.close();
	}
}
