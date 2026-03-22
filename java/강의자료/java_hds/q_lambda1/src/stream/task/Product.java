package stream.task;

import java.util.Objects;

public class Product {
	private String name;
	private int price;
	private int stock;
	
	public Product() {;}

	public Product(String name, int price, int stock) {
		super();
		this.name = name;
		this.price = price;
		this.stock = stock;
	}

	public int getTotal() {
		return price * stock;
	}
	
	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public int getPrice() {
		return price;
	}

	public void setPrice(int price) {
		this.price = price;
	}

	public int getStock() {
		return stock;
	}

	public void setStock(int stock) {
		this.stock = stock;
	}

	@Override
	public String toString() {
		return "Product [name=" + name + ", price=" + price + ", stock=" + stock + "]";
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
		return Objects.equals(name, other.name);
	}
}
