package copy;

import java.util.Objects;

public class Address {
	private String address;
	private String detailAddress;
	
	public Address() {;}
	
	public Address(Address address) {
		this(address.getAddress(), address.getDetailAddress());
	}

	public Address(String address, String detailAddress) {
		super();
		this.address = address;
		this.detailAddress = detailAddress;
	}

	public String getAddress() {
		return address;
	}

	public void setAddress(String address) {
		this.address = address;
	}

	public String getDetailAddress() {
		return detailAddress;
	}

	public void setDetailAddress(String detailAddress) {
		this.detailAddress = detailAddress;
	}

	@Override
	public String toString() {
		return "Address [address=" + address + ", detailAddress=" + detailAddress + "]";
	}

	@Override
	public int hashCode() {
		return Objects.hash(address, detailAddress);
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Address other = (Address) obj;
		return Objects.equals(address, other.address) && Objects.equals(detailAddress, other.detailAddress);
	}
	
}

