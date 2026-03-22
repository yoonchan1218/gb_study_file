// 상품 정보를 객체로 구성한다.
// 상품 번호, 상품명, 가격, 재고-1, 재고-2
// 각 정보를 출력하되, 재고-1과 재고-2는 반복문을 사용해서 출력한다.
// 재고-1이 실재고이고, 재고-2는 기타재고이다.
// 재고-1을 사용하여 총 가격을 리턴하는 메소드를 선언한다.
const product = {
    id: 1,
    productName: "보리차",
    productPrice: 3000,
    "stock-1": 32,
    "stock-2": -2,
    getTotalPrice: function () {
        return this.productPrice * this["stock-1"];
    },
};

with (product) {
    console.log(id, productName, productPrice);
    for (let i = 0; i < 2; i++) {
        console.log(product[`stock-${i + 1}`]);
    }

    console.log(product.getTotalPrice());
}
