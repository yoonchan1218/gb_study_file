package list.task.product;

public class Product {
	private long id;
	private String productName;
	private int productPrice;
	private int productStock;
	
	public Product() {;}

	public Product(Product product) {
		this(product.id, product.productName, product.productPrice, product.productStock);
	}
	
	public Product(long id, String productName, int productPrice, int productStock) {
		super();
		this.id = id;
		this.productName = productName;
		this.productPrice = productPrice;
		this.productStock = productStock;
	}

	public long getId() {
		return id;
	}

	public void setId(long id) {
		this.id = id;
	}

	public String getProductName() {
		return productName;
	}

	public void setProductName(String productName) {
		this.productName = productName;
	}

	public int getProductPrice() {
		return productPrice;
	}

	public void setProductPrice(int productPrice) {
		this.productPrice = productPrice;
	}

	public int getProductStock() {
		return productStock;
	}

	public void setProductStock(int productStock) {
		this.productStock = productStock;
	}

	@Override
	public String toString() {
		return "Product [id=" + id + ", productName=" + productName + ", productPrice=" + productPrice
				+ ", productStock=" + productStock + "]";
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Product other = (Product) obj;
		return id == other.id;
	}
}
