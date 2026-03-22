package list.task.product;

import java.util.ArrayList;
import java.util.List;

import list.task.DBConnecter;

public class ProductService {
//	- 상품 추가
	public void insert(Product product) {
		DBConnecter.products.add(new Product(product));
	}
	
//	- 상품 수정
	public void update(Product product) {
		DBConnecter.products.set(DBConnecter.products.indexOf(product), new Product(product));
	}
	
//	- 상품 삭제
	public void delete(Product product) {
		DBConnecter.products.remove(product);
	}
	
//	- 상품 조회
	public Product findById(long id) {
		Product product = null;
		for(Product data : DBConnecter.products) {
			if(data.getId() == id) {
				product = new Product(data);
			}
		}
		
		return product;
	}
	
//	- 상품 목록
	public List<Product> findAll(){
		List<Product> products = new ArrayList<Product>();
		for(Product product : DBConnecter.products) {
			products.add(new Product(product));
		}
		
		return products;
	}
	

}
















